import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import retry_pending_reports as retry_cli
from report_delivery import (
    DeliveryState,
    PendingQueueError,
    UPLOADED_CLEANUP_MARKER,
    claim_pending_report,
    cleanup_uploaded_reports,
    deliver_full_report,
    enqueue_pending_report,
    retry_pending_reports,
)


def _make_pdf(path: Path, content: bytes = b"%PDF-1.4\nreport\n") -> Path:
    path.write_bytes(content)
    return path


def test_successful_upload_deletes_local_full_pdf(safe_tmp_path):
    report = _make_pdf(safe_tmp_path / "2026-09-01_user_full.pdf")
    result = deliver_full_report(report, lambda _: "confirmed", safe_tmp_path / "pending")

    assert result.state is DeliveryState.UPLOADED
    assert result.uploaded is True
    assert result.remote_reference == "confirmed"
    assert not report.exists()


def test_failed_upload_atomically_preserves_unique_report_in_pending(safe_tmp_path):
    report = _make_pdf(safe_tmp_path / "2026-09-01_user_full.pdf", b"private report")
    pending = safe_tmp_path / "pending"

    result = deliver_full_report(
        report,
        lambda _: (_ for _ in ()).throw(RuntimeError("offline fake failure")),
        pending,
    )

    assert result.state is DeliveryState.QUEUED
    assert result.pending_path is not None
    assert result.pending_path.name != report.name
    assert result.pending_path.read_bytes() == b"private report"
    assert not report.exists()
    assert not tuple(pending.glob("pending-*.tmp"))


def test_concurrent_pending_publication_never_overwrites(safe_tmp_path):
    report = _make_pdf(safe_tmp_path / "same.pdf", b"one source")
    pending = safe_tmp_path / "pending"
    barrier = threading.Barrier(2)

    def publish():
        barrier.wait()
        try:
            return enqueue_pending_report(report, pending)
        except PendingQueueError:
            return None

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _index: publish(), range(2)))

    published = [result for result in results if result is not None]
    pending_pdfs = tuple(pending.glob("*.pdf"))
    assert len(published) == 1
    assert len(pending_pdfs) == 1
    assert pending_pdfs[0].read_bytes() == b"one source"


def test_upload_success_unlink_failure_is_marked_without_pending_or_reupload(
    safe_tmp_path, monkeypatch
):
    report = _make_pdf(safe_tmp_path / "2026-09-01_full.pdf")
    pending = safe_tmp_path / "pending"
    real_unlink = Path.unlink
    failed_once = False

    def fail_original_unlink(path, *args, **kwargs):
        nonlocal failed_once
        if UPLOADED_CLEANUP_MARKER in path.name and not failed_once:
            failed_once = True
            raise PermissionError("offline cleanup failure")
        return real_unlink(path, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", fail_original_unlink)
    uploads = []
    result = deliver_full_report(report, lambda path: uploads.append(path) or "confirmed", pending)

    assert result.state is DeliveryState.UPLOADED_CLEANUP_PENDING
    assert result.uploaded is True
    assert result.cleanup_error_type == "PermissionError"
    assert result.cleanup_path is not None
    assert result.cleanup_path.exists()
    assert not report.exists()
    assert not pending.exists()
    assert len(uploads) == 1

    removed, errors = cleanup_uploaded_reports(safe_tmp_path)
    assert removed == 1
    assert errors == ()
    assert not result.cleanup_path.exists()
    assert len(uploads) == 1


def test_retry_success_removes_claim_only_after_confirmation(safe_tmp_path):
    pending = safe_tmp_path / "pending"
    pending.mkdir()
    report = _make_pdf(pending / "2026-09-01_user_full.pdf")
    calls = []

    def successful_upload(path, report_date, remote_name):
        calls.append((path, report_date, remote_name, path.exists()))
        return "confirmed"

    summary = retry_pending_reports(pending, successful_upload)

    assert summary.uploaded == 1
    assert summary.failed == 0
    assert not report.exists()
    assert calls[0][1] == datetime(2026, 9, 1)
    assert calls[0][2] == report.name
    assert calls[0][3] is True
    assert not calls[0][0].exists()


def test_retry_failure_restores_unique_pending_report(safe_tmp_path):
    pending = safe_tmp_path / "pending"
    pending.mkdir()
    _make_pdf(pending / "2026-09-01_user_full.pdf")

    summary = retry_pending_reports(
        pending,
        lambda _path, _date, _name: (_ for _ in ()).throw(RuntimeError("offline")),
    )

    assert summary.uploaded == 0
    assert summary.failed == 1
    assert summary.retained == 1
    assert summary.error_types == ("RuntimeError",)
    assert len(tuple(pending.glob("*.pdf"))) == 1
    assert not tuple(pending.glob("*.processing-*"))


def test_retry_upload_cleanup_failure_is_never_reuploaded(safe_tmp_path, monkeypatch):
    pending = safe_tmp_path / "pending"
    pending.mkdir()
    _make_pdf(pending / "2026-09-01_user_full.pdf")
    real_unlink = Path.unlink
    failed_once = False
    upload_count = 0

    def fail_marker_unlink(path, *args, **kwargs):
        nonlocal failed_once
        if UPLOADED_CLEANUP_MARKER in path.name and not failed_once:
            failed_once = True
            raise PermissionError("offline cleanup failure")
        return real_unlink(path, *args, **kwargs)

    def upload(_path, _date, _name):
        nonlocal upload_count
        upload_count += 1
        return "confirmed"

    monkeypatch.setattr(Path, "unlink", fail_marker_unlink)
    first = retry_pending_reports(pending, upload)
    second = retry_pending_reports(pending, upload, stale_after_seconds=0)

    assert first.uploaded == 1
    assert first.cleanup_pending == 1
    assert second.attempted == 0
    assert upload_count == 1
    removed, errors = cleanup_uploaded_reports(pending)
    assert removed == 1
    assert errors == ()


def test_two_concurrent_retries_upload_one_pending_file_once(safe_tmp_path):
    pending = safe_tmp_path / "pending"
    pending.mkdir()
    _make_pdf(pending / "2026-09-01_user_full.pdf")
    start = threading.Barrier(2)
    upload_lock = threading.Lock()
    upload_count = 0
    upload_paths = []

    def upload(_path, _date, _name):
        nonlocal upload_count
        with upload_lock:
            upload_count += 1
            upload_paths.append(_path.name)
        time.sleep(0.1)
        return "confirmed"

    def run_retry():
        start.wait()
        return retry_pending_reports(pending, upload)

    with ThreadPoolExecutor(max_workers=2) as pool:
        summaries = list(pool.map(lambda _index: run_retry(), range(2)))

    assert upload_count == 1, upload_paths
    assert sum(summary.attempted for summary in summaries) == 1
    assert sum(summary.uploaded for summary in summaries) == 1
    assert not tuple(pending.glob("*" + ".pdf"))


def test_active_processing_lease_is_not_recovered_as_stale(safe_tmp_path):
    pending = safe_tmp_path / "pending"
    pending.mkdir()
    _make_pdf(pending / "2026-09-01_user_full.pdf")
    upload_started = threading.Event()
    allow_upload_to_finish = threading.Event()
    upload_count = 0

    def slow_upload(_path, _date, _name):
        nonlocal upload_count
        upload_count += 1
        upload_started.set()
        assert allow_upload_to_finish.wait(timeout=3)
        return "confirmed"

    with ThreadPoolExecutor(max_workers=2) as pool:
        first_future = pool.submit(retry_pending_reports, pending, slow_upload, 0)
        assert upload_started.wait(timeout=3)
        second = retry_pending_reports(
            pending,
            lambda _path, _date, _name: (_ for _ in ()).throw(
                AssertionError("active claim must not be uploaded twice")
            ),
            stale_after_seconds=0,
        )
        allow_upload_to_finish.set()
        first = first_future.result(timeout=3)

    assert first.uploaded == 1
    assert second.attempted == 0
    assert second.recovered == 0
    assert upload_count == 1


def test_stale_processing_claim_is_recovered_and_retried(safe_tmp_path):
    pending = safe_tmp_path / "pending"
    pending.mkdir()
    report = _make_pdf(pending / "2026-09-01_user_full.pdf")
    claim = claim_pending_report(report, claimed_at=time.time() - 7200)
    assert claim is not None

    summary = retry_pending_reports(
        pending,
        lambda _path, _date, _name: "confirmed",
        stale_after_seconds=3600,
    )

    assert summary.recovered == 1
    assert summary.uploaded == 1
    assert not tuple(pending.glob("*.processing-*"))


def test_retry_cli_defaults_to_offline_dry_run_without_claim(safe_tmp_path, monkeypatch, capsys):
    pending = safe_tmp_path / "pending"
    pending.mkdir()
    report = _make_pdf(pending / "2026-09-01_user_full.pdf")
    stale_source = _make_pdf(pending / "2026-08-31_stale_full.pdf")
    stale_claim = claim_pending_report(stale_source, claimed_at=time.time() - 7200)
    assert stale_claim is not None

    monkeypatch.setattr(
        retry_cli.GoogleDriveUploader,
        "from_environment",
        lambda: (_ for _ in ()).throw(AssertionError("Drive must not initialize")),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["retry_pending_reports.py", "--pending-dir", str(pending)],
    )

    assert retry_cli.main() == 0
    assert "no external API was called" in capsys.readouterr().out
    assert report.exists()
    assert stale_claim.processing_path.exists()


def test_retry_cli_execute_reports_safe_failure_counts(safe_tmp_path, monkeypatch, capsys):
    pending = safe_tmp_path / "pending"
    pending.mkdir()
    _make_pdf(pending / "2026-09-01_user_full.pdf")

    class FailingUploader:
        def upload(self, _path, report_date=None, remote_name=None):
            raise TimeoutError("sensitive provider detail must not be printed")

    monkeypatch.setattr(
        retry_cli.GoogleDriveUploader,
        "from_environment",
        lambda: FailingUploader(),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["retry_pending_reports.py", "--pending-dir", str(pending), "--execute"],
    )

    assert retry_cli.main() == 1
    output = capsys.readouterr().out
    assert "uploaded=0" in output
    assert "retained=1" in output
    assert "failed=1" in output
    assert "error_types=TimeoutError" in output
    assert "sensitive provider detail" not in output
