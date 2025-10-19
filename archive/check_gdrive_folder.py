#!/usr/bin/env python3
"""
Диагностика Google Drive папок - проверяем точную структуру
"""

from oauth_google_drive import setup_oauth_google_drive

def check_folder_structure():
    """Проверяем структуру папок и содержимое"""
    
    service = setup_oauth_google_drive()
    if not service:
        print("❌ Не удалось подключиться к Google Drive")
        return
    
    try:
        # Базовая папка
        base_folder_id = "1TI-P8ZGj0IOjw97OmEpjyVc7jAW_hsy2"
        print(f"🔍 Проверяем базовую папку: {base_folder_id}")
        
        # Получаем информацию о базовой папке
        base_folder = service.files().get(fileId=base_folder_id, fields="id,name").execute()
        print(f"📁 Базовая папка: {base_folder['name']} (ID: {base_folder['id']})")
        
        # Ищем папку 2025
        query = f"name='2025' and mimeType='application/vnd.google-apps.folder' and '{base_folder_id}' in parents"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        year_folders = results.get('files', [])
        
        print(f"🔍 Найдено папок '2025': {len(year_folders)}")
        for folder in year_folders:
            year_id = folder['id']
            print(f"📁 Папка 2025: {folder['name']} (ID: {year_id})")
            
            # Ищем папку месяца в каждой папке года
            month_query = f"name='10-October' and mimeType='application/vnd.google-apps.folder' and '{year_id}' in parents"
            month_results = service.files().list(q=month_query, fields="files(id, name)").execute()
            month_folders = month_results.get('files', [])
            
            print(f"  🔍 В папке {year_id} найдено папок '10-October': {len(month_folders)}")
            for month_folder in month_folders:
                month_id = month_folder['id']
                print(f"  📁 Папка 10-October: {month_folder['name']} (ID: {month_id})")
                
                # Ищем PDF файлы в папке месяца
                pdf_query = f"mimeType='application/pdf' and '{month_id}' in parents"
                pdf_results = service.files().list(q=pdf_query, fields="files(id, name, createdTime, modifiedTime)", orderBy="createdTime desc").execute()
                pdf_files = pdf_results.get('files', [])
                
                print(f"    📄 PDF файлов в папке: {len(pdf_files)}")
                for pdf in pdf_files:
                    print(f"    📄 {pdf['name']}")
                    print(f"       Создан: {pdf['createdTime']}")
                    print(f"       Изменен: {pdf['modifiedTime']}")
                    print(f"       ID: {pdf['id']}")
                    print()
        
        # Также проверим, нет ли файлов прямо в базовой папке
        print("\n🔍 Проверяем файлы прямо в базовой папке:")
        base_pdf_query = f"mimeType='application/pdf' and '{base_folder_id}' in parents"
        base_pdf_results = service.files().list(q=base_pdf_query, fields="files(id, name, createdTime)").execute()
        base_pdf_files = base_pdf_results.get('files', [])
        
        print(f"📄 PDF файлов в базовой папке: {len(base_pdf_files)}")
        for pdf in base_pdf_files:
            print(f"📄 {pdf['name']} (создан: {pdf['createdTime']})")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check_folder_structure()