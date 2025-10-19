#!/usr/bin/env python3
"""
Диагностический скрипт для проверки структуры Google Drive папок
"""

from oauth_google_drive import setup_oauth_google_drive

def list_folder_contents(service, folder_id, folder_name=""):
    """Показывает содержимое папки"""
    try:
        print(f"\n📁 Содержимое папки '{folder_name}' (ID: {folder_id}):")
        print("-" * 60)
        
        query = f"'{folder_id}' in parents"
        results = service.files().list(
            q=query, 
            fields="files(id, name, mimeType, parents, createdTime, modifiedTime)",
            orderBy="modifiedTime desc"
        ).execute()
        
        files = results.get('files', [])
        
        if not files:
            print("   📄 Папка пуста")
            return []
        
        for file in files:
            file_type = "📁" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
            modified = file.get('modifiedTime', 'Unknown')[:19]
            print(f"   {file_type} {file['name']}")
            print(f"      ID: {file['id']}")
            print(f"      Изменен: {modified}")
            print()
        
        return files
        
    except Exception as e:
        print(f"❌ Ошибка получения содержимого папки: {e}")
        return []

def diagnose_folder_structure():
    """Диагностирует структуру папок Google Drive"""
    print("🔍 ДИАГНОСТИКА СТРУКТУРЫ GOOGLE DRIVE")
    print("=" * 60)
    
    service = setup_oauth_google_drive()
    if not service:
        print("❌ Не удалось подключиться к Google Drive")
        return
    
    try:
        # 1. Ищем папку MyAiProjects
        print("\n🔍 Поиск папки MyAiProjects...")
        query = "name='MyAiProjects' and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(q=query, fields="files(id, name, parents)").execute()
        folders = results.get('files', [])
        
        if not folders:
            print("❌ Папка MyAiProjects не найдена")
            return
        
        main_folder = folders[0]
        print(f"✅ Найдена MyAiProjects: {main_folder['id']}")
        
        # 2. Показываем содержимое MyAiProjects
        main_contents = list_folder_contents(service, main_folder['id'], "MyAiProjects")
        
        # 3. Ищем папку PsychTest Reports
        psychtest_folder = None
        for item in main_contents:
            if item['name'] == 'PsychTest Reports' and item['mimeType'] == 'application/vnd.google-apps.folder':
                psychtest_folder = item
                break
        
        if not psychtest_folder:
            print("❌ Папка PsychTest Reports не найдена в MyAiProjects")
            return
        
        print(f"✅ Найдена PsychTest Reports: {psychtest_folder['id']}")
        
        # 4. Показываем содержимое PsychTest Reports
        psychtest_contents = list_folder_contents(service, psychtest_folder['id'], "PsychTest Reports")
        
        # 5. Ищем папку 2025
        year_folder = None
        for item in psychtest_contents:
            if item['name'] == '2025' and item['mimeType'] == 'application/vnd.google-apps.folder':
                year_folder = item
                break
        
        if not year_folder:
            print("❌ Папка 2025 не найдена в PsychTest Reports")
            return
        
        print(f"✅ Найдена папка 2025: {year_folder['id']}")
        
        # 6. Показываем содержимое папки 2025
        year_contents = list_folder_contents(service, year_folder['id'], "2025")
        
        # 7. Ищем папку 10-October
        month_folder = None
        for item in year_contents:
            if item['name'] == '10-October' and item['mimeType'] == 'application/vnd.google-apps.folder':
                month_folder = item
                break
        
        if not month_folder:
            print("❌ Папка 10-October не найдена в 2025")
            return
        
        print(f"✅ Найдена папка 10-October: {month_folder['id']}")
        
        # 8. Показываем содержимое папки 10-October (здесь должны быть отчеты)
        month_contents = list_folder_contents(service, month_folder['id'], "10-October")
        
        # 9. Проверяем недавние файлы в корне Google Drive
        print("\n🔍 Недавние файлы в Google Drive (последние 10):")
        print("-" * 60)
        
        recent_results = service.files().list(
            fields="files(id, name, parents, createdTime, mimeType)",
            orderBy="createdTime desc",
            pageSize=10
        ).execute()
        
        recent_files = recent_results.get('files', [])
        for file in recent_files:
            if 'pdf' in file['name'].lower():
                parents = file.get('parents', ['Нет родителя'])
                created = file.get('createdTime', 'Unknown')[:19]
                print(f"   📄 {file['name']}")
                print(f"      ID: {file['id']}")
                print(f"      Создан: {created}")
                print(f"      Родители: {parents}")
                print()
        
        print("\n" + "=" * 60)
        print("🎯 РЕКОМЕНДАЦИИ:")
        print("1. Проверьте папку 10-October - там должны быть отчеты")
        print("2. Если отчеты не в нужной папке, проверьте 'Недавние файлы'")
        print("3. Возможно, файлы загружаются в корень или другую папку")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Ошибка диагностики: {e}")

if __name__ == "__main__":
    diagnose_folder_structure()