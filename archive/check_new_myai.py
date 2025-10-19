#!/usr/bin/env python3
"""Проверяем новую папку MyAiProjects"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        # ID новой папки MyAiProjects
        myai_folder_id = "1u9tVXdSMNRLbYwBu67eZkbovVMKxnmlj"
        
        print(f"Проверяем папку MyAiProjects: {myai_folder_id}")
        
        # Проверяем доступ к папке
        try:
            folder = service.files().get(fileId=myai_folder_id, fields="id,name").execute()
            print(f"✅ Папка доступна: {folder.get('name')}")
        except Exception as e:
            print(f"❌ Папка недоступна: {e}")
            return
        
        # Ищем содержимое папки MyAiProjects
        print(f"\nСодержимое папки MyAiProjects:")
        query = f"'{myai_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(q=query, fields="files(id, name, webViewLink)", orderBy="name").execute()
        folders = results.get('files', [])
        
        psychtest_old_id = None
        
        for folder in folders:
            print(f"📁 {folder['name']} (ID: {folder['id']})")
            print(f"   🔗 {folder.get('webViewLink')}")
            
            if folder['name'] == 'PsychTest Reports old':
                psychtest_old_id = folder['id']
                print(f"   ⭐ Это наша целевая папка!")
        
        if psychtest_old_id:
            print(f"\n🎯 ID папки 'PsychTest Reports old': {psychtest_old_id}")
            return psychtest_old_id
        else:
            print(f"\n❌ Папка 'PsychTest Reports old' не найдена в MyAiProjects")
            
            # Поищем все папки PsychTest в системе
            print(f"\nПоиск всех папок PsychTest:")
            query = "mimeType='application/vnd.google-apps.folder' and name contains 'PsychTest'"
            results = service.files().list(q=query, fields="files(id, name, parents)").execute()
            all_folders = results.get('files', [])
            
            for folder in all_folders:
                parents = folder.get('parents', [])
                if parents and parents[0] == myai_folder_id:
                    print(f"📁 {folder['name']} (ID: {folder['id']}) ✅ В MyAiProjects")
                else:
                    print(f"📁 {folder['name']} (ID: {folder['id']}) ❌ Не в MyAiProjects")
            
            return None
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    target_id = main()
    if target_id:
        print(f"\n✅ Обновляю код для использования папки: {target_id}")
    else:
        print(f"\n❌ Не удалось найти целевую папку")