#!/usr/bin/env python3
"""Найти ID папки 10-October"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        # ID папки 2025 из предыдущего вывода
        year_folder_id = "1BFT4qQHJjS--qAx0Y7-3nJgKjlVl3grb"
        
        print(f"🔍 Ищем папку '10-October' в папке 2025 ({year_folder_id})...")
        
        # Поиск папки 10-October внутри 2025
        query = f"name='10-October' and mimeType='application/vnd.google-apps.folder' and '{year_folder_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name, webViewLink)").execute()
        folders = results.get('files', [])
        
        if folders:
            folder = folders[0]
            print(f"✅ Найдена папка '10-October':")
            print(f"   ID: {folder['id']}")
            print(f"   🔗 {folder.get('webViewLink')}")
            
            # Проверим содержимое
            query = f"'{folder['id']}' in parents and trashed=false"
            results = service.files().list(q=query, fields="files(id, name)", orderBy="name").execute()
            contents = results.get('files', [])
            
            print(f"\n📊 Содержимое папки 10-October ({len(contents)} файлов):")
            for item in contents:
                print(f"  📄 {item['name']}")
            
            return folder['id']
        else:
            print("❌ Папка '10-October' не найдена")
            
            # Покажем что есть в папке 2025
            query = f"'{year_folder_id}' in parents and trashed=false"
            results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
            items = results.get('files', [])
            
            print(f"\nСодержимое папки 2025:")
            for item in items:
                icon = "📁" if item['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
                print(f"  {icon} {item['name']} (ID: {item['id']})")
            
            return None
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    october_id = main()
    if october_id:
        print(f"\n🎯 ID папки 10-October: {october_id}")
        print("Обновляю код для использования этой папки...")
    else:
        print("\n❌ Не удалось найти папку 10-October")