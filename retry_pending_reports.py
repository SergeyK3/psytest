#!/usr/bin/env python3
"""Manually inspect or retry protected pending PDF reports."""

from __future__ import annotations

import argparse
from pathlib import Path

from google_drive_service import GoogleDriveUploader
from report_delivery import (
    cleanup_uploaded_reports,
    iter_pending_reports,
    pending_reports_dir_from_environment,
    report_work_dir_from_environment,
    retry_pending_reports,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pending-dir",
        type=Path,
        default=pending_reports_dir_from_environment(),
        help="Pending directory (defaults to PENDING_REPORTS_DIR)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually contact Google Drive; without this flag the command is offline/dry-run",
    )
    parser.add_argument(
        "--cleanup-uploaded",
        action="store_true",
        help="Delete upload-confirmed local cleanup markers without contacting Drive",
    )
    parser.add_argument(
        "--stale-after-seconds",
        type=float,
        default=3600.0,
        help="Recover processing claims older than this value during --execute",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    pending_count = len(tuple(iter_pending_reports(args.pending_dir)))
    if not args.execute and not args.cleanup_uploaded:
        print(f"Dry run: {pending_count} pending PDF report(s); no external API was called.")
        return 0

    if args.cleanup_uploaded:
        work_removed, work_errors = cleanup_uploaded_reports(report_work_dir_from_environment())
        pending_removed, pending_errors = cleanup_uploaded_reports(args.pending_dir)
        error_types = tuple(sorted(set(work_errors + pending_errors)))
        print(
            f"Local cleanup: removed={work_removed + pending_removed}, "
            f"failed={len(error_types)}, error_types={','.join(error_types) or 'none'}; "
            "no external API was called."
        )
        if not args.execute:
            return 0 if not error_types else 1

    uploader = GoogleDriveUploader.from_environment()
    summary = retry_pending_reports(
        args.pending_dir,
        lambda path, report_date, remote_name: _upload(
            uploader, path, report_date, remote_name
        ),
        stale_after_seconds=args.stale_after_seconds,
    )
    print(
        f"Retry complete: attempted={summary.attempted}, "
        f"uploaded={summary.uploaded}, retained={summary.retained}, "
        f"failed={summary.failed}, skipped={summary.skipped}, "
        f"recovered={summary.recovered}, cleanup_pending={summary.cleanup_pending}, "
        f"error_types={','.join(summary.error_types) or 'none'}"
    )
    return 0 if summary.failed == 0 and summary.cleanup_pending == 0 else 1


def _upload(
    uploader: GoogleDriveUploader,
    path: Path,
    report_date,
    remote_name: str,
) -> str:
    result = uploader.upload(path, report_date=report_date, remote_name=remote_name)
    return result.web_view_link or "uploaded"


if __name__ == "__main__":
    raise SystemExit(main())
