"""
Тест: создание папки 2025/09-September в Google Drive
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from oauth_google_drive import setup_oauth_google_drive, create_monthly_folder_structure

if __name__ == "__main__":
    service = setup_oauth_google_drive()
    base_folder_id = "1TI-P8ZGj0IOjw97OmEpjyVc7jAW_hsy2"  # PsychTest Reports
    year = 2025
    month = 9
    folder_id = create_monthly_folder_structure(service, year, month, base_folder_id=base_folder_id)
    print(f"Результат создания папки 2025/09: {folder_id}")
