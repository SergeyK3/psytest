#!/usr/bin/env python3
"""
Поиск правильной папки PsychTest Reports
"""

from oauth_google_drive import setup_oauth_google_drive

def find_correct_folder():
    """Ищем папку PsychTest Reports"""
    
    service = setup_oauth_google_drive()
    if not service:
        print("❌ Не удалось подключиться к Google Drive")
        return
    
    try:
        # Ищем все папки с именем "PsychTest Reports"
        query = "name='PsychTest Reports' and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(q=query, fields="files(id, name, parents)").execute()
        folders = results.get('files', [])
        
        print(f"🔍 Найдено папок 'PsychTest Reports': {len(folders)}")
        
        for i, folder in enumerate(folders):
            print(f"\n📁 Папка {i+1}: {folder['name']}")
            print(f"   ID: {folder['id']}")
            
            # Получаем информацию о родительских папках
            if 'parents' in folder:
                for parent_id in folder['parents']:
                    try:
                        parent = service.files().get(fileId=parent_id, fields="id,name").execute()
                        print(f"   Родительская папка: {parent['name']} (ID: {parent['id']})")
                    except Exception:
                        print(f"   Родительская папка: {parent_id} (недоступна)")
            else:
                print("   Находится в корне Drive")
            
            # Ищем файлы в папке
            pdf_query = f"mimeType='application/pdf' and '{folder['id']}' in parents"
            pdf_results = service.files().list(q=pdf_query, fields="files(id, name, createdTime)", orderBy="createdTime desc", pageSize=5).execute()
            pdf_files = pdf_results.get('files', [])
            
            print(f"   📄 Последние PDF файлы ({len(pdf_files)}):")
            for pdf in pdf_files[:3]:  # Показываем только первые 3
                print(f"     • {pdf['name']} (создан: {pdf['createdTime']})")
            
            # Ищем подпапки года
            year_query = f"name='2025' and mimeType='application/vnd.google-apps.folder' and '{folder['id']}' in parents"
            year_results = service.files().list(q=year_query, fields="files(id, name)").execute()
            year_folders = year_results.get('files', [])
            
            if year_folders:
                year_id = year_folders[0]['id']
                print(f"   📁 Найдена папка 2025: {year_id}")
                
                # Ищем папку месяца
                month_query = f"name='10-October' and mimeType='application/vnd.google-apps.folder' and '{year_id}' in parents"
                month_results = service.files().list(q=month_query, fields="files(id, name)").execute()
                month_folders = month_results.get('files', [])
                
                if month_folders:
                    month_id = month_folders[0]['id']
                    print(f"   📁 Найдена папка 10-October: {month_id}")
                    
                    # Ищем последние PDF файлы в папке месяца
                    month_pdf_query = f"mimeType='application/pdf' and '{month_id}' in parents"
                    month_pdf_results = service.files().list(q=month_pdf_query, fields="files(id, name, createdTime)", orderBy="createdTime desc", pageSize=5).execute()
                    month_pdf_files = month_pdf_results.get('files', [])
                    
                    print(f"   📄 PDF в папке 10-October ({len(month_pdf_files)}):")
                    for pdf in month_pdf_files:
                        print(f"     • {pdf['name']} (создан: {pdf['createdTime']})")
                        
        # Также поищем просто по 2025 папкам
        print(f"\n🔍 Поиск всех папок '2025':")
        year_query_all = "name='2025' and mimeType='application/vnd.google-apps.folder'"
        year_results_all = service.files().list(q=year_query_all, fields="files(id, name, parents)").execute()
        year_folders_all = year_results_all.get('files', [])
        
        for year_folder in year_folders_all:
            print(f"📁 Папка 2025: {year_folder['id']}")
            if 'parents' in year_folder:
                for parent_id in year_folder['parents']:
                    try:
                        parent = service.files().get(fileId=parent_id, fields="id,name").execute()
                        print(f"   Родитель: {parent['name']} (ID: {parent['id']})")
                    except Exception:
                        print(f"   Родитель: {parent_id} (недоступен)")
                        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    find_correct_folder()