#!/usr/bin/env python3
"""Находим ID папки PsychTest Reports old"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        print("Ищем папку 'PsychTest Reports old'...")
        
        # Поиск папки PsychTest Reports old
        query = "mimeType='application/vnd.google-apps.folder' and name='PsychTest Reports old'"
        results = service.files().list(q=query, fields="files(id, name, parents, webViewLink)").execute()
        folders = results.get('files', [])
        
        if folders:
            folder = folders[0]
            print(f"✅ Найдена папка: {folder.get('name')}")
            print(f"🆔 ID: {folder.get('id')}")
            print(f"🔗 Ссылка: {folder.get('webViewLink')}")
            
            # Проверяем родительскую папку
            parent_id = folder.get('parents', [])[0] if folder.get('parents') else None
            if parent_id:
                parent = service.files().get(fileId=parent_id, fields="id,name").execute()
                print(f"📂 Родительская папка: {parent.get('name')}")
            
            # Проверяем содержимое
            query = f"'{folder['id']}' in parents"
            results = service.files().list(q=query, fields="files(id, name, mimeType)", orderBy="name").execute()
            files = results.get('files', [])
            
            print(f"\n📊 Содержимое ({len(files)} элементов):")
            for file in files[:10]:  # Показываем первые 10
                icon = "📁" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
                print(f"  {icon} {file['name']}")
            
            return folder.get('id')
            
        else:
            print("❌ Папка 'PsychTest Reports old' не найдена")
            
            # Покажем все папки с PsychTest в названии
            query = "mimeType='application/vnd.google-apps.folder' and name contains 'PsychTest'"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            all_folders = results.get('files', [])
            
            print("\nВсе папки с 'PsychTest':")
            for folder in all_folders:
                print(f"  📁 {folder['name']} (ID: {folder['id']})")
                
            return None
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    folder_id = main()
    if folder_id:
        print(f"\n🎯 ID вашей рабочей папки: {folder_id}")
        print("Обновляю код для использования этой папки...")
    else:
        print("\n❌ Не удалось найти папку")