#!/usr/bin/env python3
"""
Поиск ВСЕХ папок PsychTest Reports и определение правильной
"""

from oauth_google_drive import setup_oauth_google_drive

def find_all_psychtest_folders():
    """Находим все папки PsychTest Reports и показываем их содержимое"""
    
    service = setup_oauth_google_drive()
    if not service:
        print("❌ Не удалось подключиться к Google Drive")
        return
    
    try:
        # Ищем ВСЕ папки с именем похожим на PsychTest
        queries = [
            "name contains 'PsychTest' and mimeType='application/vnd.google-apps.folder'",
            "name='PsychTest Reports' and mimeType='application/vnd.google-apps.folder'",
            "name contains 'Reports' and mimeType='application/vnd.google-apps.folder'"
        ]
        
        all_folders = []
        
        for query in queries:
            results = service.files().list(q=query, fields="files(id, name, parents, createdTime)").execute()
            folders = results.get('files', [])
            
            for folder in folders:
                if folder not in all_folders:
                    all_folders.append(folder)
        
        print(f"🔍 Найдено папок: {len(all_folders)}")
        
        for i, folder in enumerate(all_folders, 1):
            print(f"\n📁 Папка {i}: {folder['name']}")
            print(f"   ID: {folder['id']}")
            print(f"   Создана: {folder['createdTime']}")
            
            # Получаем полный путь
            path = []
            try:
                if 'parents' in folder:
                    parent_id = folder['parents'][0]
                    while parent_id:
                        try:
                            parent = service.files().get(fileId=parent_id, fields="id,name,parents").execute()
                            path.insert(0, parent['name'])
                            parent_id = parent.get('parents', [None])[0] if parent.get('parents') else None
                        except:
                            break
                    print(f"   Путь: {' → '.join(path)} → {folder['name']}")
                else:
                    print("   Путь: (корень) → " + folder['name'])
            except Exception as e:
                print(f"   Путь: (не удалось определить) - {e}")
            
            # Проверяем содержимое папки
            folder_id = folder['id']
            
            # Ищем файлы и подпапки
            content_query = f"'{folder_id}' in parents"
            content_results = service.files().list(q=content_query, fields="files(id, name, mimeType, createdTime)", pageSize=20).execute()
            content_files = content_results.get('files', [])
            
            print(f"   📄 Содержимое ({len(content_files)} элементов):")
            
            recent_pdfs = []
            subfolders = []
            
            for file in content_files:
                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    subfolders.append(file)
                elif file['mimeType'] == 'application/pdf':
                    recent_pdfs.append(file)
            
            # Показываем подпапки
            for subfolder in subfolders[:5]:
                print(f"     📁 {subfolder['name']} (создана: {subfolder['createdTime']})")
            
            # Показываем последние PDF
            recent_pdfs.sort(key=lambda x: x['createdTime'], reverse=True)
            for pdf in recent_pdfs[:3]:
                print(f"     📄 {pdf['name']} (создан: {pdf['createdTime']})")
            
            if len(content_files) > 8:
                print(f"     ... и ещё {len(content_files) - 8} файлов")
        
        print(f"\n🎯 ВЫВОДЫ:")
        print(f"Найдено папок с отчетами: {len(all_folders)}")
        
        # Определяем самую активную папку
        most_recent = None
        most_recent_time = None
        
        for folder in all_folders:
            folder_id = folder['id']
            pdf_query = f"mimeType='application/pdf' and '{folder_id}' in parents"
            pdf_results = service.files().list(q=pdf_query, fields="files(createdTime)", orderBy="createdTime desc", pageSize=1).execute()
            pdf_files = pdf_results.get('files', [])
            
            if pdf_files:
                latest_pdf_time = pdf_files[0]['createdTime']
                if not most_recent_time or latest_pdf_time > most_recent_time:
                    most_recent_time = latest_pdf_time
                    most_recent = folder
        
        if most_recent:
            print(f"\n🏆 САМАЯ АКТИВНАЯ ПАПКА:")
            print(f"   📁 {most_recent['name']}")
            print(f"   🆔 ID: {most_recent['id']}")
            print(f"   📅 Последний файл: {most_recent_time}")
            print(f"\n💡 РЕКОМЕНДАЦИЯ: Используйте ID {most_recent['id']}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    find_all_psychtest_folders()