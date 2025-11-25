
import sys
import os
import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from oauth_google_drive import setup_oauth_google_drive, create_monthly_folder_structure

def test_create_november_folder():
    service = setup_oauth_google_drive()
    year = datetime.datetime.now().year
    month = 11  # Ноябрь
    base_folder_name = "PsychTest Reports"
    base_folder_id = "1TI-P8ZGj0IOjw97OmEpjyVc7jAW_hsy2"  # ID вашей папки PsychTest Reports

    folder = create_monthly_folder_structure(service, year, month, base_folder_id=base_folder_id, base_folder_name=base_folder_name)
    assert folder is not None, "Папка для ноября не создана"
    print(f"✅ Папка для ноября {year}/11-November успешно создана или найдена. ID: {folder}")

if __name__ == "__main__":
    test_create_november_folder()
