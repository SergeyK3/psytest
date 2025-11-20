#!/usr/bin/env python3
"""Получаем прямую ссылку на папку PsychTest Reports"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        # ID нашей новой папки
        folder_id = "1wvj36SIIUlDZAur3bJYzFcGSZCVY7n7D"
        
        # Получаем информацию о папке
        folder = service.files().get(fileId=folder_id, fields="id,name,parents,webViewLink").execute()
        
        print(f"📁 Папка: {folder.get('name')}")
        print(f"🆔 ID: {folder.get('id')}")
        print(f"🔗 Прямая ссылка: {folder.get('webViewLink')}")
        
        # Проверяем содержимое
        query = f"'{folder_id}' in parents"
        results = service.files().list(q=query, fields="files(id, name, mimeType)", orderBy="name").execute()
        files = results.get('files', [])
        
        print(f"\n📊 Содержимое папки ({len(files)} элементов):")
        for file in files:
            icon = "📁" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
            print(f"  {icon} {file['name']}")
        
        # Проверяем родительскую папку MyAiProjects
        parent_id = folder.get('parents', [])[0] if folder.get('parents') else None
        if parent_id:
            parent = service.files().get(fileId=parent_id, fields="id,name,webViewLink").execute()
            print(f"\n📂 Родительская папка: {parent.get('name')}")
            print(f"🔗 Ссылка на MyAiProjects: {parent.get('webViewLink')}")
        
        return folder.get('webViewLink')
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    link = main()
    if link:
        print(f"\n✅ Откройте эту прямую ссылку: {link}")
    else:
        print("\n❌ Не удалось получить ссылку")