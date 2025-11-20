#!/usr/bin/env python3
"""Находим правильную целевую папку"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        print("🔍 Ищем правильную папку для сохранения отчетов...")
        
        # Ищем файлы с именем Ким_Сергей (ваши отчеты)
        query = "name contains 'Ким_Сергей' and mimeType='application/pdf' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name, parents)", pageSize=10).execute()
        files = results.get('files', [])
        
        print(f"Найдено ваших отчетов: {len(files)}")
        
        # Собираем папки где находятся ваши отчеты
        parent_folders = set()
        for file in files:
            parents = file.get('parents', [])
            if parents:
                parent_folders.add(parents[0])
        
        print(f"\n📁 Папки с вашими отчетами:")
        for folder_id in parent_folders:
            try:
                folder = service.files().get(fileId=folder_id, fields="id,name,parents,webViewLink").execute()
                print(f"\n📁 {folder.get('name')} (ID: {folder_id})")
                print(f"   🔗 {folder.get('webViewLink')}")
                
                # Проверим родительскую папку
                parents = folder.get('parents', [])
                if parents:
                    try:
                        parent = service.files().get(fileId=parents[0], fields="name").execute()
                        print(f"   📂 Внутри: {parent.get('name')}")
                    except:
                        pass
                
                # Покажем последние файлы
                query = f"'{folder_id}' in parents and trashed=false"
                results = service.files().list(q=query, fields="files(name)", orderBy="name desc", pageSize=3).execute()
                contents = results.get('files', [])
                
                print(f"   📊 Последние файлы:")
                for item in contents:
                    print(f"      📄 {item['name']}")
                
            except Exception as e:
                print(f"❌ Ошибка получения папки {folder_id}: {e}")
        
        print(f"\n❓ Какую папку использовать для новых отчетов?")
        print(f"Скопируйте ID нужной папки и обновите код.")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()