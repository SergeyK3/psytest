#!/usr/bin/env python3
"""Проверяем и восстанавливаем папку из корзины"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        # ID папки 2025
        folder_id = "1BFT4qQHJjS--qAx0Y7-3nJgKjlVl3grb"
        
        print(f"🔍 Проверяем статус папки 2025: {folder_id}")
        
        # Проверяем папку
        try:
            folder = service.files().get(fileId=folder_id, fields="id,name,trashed,parents").execute()
            print(f"📁 Папка: {folder.get('name')}")
            print(f"🗑️ В корзине: {folder.get('trashed', False)}")
            print(f"📂 Родители: {folder.get('parents', [])}")
            
            if folder.get('trashed'):
                print(f"\n🔄 Восстанавливаем папку из корзины...")
                
                # Восстанавливаем папку
                restored = service.files().update(
                    fileId=folder_id,
                    body={'trashed': False}
                ).execute()
                
                print(f"✅ Папка восстановлена: {restored.get('name')}")
                
                # Проверяем содержимое после восстановления
                query = f"'{folder_id}' in parents and trashed=true"
                results = service.files().list(q=query, fields="files(id, name)").execute()
                trashed_files = results.get('files', [])
                
                if trashed_files:
                    print(f"\n🔄 Восстанавливаем файлы из корзины ({len(trashed_files)} шт.)...")
                    for file in trashed_files:
                        try:
                            service.files().update(
                                fileId=file['id'],
                                body={'trashed': False}
                            ).execute()
                            print(f"✅ Восстановлен: {file['name']}")
                        except Exception as e:
                            print(f"❌ Ошибка восстановления {file['name']}: {e}")
                else:
                    print(f"✅ Файлы в корзине не найдены")
            else:
                print(f"✅ Папка не в корзине")
                
        except Exception as e:
            print(f"❌ Ошибка проверки папки: {e}")
            return None
        
        # Проверяем итоговое состояние
        print(f"\n📊 Итоговое содержимое папки 2025:")
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name, createdTime)", orderBy="createdTime desc").execute()
        files = results.get('files', [])
        
        for file in files:
            print(f"📄 {file['name']} ({file.get('createdTime')})")
        
        return folder_id
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    main()