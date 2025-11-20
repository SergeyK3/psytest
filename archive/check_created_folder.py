#!/usr/bin/env python3
"""Проверка созданной папки PsychTest Reports"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        # Проверяем созданную папку по ID
        created_folder_id = "1wvj36SIIUlDZAur3bJYzFcGSZCVY7n7D"
        print(f"Проверяем созданную папку: {created_folder_id}")
        
        try:
            folder = service.files().get(fileId=created_folder_id, fields="id,name,parents").execute()
            print(f"✅ Папка существует:")
            print(f"   ID: {folder.get('id')}")
            print(f"   Название: {folder.get('name')}")
            print(f"   Родители: {folder.get('parents')}")
            
            # Проверяем родительскую папку
            parent_id = folder.get('parents', [])[0] if folder.get('parents') else None
            if parent_id:
                parent = service.files().get(fileId=parent_id, fields="id,name").execute()
                print(f"   Родительская папка: {parent.get('name')} (ID: {parent_id})")
            
        except Exception as e:
            print(f"❌ Папка не найдена: {e}")
        
        # Проверяем содержимое MyAiProjects
        myai_folder_id = "1cL2MLXpREmwE4k-MJRAuWg_G8SyVizg7"
        print(f"\nСодержимое папки MyAiProjects ({myai_folder_id}):")
        
        query = f"'{myai_folder_id}' in parents"
        results = service.files().list(q=query, fields="files(id, name, mimeType)", pageSize=20).execute()
        files = results.get('files', [])
        
        print(f"Найдено элементов: {len(files)}")
        for file in files:
            icon = "📁" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
            print(f"  {icon} {file['name']} (ID: {file['id']})")
        
        # Поищем все папки PsychTest Reports
        print(f"\nПоиск всех папок 'PsychTest Reports':")
        query = "mimeType='application/vnd.google-apps.folder' and name='PsychTest Reports'"
        results = service.files().list(q=query, fields="files(id, name, parents)").execute()
        folders = results.get('files', [])
        
        for folder in folders:
            print(f"📁 PsychTest Reports (ID: {folder['id']})")
            print(f"   Родители: {folder.get('parents', 'Корень')}")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()