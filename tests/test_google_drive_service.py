import re
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from google_drive_service import FOLDER_MIME_TYPE, GoogleDriveUploader


class FakeRequest:
    def __init__(self, response):
        self.response = response

    def execute(self):
        return self.response


class FakeFiles:
    def __init__(self):
        self.list_calls = []
        self.create_calls = []
        self.next_id = 1

    def list(self, **kwargs):
        self.list_calls.append(kwargs)
        return FakeRequest({"files": []})

    def create(self, **kwargs):
        self.create_calls.append(kwargs)
        body = kwargs["body"]
        if body.get("mimeType") == FOLDER_MIME_TYPE:
            response = {"id": f"folder-{self.next_id}"}
        else:
            response = {"id": f"file-{self.next_id}", "webViewLink": "fake-link"}
        self.next_id += 1
        return FakeRequest(response)


class FakeDrive:
    def __init__(self):
        self.files_resource = FakeFiles()

    def files(self):
        return self.files_resource


def test_upload_creates_year_month_under_configured_parent_without_network(safe_tmp_path):
    report = safe_tmp_path / "full.pdf"
    report.write_bytes(b"%PDF-1.4\noffline\n")
    drive = FakeDrive()
    uploader = GoogleDriveUploader(
        drive,
        parent_folder_id="configured-parent",
        folder_lock_path=safe_tmp_path / "drive.lock",
        media_factory=lambda path: ("fake-media", path.name),
    )

    result = uploader.upload(report, report_date=datetime(2026, 9, 1))

    creates = drive.files_resource.create_calls
    assert creates[0]["body"] == {
        "name": "2026",
        "mimeType": FOLDER_MIME_TYPE,
        "parents": ["configured-parent"],
    }
    assert creates[1]["body"] == {
        "name": "09-September",
        "mimeType": FOLDER_MIME_TYPE,
        "parents": [result.year_folder_id],
    }
    assert creates[2]["body"] == {
        "name": "full.pdf",
        "parents": [result.month_folder_id],
    }
    assert result.file_id
    assert result.web_view_link == "fake-link"
    assert len(drive.files_resource.list_calls) == 2


def test_existing_year_and_month_are_reused(safe_tmp_path):
    report = safe_tmp_path / "full.pdf"
    report.write_bytes(b"%PDF-1.4\n")
    drive = FakeDrive()
    responses = iter(
        [
            {"files": [{"id": "existing-year", "name": "2026"}]},
            {"files": [{"id": "existing-month", "name": "09-September"}]},
        ]
    )
    drive.files_resource.list = lambda **_kwargs: FakeRequest(next(responses))
    uploader = GoogleDriveUploader(
        drive,
        parent_folder_id="configured-parent",
        folder_lock_path=safe_tmp_path / "drive.lock",
        media_factory=lambda _path: "fake-media",
    )

    result = uploader.upload(report, report_date=datetime(2026, 9, 1))

    assert result.year_folder_id == "existing-year"
    assert result.month_folder_id == "existing-month"
    assert len(drive.files_resource.create_calls) == 1
    assert drive.files_resource.create_calls[0]["body"]["parents"] == ["existing-month"]


def test_processing_claim_uploads_with_original_pdf_remote_name(safe_tmp_path):
    processing = safe_tmp_path / "report.pdf.processing-claim"
    processing.write_bytes(b"%PDF-1.4\n")
    drive = FakeDrive()
    uploader = GoogleDriveUploader(
        drive,
        parent_folder_id="configured-parent",
        folder_lock_path=safe_tmp_path / "drive.lock",
        media_factory=lambda path: ("fake-media", path.name),
    )

    uploader.upload(
        processing,
        report_date=datetime(2026, 9, 1),
        remote_name="report.pdf",
    )

    assert drive.files_resource.create_calls[-1]["body"]["name"] == "report.pdf"


class CallbackRequest:
    def __init__(self, callback):
        self.callback = callback

    def execute(self):
        return self.callback()


class ConcurrentFakeFiles:
    def __init__(self, upload_barrier):
        self.upload_barrier = upload_barrier
        self.lock = threading.Lock()
        self.folders = {}
        self.folder_creates = []
        self.file_creates = []
        self.next_id = 1

    def list(self, **kwargs):
        query = kwargs["q"]
        name = re.search(r"name='([^']+)'", query).group(1)
        parent = re.search(r"and '([^']+)' in parents", query).group(1)

        def response():
            with self.lock:
                folder_id = self.folders.get((parent, name))
            return {"files": [{"id": folder_id, "name": name}]} if folder_id else {"files": []}

        return CallbackRequest(response)

    def create(self, **kwargs):
        body = kwargs["body"]
        if body.get("mimeType") == FOLDER_MIME_TYPE:
            def create_folder():
                with self.lock:
                    folder_id = f"folder-{self.next_id}"
                    self.next_id += 1
                    key = (body["parents"][0], body["name"])
                    self.folders[key] = folder_id
                    self.folder_creates.append(key)
                return {"id": folder_id}

            return CallbackRequest(create_folder)

        def upload_file():
            # Both uploads must reach the API concurrently, proving the folder
            # coordination lock was released before media upload.
            self.upload_barrier.wait(timeout=3)
            with self.lock:
                self.file_creates.append(body)
                file_id = f"file-{self.next_id}"
                self.next_id += 1
            return {"id": file_id, "webViewLink": "fake-link"}

        return CallbackRequest(upload_file)


class ConcurrentFakeDrive:
    def __init__(self, upload_barrier):
        self.files_resource = ConcurrentFakeFiles(upload_barrier)

    def files(self):
        return self.files_resource


def test_concurrent_uploads_create_one_year_month_and_do_not_lock_media(safe_tmp_path):
    first = safe_tmp_path / "first.pdf"
    second = safe_tmp_path / "second.pdf"
    first.write_bytes(b"%PDF-1.4\nfirst")
    second.write_bytes(b"%PDF-1.4\nsecond")
    upload_barrier = threading.Barrier(2)
    drive = ConcurrentFakeDrive(upload_barrier)
    lock_path = safe_tmp_path / "drive-folders.lock"

    def upload(path):
        uploader = GoogleDriveUploader(
            drive,
            parent_folder_id="configured-parent",
            folder_lock_path=lock_path,
            media_factory=lambda item: ("fake-media", item.name),
        )
        return uploader.upload(path, report_date=datetime(2026, 9, 1))

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(upload, (first, second)))

    assert len(results) == 2
    assert drive.files_resource.folder_creates.count(("configured-parent", "2026")) == 1
    year_id = drive.files_resource.folders[("configured-parent", "2026")]
    assert drive.files_resource.folder_creates.count((year_id, "09-September")) == 1
    assert len(drive.files_resource.file_creates) == 2
