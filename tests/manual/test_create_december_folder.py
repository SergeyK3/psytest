import sys
import os
import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from oauth_google_drive import setup_oauth_google_drive, upload_to_google_drive_oauth

def test_create_specific_month_folder():
    service = setup_oauth_google_drive()
    year = 2025
    month = 12  # Декабрь
    base_folder_id = "1TI-P8ZGj0IOjw97OmEpjyVc7jAW_hsy2"  # Ваш ID папки PsychTest Reports
    base_folder_name = "PsychTest Reports"

    # Просто создаём папку, не загружая файл (используем фиктивный путь)
    fake_file_path = __file__  # Любой существующий файл, загрузка не важна
    result = upload_to_google_drive_oauth(
        file_path=fake_file_path,
        folder_name=base_folder_name,
        folder_id=base_folder_id,
        use_monthly_structure=True,
        year=year,
        month=month
    )
    print(f"Результат создания папки {year}/{month:02d}: {result}")

if __name__ == "__main__":
    test_create_specific_month_folder()
