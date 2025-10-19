#!/usr/bin/env python3
"""Проверяем где находятся наши тестовые файлы"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        # ID папки 2025 (куда мы загружаем)
        target_folder_id = "1BFT4qQHJjS--qAx0Y7-3nJgKjlVl3grb"
        
        print(f"🔍 Проверяем содержимое папки 2025: {target_folder_id}")
        
        # Получаем содержимое папки 2025
        query = f"'{target_folder_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name, createdTime, webViewLink)", orderBy="createdTime desc").execute()
        files = results.get('files', [])
        
        print(f"📊 Найдено файлов: {len(files)}")
        
        for file in files:
            created = file.get('createdTime', 'Неизвестно')
            print(f"📄 {file['name']}")
            print(f"   Создан: {created}")
            print(f"   🔗 {file.get('webViewLink')}")
            print()
        
        # Поищем последние тестовые файлы
        print(f"\n🔍 Поиск последних тестовых файлов...")
        query = "name contains 'TEST' and mimeType='application/pdf' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name, parents, createdTime, webViewLink)", orderBy="createdTime desc", pageSize=5).execute()
        test_files = results.get('files', [])
        
        print(f"📊 Последние 5 тестовых файлов:")
        for file in test_files:
            parents = file.get('parents', [])
            parent_info = "Неизвестно"
            if parents:
                parent_id = parents[0]
                try:
                    parent = service.files().get(fileId=parent_id, fields="name").execute()
                    parent_info = f"{parent.get('name')} (ID: {parent_id})"
                except:
                    parent_info = f"ID: {parent_id}"
            
            print(f"📄 {file['name']}")
            print(f"   📁 Папка: {parent_info}")
            print(f"   📅 Создан: {file.get('createdTime')}")
            print(f"   🔗 {file.get('webViewLink')}")
            print()
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()