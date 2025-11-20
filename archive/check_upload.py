#!/usr/bin/env python3
"""Проверяем последнюю загрузку в Google Drive"""

from oauth_google_drive import setup_oauth_google_drive
from datetime import datetime, timedelta

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        # ID вашей папки
        folder_id = "1TI-P8ZGj0IOjw97OmEpjyVc7jAW_hsy2"
        
        print(f"Проверяем папку: {folder_id}")
        
        # Проверяем саму папку
        try:
            folder = service.files().get(fileId=folder_id, fields="id,name").execute()
            print(f"✅ Папка доступна: {folder.get('name')}")
        except Exception as e:
            print(f"❌ Папка недоступна: {e}")
            return
        
        # Ищем папку October внутри 2025
        print("\n🔍 Поиск структуры папок...")
        
        # Сначала ищем папку 2025
        query = f"'{folder_id}' in parents and name='2025' and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        year_folders = results.get('files', [])
        
        if year_folders:
            year_folder_id = year_folders[0]['id']
            print(f"📁 Найдена папка 2025: {year_folder_id}")
            
            # Теперь ищем папку October
            query = f"'{year_folder_id}' in parents and name='10-October' and mimeType='application/vnd.google-apps.folder'"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            month_folders = results.get('files', [])
            
            if month_folders:
                month_folder_id = month_folders[0]['id']
                print(f"📁 Найдена папка 10-October: {month_folder_id}")
                
                # Ищем файлы в папке October
                query = f"'{month_folder_id}' in parents"
                results = service.files().list(q=query, fields="files(id, name, createdTime, webViewLink)", orderBy="createdTime desc").execute()
                files = results.get('files', [])
                
                print(f"\n📊 Файлы в папке 10-October ({len(files)} шт.):")
                for file in files:
                    created = file.get('createdTime', 'Неизвестно')
                    print(f"  📄 {file['name']}")
                    print(f"      Создан: {created}")
                    print(f"      ID: {file['id']}")
                    print(f"      Ссылка: {file.get('webViewLink', 'Нет ссылки')}")
                    print()
                
                # Проверяем последний тестовый файл
                test_files = [f for f in files if 'TEST' in f['name']]
                if test_files:
                    latest_test = test_files[0]
                    print(f"🎯 Последний тестовый файл: {latest_test['name']}")
                    print(f"🔗 Прямая ссылка: {latest_test.get('webViewLink')}")
                else:
                    print("❌ Тестовые файлы не найдены")
            else:
                print("❌ Папка 10-October не найдена")
        else:
            print("❌ Папка 2025 не найдена")
            
            # Покажем что есть в корне
            query = f"'{folder_id}' in parents"
            results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
            root_files = results.get('files', [])
            
            print(f"\nСодержимое корневой папки:")
            for file in root_files:
                icon = "📁" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
                print(f"  {icon} {file['name']} (ID: {file['id']})")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()