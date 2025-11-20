#!/usr/bin/env python3
"""Поиск папки MyAiProjects"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        print("Ищем папку MyAiProjects...")
        
        # Поиск папки MyAiProjects
        query = "mimeType='application/vnd.google-apps.folder' and name='MyAiProjects'"
        results = service.files().list(q=query, fields="files(id, name, parents)").execute()
        folders = results.get('files', [])
        
        if folders:
            folder = folders[0]
            print(f"✅ Папка MyAiProjects найдена:")
            print(f"   ID: {folder['id']}")
            print(f"   Название: {folder['name']}")
            print(f"   Родители: {folder.get('parents', 'Корень диска')}")
            
            # Создаем новую папку PsychTest Reports внутри MyAiProjects
            print(f"\nСоздаю новую папку 'PsychTest Reports' внутри MyAiProjects...")
            
            folder_metadata = {
                'name': 'PsychTest Reports',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [folder['id']]
            }
            
            new_folder = service.files().create(body=folder_metadata).execute()
            new_folder_id = new_folder.get('id')
            
            print(f"✅ Создана новая папка:")
            print(f"   ID: {new_folder_id}")
            print(f"   Название: PsychTest Reports")
            print(f"   Путь: MyAiProjects/PsychTest Reports")
            
            return new_folder_id
            
        else:
            print("❌ Папка MyAiProjects не найдена")
            
            # Покажем все доступные папки
            query = "mimeType='application/vnd.google-apps.folder'"
            results = service.files().list(q=query, fields="files(id, name)", pageSize=20).execute()
            all_folders = results.get('files', [])
            
            print("\nДоступные папки:")
            for folder in all_folders:
                print(f"  - {folder['name']} (ID: {folder['id']})")
                
            return None
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    new_id = main()
    if new_id:
        print(f"\n🎉 Новая папка создана с ID: {new_id}")
        print("Теперь обновлю код для использования этой папки...")
    else:
        print("\n❌ Не удалось создать папку")