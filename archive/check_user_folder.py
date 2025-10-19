#!/usr/bin/env python3
"""
Проверка доступа к правильной папке пользователя
"""

from oauth_google_drive import setup_oauth_google_drive

def check_user_folder():
    """Проверяем доступ к папке пользователя"""
    
    service = setup_oauth_google_drive()
    if not service:
        print("❌ Не удалось подключиться к Google Drive")
        return
    
    folder_id = "1TI-P8ZGj0IOjw97OmEpjyVc7jAW_hsy2"
    
    try:
        # Пытаемся получить доступ к папке
        folder = service.files().get(fileId=folder_id, fields="id,name,parents").execute()
        print(f"✅ Папка найдена: {folder['name']} (ID: {folder['id']})")
        
        # Проверяем родительские папки
        if 'parents' in folder:
            for parent_id in folder['parents']:
                try:
                    parent = service.files().get(fileId=parent_id, fields="id,name").execute()
                    print(f"📁 Родительская папка: {parent['name']} (ID: {parent['id']})")
                except Exception as e:
                    print(f"⚠️ Родительская папка {parent_id} недоступна: {e}")
        else:
            print("📁 Папка находится в корне Drive")
        
        # Ищем существующие подпапки
        year_query = f"name='2025' and mimeType='application/vnd.google-apps.folder' and '{folder_id}' in parents"
        year_results = service.files().list(q=year_query, fields="files(id, name)").execute()
        year_folders = year_results.get('files', [])
        
        print(f"\n🔍 Папок '2025': {len(year_folders)}")
        
        if year_folders:
            year_id = year_folders[0]['id']
            print(f"📁 Папка 2025: {year_id}")
            
            # Ищем папку месяца
            month_query = f"name='10-October' and mimeType='application/vnd.google-apps.folder' and '{year_id}' in parents"
            month_results = service.files().list(q=month_query, fields="files(id, name)").execute()
            month_folders = month_results.get('files', [])
            
            print(f"📁 Папок '10-October': {len(month_folders)}")
            
            if month_folders:
                month_id = month_folders[0]['id']
                print(f"📁 Папка 10-October: {month_id}")
                
                # Ищем PDF файлы
                pdf_query = f"mimeType='application/pdf' and '{month_id}' in parents"
                pdf_results = service.files().list(q=pdf_query, fields="files(id, name, createdTime)", orderBy="createdTime desc").execute()
                pdf_files = pdf_results.get('files', [])
                
                print(f"\n📄 PDF файлов в папке месяца: {len(pdf_files)}")
                for pdf in pdf_files:
                    print(f"  • {pdf['name']} (создан: {pdf['createdTime']})")
        
        # Также проверим все файлы в базовой папке
        print(f"\n📄 Файлы в базовой папке {folder_id}:")
        base_query = f"'{folder_id}' in parents"
        base_results = service.files().list(q=base_query, fields="files(id, name, mimeType)", pageSize=10).execute()
        base_files = base_results.get('files', [])
        
        for file in base_files:
            file_type = "📁" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
            print(f"  {file_type} {file['name']}")
            
        print("\n✅ Тест доступа к папке завершен успешно")
        
    except Exception as e:
        print(f"❌ Ошибка доступа к папке: {e}")
        print("🔄 Возможные причины:")
        print("   1. Нужно обновить OAuth токены")
        print("   2. Папка находится в другом Google аккаунте")
        print("   3. Недостаточно прав доступа")
        
        # Попробуем удалить старые токены и пересоздать
        import os
        if os.path.exists('token.json'):
            print("🔄 Удаляю старые токены для повторной авторизации...")
            os.remove('token.json')
            print("✅ Перезапустите скрипт для новой авторизации")

if __name__ == "__main__":
    check_user_folder()