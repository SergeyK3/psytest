"""Google Drive upload support for production reports.

Credentials and the destination folder are configuration, never repository data.
The Google client is imported lazily so unit tests can use a fake service without
network access or credentials.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from runtime_lock import InterProcessFileLock


FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"
PDF_MIME_TYPE = "application/pdf"
DRIVE_SCOPE = "https://www.googleapis.com/auth/drive.file"
DEFAULT_DRIVE_LOCK_PATH = Path("/var/lib/psytest/locks/google-drive-folders.lock")
MONTH_NAMES = (
    "",
    "01-January",
    "02-February",
    "03-March",
    "04-April",
    "05-May",
    "06-June",
    "07-July",
    "08-August",
    "09-September",
    "10-October",
    "11-November",
    "12-December",
)


class DriveConfigurationError(ValueError):
    """Raised when required Drive configuration is absent or unsafe."""


class DriveUploadError(RuntimeError):
    """Raised when Drive does not confirm an upload."""


@dataclass(frozen=True)
class DriveConfig:
    credentials_path: Path
    parent_folder_id: str
    folder_lock_path: Path

    @classmethod
    def from_environment(cls) -> "DriveConfig":
        credentials_value = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
        parent_folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "").strip()
        lock_value = os.getenv("GOOGLE_DRIVE_LOCK_PATH", "").strip()

        if not credentials_value:
            raise DriveConfigurationError("GOOGLE_APPLICATION_CREDENTIALS is required")
        if not parent_folder_id:
            raise DriveConfigurationError("GOOGLE_DRIVE_FOLDER_ID is required")

        credentials_path = Path(credentials_value)
        if not credentials_path.is_absolute():
            raise DriveConfigurationError("GOOGLE_APPLICATION_CREDENTIALS must be absolute")
        if not credentials_path.is_file():
            raise DriveConfigurationError("Google credentials file does not exist")

        folder_lock_path = Path(lock_value) if lock_value else DEFAULT_DRIVE_LOCK_PATH
        if not folder_lock_path.is_absolute():
            raise DriveConfigurationError("GOOGLE_DRIVE_LOCK_PATH must be absolute")

        return cls(
            credentials_path=credentials_path,
            parent_folder_id=parent_folder_id,
            folder_lock_path=folder_lock_path,
        )


@dataclass(frozen=True)
class DriveUploadResult:
    file_id: str
    web_view_link: Optional[str]
    year_folder_id: str
    month_folder_id: str


def build_drive_service(credentials_path: Path) -> Any:
    """Build a Drive API client from service-account credentials."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    credentials = service_account.Credentials.from_service_account_file(
        str(credentials_path), scopes=[DRIVE_SCOPE]
    )
    return build("drive", "v3", credentials=credentials, cache_discovery=False)


def _default_media_factory(path: Path) -> Any:
    from googleapiclient.http import MediaFileUpload

    return MediaFileUpload(str(path), mimetype=PDF_MIME_TYPE, resumable=False)


def _escape_query_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


class GoogleDriveUploader:
    """Upload reports beneath a configured parent as ``YYYY/MM-Month``."""

    def __init__(
        self,
        service: Any,
        parent_folder_id: str,
        folder_lock_path: Path,
        media_factory: Optional[Callable[[Path], Any]] = None,
    ) -> None:
        if not parent_folder_id.strip():
            raise DriveConfigurationError("Google Drive parent folder ID is required")
        self.service = service
        self.parent_folder_id = parent_folder_id.strip()
        self.folder_lock_path = Path(folder_lock_path)
        self.media_factory = media_factory or _default_media_factory

    @classmethod
    def from_environment(cls) -> "GoogleDriveUploader":
        config = DriveConfig.from_environment()
        return cls(
            service=build_drive_service(config.credentials_path),
            parent_folder_id=config.parent_folder_id,
            folder_lock_path=config.folder_lock_path,
        )

    def _find_folder(self, name: str, parent_id: str) -> Optional[str]:
        escaped_name = _escape_query_value(name)
        escaped_parent = _escape_query_value(parent_id)
        query = (
            f"name='{escaped_name}' and mimeType='{FOLDER_MIME_TYPE}' "
            f"and '{escaped_parent}' in parents and trashed=false"
        )
        response = (
            self.service.files()
            .list(
                q=query,
                spaces="drive",
                fields="files(id,name)",
                pageSize=10,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            )
            .execute()
        )
        files = response.get("files", [])
        return str(files[0]["id"]) if files else None

    def _create_folder(self, name: str, parent_id: str) -> str:
        response = (
            self.service.files()
            .create(
                body={
                    "name": name,
                    "mimeType": FOLDER_MIME_TYPE,
                    "parents": [parent_id],
                },
                fields="id",
                supportsAllDrives=True,
            )
            .execute()
        )
        folder_id = response.get("id")
        if not folder_id:
            raise DriveUploadError("Drive did not return a folder ID")
        return str(folder_id)

    def ensure_folder(self, name: str, parent_id: str) -> str:
        return self._find_folder(name, parent_id) or self._create_folder(name, parent_id)

    def ensure_year_month(self, report_date: datetime) -> tuple[str, str]:
        year_folder_id = self.ensure_folder(str(report_date.year), self.parent_folder_id)
        month_folder_id = self.ensure_folder(MONTH_NAMES[report_date.month], year_folder_id)
        return year_folder_id, month_folder_id

    def upload(
        self,
        file_path: Path,
        report_date: Optional[datetime] = None,
        remote_name: Optional[str] = None,
    ) -> DriveUploadResult:
        path = Path(file_path)
        if not path.is_file() or path.is_symlink():
            raise DriveUploadError("Report must be an existing regular file")

        upload_name = remote_name or path.name
        if not upload_name or "/" in upload_name or "\\" in upload_name:
            raise DriveUploadError("Drive report name must not contain path separators")
        if not upload_name.lower().endswith(".pdf"):
            raise DriveUploadError("Drive report name must end with .pdf")

        effective_date = report_date or datetime.now()
        # Folder lookup/create is serialized across live delivery and retry. The
        # potentially slow PDF upload happens after releasing this lock.
        with InterProcessFileLock(self.folder_lock_path):
            year_folder_id, month_folder_id = self.ensure_year_month(effective_date)
        response = (
            self.service.files()
            .create(
                body={"name": upload_name, "parents": [month_folder_id]},
                media_body=self.media_factory(path),
                fields="id,webViewLink",
                supportsAllDrives=True,
            )
            .execute()
        )
        file_id = response.get("id")
        if not file_id:
            raise DriveUploadError("Drive did not confirm the uploaded file")

        return DriveUploadResult(
            file_id=str(file_id),
            web_view_link=response.get("webViewLink"),
            year_folder_id=year_folder_id,
            month_folder_id=month_folder_id,
        )
