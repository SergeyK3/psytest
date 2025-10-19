#!/usr/bin/env python3
"""Ищем куда реально загрузился файл"""

from oauth_google_drive import setup_oauth_google_drive
from datetime import datetime

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        print("🔍 Ищем файлы с TEST в названии за последние 10 минут...")
        
        # Поиск всех файлов с TEST в названии
        query = "name contains 'TEST' and mimeType='application/pdf'"
        results = service.files().list(q=query, fields="files(id, name, parents, createdTime, webViewLink)", orderBy="createdTime desc", pageSize=10).execute()
        files = results.get('files', [])
        
        if files:
            print(f"Найдено {len(files)} тестовых файлов:")
            for file in files:
                print(f"\n📄 {file['name']}")
                print(f"   ID: {file['id']}")
                print(f"   Создан: {file.get('createdTime', 'Неизвестно')}")
                print(f"   Ссылка: {file.get('webViewLink', 'Нет')}")
                
                # Найдем родительскую папку
                parent_ids = file.get('parents', [])
                if parent_ids:
                    parent_id = parent_ids[0]
                    try:
                        parent = service.files().get(fileId=parent_id, fields="id,name,parents").execute()
                        print(f"   📁 Родительская папка: {parent.get('name')} (ID: {parent_id})")
                        
                        # Найдем папку уровнем выше
                        grandparent_ids = parent.get('parents', [])
                        if grandparent_ids:
                            grandparent_id = grandparent_ids[0]
                            grandparent = service.files().get(fileId=grandparent_id, fields="id,name").execute()
                            print(f"   📂 Выше: {grandparent.get('name')} (ID: {grandparent_id})")
                    except Exception as e:
                        print(f"   ❌ Не удалось получить родительскую папку: {e}")
        else:
            print("❌ Тестовые файлы не найдены")
            
        # Поищем все папки PsychTest
        print(f"\n🔍 Все доступные папки с 'PsychTest':")
        query = "mimeType='application/vnd.google-apps.folder' and name contains 'PsychTest'"
        results = service.files().list(q=query, fields="files(id, name, webViewLink)").execute()
        folders = results.get('files', [])
        
        for folder in folders:
            print(f"📁 {folder['name']} (ID: {folder['id']})")
            print(f"   🔗 {folder.get('webViewLink', 'Нет ссылки')}")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()