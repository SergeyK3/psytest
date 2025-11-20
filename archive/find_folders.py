#!/usr/bin/env python3
"""Поиск всех доступных папок PsychTest"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        print("Ищем все папки с 'PsychTest' в названии...")
        
        # Поиск папок с PsychTest в названии
        query = "mimeType='application/vnd.google-apps.folder' and name contains 'PsychTest'"
        results = service.files().list(q=query, fields="files(id, name, parents)", pageSize=20).execute()
        folders = results.get('files', [])
        
        if not folders:
            print("Папки с 'PsychTest' не найдены.")
            
            # Попробуем найти все папки вообще
            print("\nПоказываем все доступные папки:")
            query = "mimeType='application/vnd.google-apps.folder'"
            results = service.files().list(q=query, fields="files(id, name)", pageSize=50).execute()
            all_folders = results.get('files', [])
            
            for folder in all_folders:
                print(f"  - {folder['name']} (ID: {folder['id']})")
        else:
            print(f"Найдено папок: {len(folders)}")
            for folder in folders:
                print(f"  📁 {folder['name']}")
                print(f"     ID: {folder['id']}")
                print(f"     Родители: {folder.get('parents', 'Нет')}")
                print()
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()