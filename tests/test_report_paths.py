import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from telegram_test_bot import build_unique_report_paths, display_report_filename


def test_same_name_same_instant_uses_user_id_microseconds_and_uuid(safe_tmp_path):
    instant = datetime(2026, 9, 1, 12, 30, 45, 123456, tzinfo=timezone.utc)
    start = threading.Barrier(2)

    def finish(user_id):
        start.wait()
        return build_unique_report_paths(
            user_id,
            "Одинаковое Имя",
            safe_tmp_path,
            now_utc=instant,
        )

    with ThreadPoolExecutor(max_workers=2) as pool:
        (first_user, first_full), (second_user, second_full) = pool.map(
            finish, (1001, 1002)
        )

    for path in (first_user, first_full, second_user, second_full):
        path.write_bytes(b"%PDF-1.4\n")
        assert path.parent == safe_tmp_path
        assert "2026-09-01_12-30-45.123456Z" in path.name

    assert len({first_user, first_full, second_user, second_full}) == 4
    assert "tg-1001" in first_user.name
    assert "tg-1002" in second_user.name


def test_user_filename_parts_cannot_escape_work_directory(safe_tmp_path):
    user_pdf, full_pdf = build_unique_report_paths(
        42,
        "../../секрет\\чужой/report",
        safe_tmp_path,
    )

    assert user_pdf.parent == safe_tmp_path
    assert full_pdf.parent == safe_tmp_path
    assert "/" not in user_pdf.name
    assert "\\" not in user_pdf.name
    assert display_report_filename("../../Имя\\Файл").startswith("Отчет_")
