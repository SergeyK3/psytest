#!/usr/bin/env python3
"""Удаление дублированной папки PsychTest Reports"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        # ID старой папки, которую нужно удалить из MyAiProjects
        old_folder_id = "1usUktKpJROojo3rT_Goi3AmNhnMRCFyh"
        new_folder_id = "1wvj36SIIUlDZAur3bJYzFcGSZCVY7n7D"
        
        print(f"Проверяем содержимое старой папки: {old_folder_id}")
        
        # Проверяем содержимое старой папки
        query = f"'{old_folder_id}' in parents"
        results = service.files().list(q=query, fields="files(id, name)", pageSize=10).execute()
        files = results.get('files', [])
        
        print(f"В старой папке {len(files)} файлов:")
        for file in files:
            print(f"  - {file['name']}")
        
        if files:
            print("\n❌ В старой папке есть файлы! Не удаляем.")
            print("Переименуем старую папку в 'PsychTest Reports OLD'")
            
            # Переименовываем старую папку
            body = {'name': 'PsychTest Reports OLD'}
            updated_file = service.files().update(fileId=old_folder_id, body=body).execute()
            print(f"✅ Папка переименована: {updated_file.get('name')}")
            
        else:
            print("\n✅ Старая папка пустая, удаляем ее")
            service.files().delete(fileId=old_folder_id).execute()
            print("✅ Старая папка удалена")
        
        print(f"\n✅ Активная папка: PsychTest Reports (ID: {new_folder_id})")
        
        # Проверяем итоговое состояние
        query = f"'1cL2MLXpREmwE4k-MJRAuWg_G8SyVizg7' in parents and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get('files', [])
        
        print(f"\nПапки в MyAiProjects:")
        for folder in folders:
            print(f"  📁 {folder['name']} (ID: {folder['id']})")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()