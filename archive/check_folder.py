#!/usr/bin/env python3
"""Быстрая проверка доступа к папке Google Drive"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        folder_id = "1TI-P8ZGj0IOjw97OmEpjyVc7jAW_hsy2"
        print(f"Проверяем папку: {folder_id}")
        
        # Получаем информацию о папке
        folder = service.files().get(fileId=folder_id, fields="id,name,parents").execute()
        print(f"Папка найдена: '{folder.get('name')}'")
        print(f"ID: {folder.get('id')}")
        
        # Проверяем содержимое
        query = f"'{folder_id}' in parents"
        results = service.files().list(q=query, fields="files(id, name, mimeType)", pageSize=10).execute()
        files = results.get('files', [])
        
        print(f"Содержимое папки ({len(files)} элементов):")
        for file in files:
            print(f"  - {file['name']} ({file['mimeType']})")
        
        print("SUCCESS: Доступ к папке есть!")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    main()