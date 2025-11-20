#!/usr/bin/env python3
"""Проверяем и исправляем названия папок"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        # Наша новая папка (должна называться "PsychTest Reports")
        new_folder_id = "1wvj36SIIUlDZAur3bJYzFcGSZCVY7n7D"
        
        # Старая папка (должна называться "PsychTest Reports old")  
        old_folder_id = "1usUktKpJROojo3rT_Goi3AmNhnMRCFyh"
        
        print("Текущие названия папок:")
        
        # Проверяем новую папку
        new_folder = service.files().get(fileId=new_folder_id, fields="id,name").execute()
        print(f"📁 Новая: '{new_folder.get('name')}' (ID: {new_folder_id})")
        
        # Проверяем старую папку
        old_folder = service.files().get(fileId=old_folder_id, fields="id,name").execute()
        print(f"📁 Старая: '{old_folder.get('name')}' (ID: {old_folder_id})")
        
        # Если старая папка не переименована, переименовываем ее
        if old_folder.get('name') == 'PsychTest Reports':
            print(f"\n🔄 Переименовываем старую папку в 'PsychTest Reports old'...")
            body = {'name': 'PsychTest Reports old'}
            updated = service.files().update(fileId=old_folder_id, body=body).execute()
            print(f"✅ Переименовано: '{updated.get('name')}'")
        
        # Убеждаемся что новая папка правильно называется
        if new_folder.get('name') != 'PsychTest Reports':
            print(f"\n🔄 Исправляем название новой папки...")
            body = {'name': 'PsychTest Reports'}
            updated = service.files().update(fileId=new_folder_id, body=body).execute()
            print(f"✅ Исправлено: '{updated.get('name')}'")
        
        print(f"\n✅ Итоговое состояние:")
        print(f"📁 Рабочая папка: PsychTest Reports (ID: {new_folder_id})")
        print(f"📁 Архивная папка: PsychTest Reports old (ID: {old_folder_id})")
        
        # Показываем итоговое содержимое MyAiProjects
        print(f"\nСодержимое MyAiProjects:")
        query = f"'1cL2MLXpREmwE4k-MJRAuWg_G8SyVizg7' in parents and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(q=query, fields="files(id, name)", orderBy="name").execute()
        folders = results.get('files', [])
        
        for folder in folders:
            print(f"  📁 {folder['name']} (ID: {folder['id']})")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()