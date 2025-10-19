#!/usr/bin/env python3
"""
Тестовый скрипт для проверки Google Drive OAuth интеграции
"""

import os
from oauth_google_drive import setup_oauth_google_drive, create_monthly_folder_structure

def test_google_drive_connection():
    """Тестируем подключение к Google Drive"""
    print("🔍 Тестирование подключения к Google Drive...")
    
    service = setup_oauth_google_drive()
    if not service:
        print("❌ Не удалось подключиться к Google Drive")
        return False
    
    print("✅ Подключение к Google Drive успешно")
    return service

def test_folder_search(service):
    """Тестируем поиск папок"""
    print("\n🔍 Поиск папки MyAiProjects...")
    
    try:
        # Поиск папки MyAiProjects
        query = "name='MyAiProjects' and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(q=query, fields="files(id, name, parents)").execute()
        folders = results.get('files', [])
        
        if folders:
            folder = folders[0]
            print(f"✅ Папка MyAiProjects найдена:")
            print(f"   ID: {folder['id']}")
            print(f"   Имя: {folder['name']}")
            print(f"   Родители: {folder.get('parents', 'Корень')}")
            return folder['id']
        else:
            print("❌ Папка MyAiProjects не найдена")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка поиска папки: {e}")
        return None

def test_monthly_structure(service):
    """Тестируем создание месячной структуры"""
    print("\n🔍 Тестирование создания месячной структуры...")
    
    try:
        folder_id = create_monthly_folder_structure(service, 2025, 10, "PsychTest Reports")
        
        if folder_id:
            print(f"✅ Месячная структура создана успешно")
            print(f"   ID папки октября: {folder_id}")
            return folder_id
        else:
            print("❌ Не удалось создать месячную структуру")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка создания структуры: {e}")
        return None

def test_file_upload(service, folder_id):
    """Тестируем загрузку файла"""
    print(f"\n🔍 Тестирование загрузки файла в папку {folder_id}...")
    
    # Создаем тестовый файл
    test_filename = "test_google_drive.txt"
    test_content = f"""Тестовый файл для проверки Google Drive интеграции
Время создания: {os.popen('date /t & time /t').read()}
Папка назначения: {folder_id}
"""
    
    try:
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        from googleapiclient.http import MediaFileUpload
        
        # Метаданные файла
        file_metadata = {
            'name': test_filename,
            'parents': [folder_id]
        }
        
        # Загрузка файла
        media = MediaFileUpload(test_filename, mimetype='text/plain')
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink'
        ).execute()
        
        # Удаляем локальный тестовый файл
        os.remove(test_filename)
        
        file_id = file.get('id')
        web_link = file.get('webViewLink')
        
        print(f"✅ Файл загружен успешно:")
        print(f"   ID файла: {file_id}")
        print(f"   Ссылка: {web_link}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка загрузки файла: {e}")
        if os.path.exists(test_filename):
            os.remove(test_filename)
        return False

def main():
    """Основная функция тестирования"""
    print("=" * 60)
    print("           ТЕСТИРОВАНИЕ GOOGLE DRIVE ИНТЕГРАЦИИ")
    print("=" * 60)
    
    # 1. Тестируем подключение
    service = test_google_drive_connection()
    if not service:
        return
    
    # 2. Тестируем поиск папок
    main_folder_id = test_folder_search(service)
    
    # 3. Тестируем создание структуры
    month_folder_id = test_monthly_structure(service)
    
    # 4. Тестируем загрузку файла
    if month_folder_id:
        success = test_file_upload(service, month_folder_id)
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
            print("   Отчеты должны корректно загружаться в Google Drive")
        else:
            print("❌ ТЕСТЫ НЕ ПРОЙДЕНЫ")
            print("   Необходимо исправить проблемы с загрузкой")
        print("=" * 60)
    
if __name__ == "__main__":
    main()