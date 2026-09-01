"""Reliable delivery, pending claims, retry, and local cleanup handling."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Callable, Iterable, Optional

from runtime_lock import InterProcessFileLock, LockTimeoutError


DEFAULT_PENDING_REPORTS_DIR = Path("/var/lib/psytest/pending-reports")
DEFAULT_REPORT_WORK_DIR = Path("docs")
REPORT_DATE_PATTERN = re.compile(r"^(\d{4})-(\d{2})-(\d{2})_")
PROCESSING_MARKER = ".processing-"
UPLOADED_CLEANUP_MARKER = ".uploaded-cleanup-"
QUEUED_CLEANUP_MARKER = ".queued-cleanup-"


class PendingQueueError(RuntimeError):
    """Raised when a report cannot be safely published to pending."""


class DeliveryState(str, Enum):
    UPLOADED = "uploaded"
    UPLOADED_CLEANUP_PENDING = "uploaded_cleanup_pending"
    QUEUED = "queued"
    QUEUED_CLEANUP_PENDING = "queued_cleanup_pending"
    FAILED_RETAINED = "failed_retained"


@dataclass(frozen=True)
class PendingPublishResult:
    path: Path
    source_cleanup_path: Optional[Path] = None
    cleanup_error_type: Optional[str] = None


@dataclass(frozen=True)
class DeliveryResult:
    state: DeliveryState
    remote_reference: Optional[str] = None
    pending_path: Optional[Path] = None
    cleanup_path: Optional[Path] = None
    upload_error_type: Optional[str] = None
    pending_error_type: Optional[str] = None
    cleanup_error_type: Optional[str] = None

    @property
    def uploaded(self) -> bool:
        return self.state in {
            DeliveryState.UPLOADED,
            DeliveryState.UPLOADED_CLEANUP_PENDING,
        }


@dataclass(frozen=True)
class RetrySummary:
    attempted: int
    uploaded: int
    retained: int
    failed: int
    skipped: int
    recovered: int
    cleanup_pending: int
    error_types: tuple[str, ...]


@dataclass(frozen=True)
class ClaimedReport:
    processing_path: Path
    original_name: str


def pending_reports_dir_from_environment() -> Path:
    value = os.getenv("PENDING_REPORTS_DIR", "").strip()
    return Path(value) if value else DEFAULT_PENDING_REPORTS_DIR


def report_work_dir_from_environment() -> Path:
    value = os.getenv("REPORT_WORK_DIR", "").strip()
    return Path(value) if value else DEFAULT_REPORT_WORK_DIR


def ensure_private_directory(path: Path) -> Path:
    directory = Path(path)
    if directory.exists() and (not directory.is_dir() or directory.is_symlink()):
        raise PendingQueueError("Runtime path must be a real directory")
    if os.name == "nt":
        directory.mkdir(parents=True, exist_ok=True)
    else:
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        directory.chmod(0o700)
    return directory


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _cleanup_marker_path(source: Path, marker: str) -> Path:
    return source.with_name(f"{source.name}{marker}{uuid.uuid4().hex}")


def _mark_local_cleanup(source: Path, marker: str) -> Path:
    cleanup_path = _cleanup_marker_path(source, marker)
    os.rename(source, cleanup_path)
    return cleanup_path


def _source_lock_path(source: Path, pending_dir: Path) -> Path:
    digest = hashlib.sha256(str(source.resolve()).encode("utf-8")).hexdigest()
    return pending_dir / ".locks" / f"enqueue-{digest}.lock"


def enqueue_pending_report(source_path: Path, pending_dir: Path) -> PendingPublishResult:
    """Publish a unique pending copy atomically, then remove the source.

    The full copy is written and fsynced inside pending. ``os.link`` publishes it
    without overwrite semantics; the source is touched only after publication.
    """
    source = Path(source_path)
    target_dir = ensure_private_directory(Path(pending_dir))
    lock_path = _source_lock_path(source, target_dir)

    with InterProcessFileLock(lock_path):
        if not source.is_file() or source.is_symlink() or source.suffix.lower() != ".pdf":
            raise PendingQueueError("Only an existing regular PDF may be queued")

        temporary_path = target_dir / f"pending-{uuid.uuid4().hex}.tmp"
        target: Optional[Path] = None
        temporary_cleanup_error: Optional[str] = None
        try:
            with source.open("rb") as source_file, temporary_path.open("xb") as temporary_file:
                shutil.copyfileobj(source_file, temporary_file)
                temporary_file.flush()
                os.fsync(temporary_file.fileno())
            if os.name != "nt":
                temporary_path.chmod(0o600)

            while target is None:
                candidate = target_dir / f"{source.stem}_{uuid.uuid4().hex}.pdf"
                try:
                    os.link(temporary_path, candidate)
                    target = candidate
                except FileExistsError:
                    continue
            try:
                _fsync_directory(target_dir)
            except Exception:
                target.unlink(missing_ok=True)
                raise
        except Exception as exc:
            temporary_path.unlink(missing_ok=True)
            raise PendingQueueError("Failed to atomically publish the full report") from exc

        try:
            temporary_path.unlink()
        except Exception as cleanup_exc:
            # The unique PDF target is already fully published. A leftover .tmp
            # file is not eligible for retry and must not invalidate publication.
            temporary_cleanup_error = type(cleanup_exc).__name__

        try:
            source.unlink()
            return PendingPublishResult(
                path=target,
                cleanup_error_type=temporary_cleanup_error,
            )
        except Exception as cleanup_exc:
            try:
                cleanup_path = _mark_local_cleanup(source, QUEUED_CLEANUP_MARKER)
            except Exception:
                cleanup_path = source
            return PendingPublishResult(
                path=target,
                source_cleanup_path=cleanup_path,
                cleanup_error_type=temporary_cleanup_error or type(cleanup_exc).__name__,
            )


def deliver_full_report(
    report_path: Path,
    upload: Callable[[Path], Optional[str]],
    pending_dir: Path,
) -> DeliveryResult:
    """Upload a report and keep upload confirmation separate from cleanup."""
    path = Path(report_path)
    try:
        remote_reference = upload(path)
        if not remote_reference:
            raise RuntimeError("Drive upload was not confirmed")
    except Exception as upload_exc:
        try:
            published = enqueue_pending_report(path, pending_dir)
        except Exception as pending_exc:
            return DeliveryResult(
                state=DeliveryState.FAILED_RETAINED,
                cleanup_path=path if path.exists() else None,
                upload_error_type=type(upload_exc).__name__,
                pending_error_type=type(pending_exc).__name__,
            )
        return DeliveryResult(
            state=(
                DeliveryState.QUEUED_CLEANUP_PENDING
                if published.source_cleanup_path
                else DeliveryState.QUEUED
            ),
            pending_path=published.path,
            cleanup_path=published.source_cleanup_path,
            upload_error_type=type(upload_exc).__name__,
            cleanup_error_type=published.cleanup_error_type,
        )

    try:
        cleanup_path = _mark_local_cleanup(path, UPLOADED_CLEANUP_MARKER)
    except Exception as cleanup_exc:
        return DeliveryResult(
            state=DeliveryState.UPLOADED_CLEANUP_PENDING,
            remote_reference=remote_reference,
            cleanup_path=path,
            cleanup_error_type=type(cleanup_exc).__name__,
        )
    try:
        cleanup_path.unlink()
        return DeliveryResult(
            state=DeliveryState.UPLOADED,
            remote_reference=remote_reference,
        )
    except Exception as cleanup_exc:
        return DeliveryResult(
            state=DeliveryState.UPLOADED_CLEANUP_PENDING,
            remote_reference=remote_reference,
            cleanup_path=cleanup_path,
            cleanup_error_type=type(cleanup_exc).__name__,
        )


def report_date_from_filename(path: Path, fallback_path: Optional[Path] = None) -> datetime:
    match = REPORT_DATE_PATTERN.match(path.name)
    if match:
        try:
            return datetime(*(int(part) for part in match.groups()))
        except ValueError:
            pass
    stat_path = fallback_path or path
    return datetime.fromtimestamp(stat_path.stat().st_mtime)


def iter_pending_reports(pending_dir: Path) -> Iterable[Path]:
    directory = Path(pending_dir)
    if not directory.exists():
        return ()
    if not directory.is_dir() or directory.is_symlink():
        raise PendingQueueError("Pending report path must be a real directory")
    return tuple(
        path
        for path in sorted(directory.glob("*.pdf"))
        if path.is_file() and not path.is_symlink()
    )


def _processing_original_name(processing_path: Path) -> str:
    return processing_path.name.split(PROCESSING_MARKER, 1)[0]


def _processing_lease_path(processing_path: Path) -> Path:
    digest = hashlib.sha256(processing_path.name.encode("utf-8")).hexdigest()
    return processing_path.parent / ".locks" / f"lease-{digest}.lock"


def claim_pending_report(
    path: Path, claimed_at: Optional[float] = None
) -> Optional[ClaimedReport]:
    source = Path(path)
    claim_timestamp = int(claimed_at if claimed_at is not None else time.time())
    processing = source.with_name(
        f"{source.name}{PROCESSING_MARKER}{claim_timestamp}-{uuid.uuid4().hex}"
    )
    claim_lock = source.parent / ".locks" / "retry-claims.lock"
    with InterProcessFileLock(claim_lock):
        if not source.is_file() or source.is_symlink():
            return None
        try:
            os.rename(source, processing)
        except FileNotFoundError:
            return None
    return ClaimedReport(processing_path=processing, original_name=source.name)


def _restore_claim(claim: ClaimedReport) -> Path:
    source = claim.processing_path
    original = Path(claim.original_name)
    candidate = source.parent / f"{original.stem}_retry_{uuid.uuid4().hex}.pdf"
    os.rename(source, candidate)
    return candidate


def recover_stale_processing(pending_dir: Path, stale_after_seconds: float) -> int:
    directory = Path(pending_dir)
    if not directory.exists():
        return 0
    cutoff = datetime.now().timestamp() - stale_after_seconds
    recovered = 0
    claim_lock = directory / ".locks" / "retry-claims.lock"
    with InterProcessFileLock(claim_lock):
        for processing in tuple(directory.glob(f"*.pdf{PROCESSING_MARKER}*")):
            if UPLOADED_CLEANUP_MARKER in processing.name:
                continue
            try:
                claim_suffix = processing.name.split(PROCESSING_MARKER, 1)[1]
                claim_timestamp_text = claim_suffix.split("-", 1)[0]
                try:
                    claim_timestamp = float(claim_timestamp_text)
                except ValueError:
                    claim_timestamp = processing.stat().st_mtime
                if claim_timestamp > cutoff:
                    continue
                try:
                    with InterProcessFileLock(
                        _processing_lease_path(processing), timeout_seconds=0
                    ):
                        original = Path(_processing_original_name(processing))
                        target = directory / f"{original.stem}_recovered_{uuid.uuid4().hex}.pdf"
                        os.rename(processing, target)
                        recovered += 1
                except LockTimeoutError:
                    continue
            except FileNotFoundError:
                continue
    return recovered


def cleanup_uploaded_reports(work_dir: Path) -> tuple[int, tuple[str, ...]]:
    """Delete local cleanup markers without performing any Drive operation."""
    directory = Path(work_dir)
    if not directory.exists():
        return 0, ()
    removed = 0
    errors: list[str] = []
    patterns = (f"*{UPLOADED_CLEANUP_MARKER}*", f"*{QUEUED_CLEANUP_MARKER}*")
    for pattern in patterns:
        for path in tuple(directory.glob(pattern)):
            try:
                path.unlink()
                removed += 1
            except Exception as exc:
                errors.append(type(exc).__name__)
    return removed, tuple(sorted(set(errors)))


def retry_pending_reports(
    pending_dir: Path,
    upload: Callable[[Path, datetime, str], Optional[str]],
    stale_after_seconds: float = 3600.0,
) -> RetrySummary:
    recovered = recover_stale_processing(pending_dir, stale_after_seconds)
    attempted = uploaded = retained = failed = skipped = cleanup_pending = 0
    error_types: list[str] = []

    for report_path in iter_pending_reports(pending_dir):
        claim = claim_pending_report(report_path)
        if claim is None:
            skipped += 1
            continue
        attempted += 1
        with InterProcessFileLock(_processing_lease_path(claim.processing_path)):
            try:
                remote_reference = upload(
                    claim.processing_path,
                    report_date_from_filename(
                        Path(claim.original_name), fallback_path=claim.processing_path
                    ),
                    claim.original_name,
                )
                if not remote_reference:
                    raise RuntimeError("Drive upload was not confirmed")
            except Exception as exc:
                error_types.append(type(exc).__name__)
                failed += 1
                try:
                    _restore_claim(claim)
                except Exception as restore_exc:
                    error_types.append(type(restore_exc).__name__)
                retained += 1
                continue

            uploaded += 1
            try:
                cleanup_path = _mark_local_cleanup(
                    claim.processing_path, UPLOADED_CLEANUP_MARKER
                )
            except Exception as cleanup_exc:
                error_types.append(type(cleanup_exc).__name__)
                cleanup_pending += 1
                continue
            try:
                cleanup_path.unlink()
            except Exception as cleanup_exc:
                error_types.append(type(cleanup_exc).__name__)
                cleanup_pending += 1

    return RetrySummary(
        attempted=attempted,
        uploaded=uploaded,
        retained=retained,
        failed=failed,
        skipped=skipped,
        recovered=recovered,
        cleanup_pending=cleanup_pending,
        error_types=tuple(sorted(set(error_types))),
    )
