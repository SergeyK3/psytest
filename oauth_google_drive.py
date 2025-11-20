"""
Альтернативная реализация Google Drive интеграции с OAuth
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

def setup_oauth_google_drive():
    """Настраивает OAuth аутентификацию для Google Drive"""
    
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        
        creds = None
        token_file = 'token.json'
        credentials_file = 'oauth_credentials.json'
        
        # Загружаем существующие токены
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        
        # Если нет валидных токенов, запускаем OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(credentials_file):
                    print(f"❌ Файл {credentials_file} не найден!")
                    print("📖 Создайте OAuth credentials в Google Cloud Console")
                    return None
                    
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Сохраняем токены для будущего использования
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        service = build('drive', 'v3', credentials=creds)
        print("✅ OAuth Google Drive API инициализирован")
        return service
        
    except Exception as e:
        print(f"❌ Ошибка инициализации OAuth: {e}")
        return None

def create_monthly_folder_structure(service, year: int, month: int, base_folder_id: str = None, base_folder_name: str = "PsychTest Reports") -> Optional[str]:
    """Создает структуру папок: базовая_папка / 2025 / 10-October
    
    Args:
        service: Google Drive API service
        year: Год (например, 2025)
        month: Месяц (1-12)
        base_folder_id: ID базовой папки (если указан, используется вместо поиска по имени)
        base_folder_name: Название базовой папки (используется если base_folder_id не указан)
    
    Returns:
        folder_id месячной папки или None при ошибке
    """
    try:
        # Названия месяцев на английском
        month_names = {
            1: "01-January", 2: "02-February", 3: "03-March", 4: "04-April",
            5: "05-May", 6: "06-June", 7: "07-July", 8: "08-August", 
            9: "09-September", 10: "10-October", 11: "11-November", 12: "12-December"
        }
        
        # 1. Определяем базовую папку
        if base_folder_id:
            # Используем переданный ID
            print(f"📁 Используется базовая папка с ID: {base_folder_id}")
        else:
            # Ищем папку по имени (старая логика)
            query = f"name='{base_folder_name}' and mimeType='application/vnd.google-apps.folder'"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            folders = results.get('files', [])
            
            if not folders:
                print(f"❌ Папка '{base_folder_name}' не найдена")
                return None
            
            base_folder_id = folders[0]['id']
            print(f"📁 Найдена папка {base_folder_name}: {base_folder_id}")
        
        # 2. Ищем или создаем папку года в базовой папке
        year_str = str(year)
        query = f"name='{year_str}' and mimeType='application/vnd.google-apps.folder' and '{base_folder_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get('files', [])
        
        print(f"🔍 Поиск папки года '{year_str}' в базовой папке")
        print(f"🔍 Найдено папок с именем '{year_str}': {len(folders)}")
        
        if folders:
            year_folder_id = folders[0]['id']
            print(f"📁 ✅ Найдена существующая папка года: {year_str} (ID: {year_folder_id})")
        else:
            # Создаем папку года
            folder_metadata = {
                'name': year_str,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [base_folder_id]
            }
            folder = service.files().create(body=folder_metadata).execute()
            year_folder_id = folder.get('id')
            print(f"📁 ➕ Создана новая папка года: {year_str} (ID: {year_folder_id})")
        
        # 3. Ищем или создаем папку месяца внутри папки года
        month_folder_name = month_names[month]
        query = f"name='{month_folder_name}' and mimeType='application/vnd.google-apps.folder' and '{year_folder_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get('files', [])
        
        print(f"🔍 Поиск папки месяца '{month_folder_name}' в папке года")
        print(f"🔍 Найдено папок с именем '{month_folder_name}': {len(folders)}")
        
        if folders:
            month_folder_id = folders[0]['id']
            print(f"📁 ✅ Найдена существующая папка месяца: {month_folder_name} (ID: {month_folder_id})")
        else:
            # Создаем папку месяца
            folder_metadata = {
                'name': month_folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [year_folder_id]
            }
            folder = service.files().create(body=folder_metadata).execute()
            month_folder_id = folder.get('id')
            print(f"📁 ➕ Создана новая папка месяца: {month_folder_name} (ID: {month_folder_id})")
        
        return month_folder_id
        
    except Exception as e:
        print(f"❌ Ошибка создания структуры папок: {e}")
        return None

def upload_to_google_drive_oauth(file_path: str, folder_name: str = "PsychTest Reports", folder_id: str = "1Z77eo09GmcLuhsDGlb17E86vfb2p3jEM", use_monthly_structure: bool = False) -> Optional[str]:
    """Загружает файл в Google Drive используя OAuth
    
    Args:
        file_path: Путь к файлу для загрузки
        folder_name: Название базовой папки (используется если folder_id не указан)
        folder_id: Конкретный ID базовой папки Google Drive (внутри создается структура год/месяц)
        use_monthly_structure: Использовать ли месячную структуру папок (год/месяц)
    """
    
    service = setup_oauth_google_drive()
    if not service:
        return None
    
    try:
        from googleapiclient.http import MediaFileUpload
        from googleapiclient.errors import HttpError
        import datetime
        
        # Если указан конкретный ID папки и нужна месячная структура
        if folder_id and use_monthly_structure:
            # Создаем месячную структуру внутри указанной папки
            now = datetime.datetime.now()
            monthly_folder_id = create_monthly_folder_structure(service, now.year, now.month, folder_id, folder_name)
            if monthly_folder_id:
                folder_id = monthly_folder_id
            else:
                print("❌ Не удалось создать месячную структуру, используем базовую папку")
                print(f"📁 Используется базовая папка с ID: {folder_id}")
        elif folder_id:
            print(f"📁 Используется указанная папка с ID: {folder_id}")
        elif use_monthly_structure:
            # Используем месячную структуру папок
            now = datetime.datetime.now()
            folder_id = create_monthly_folder_structure(service, now.year, now.month, folder_id, folder_name)
            if not folder_id:
                print("❌ Не удалось создать месячную структуру папок")
                return None
        else:
            # Ищем или создаем папку по имени (старая логика)
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            folders = results.get('files', [])
            
            if folders:
                folder_id = folders[0]['id']
                print(f"📁 Найдена папка: {folder_name}")
            else:
                # Создаем папку
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = service.files().create(body=folder_metadata).execute()
                folder_id = folder.get('id')
                print(f"📁 Создана папка: {folder_name}")
        
        # Загружаем файл
        file_name = os.path.basename(file_path)
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        
        media = MediaFileUpload(file_path, mimetype='application/pdf')
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink'
        ).execute()
        
        file_id = file.get('id')
        web_link = file.get('webViewLink')
        
        print(f"📤 Файл загружен: {file_name}")
        print(f"🔗 Ссылка: {web_link}")
        
        return web_link
        
    except HttpError as e:
        print(f"❌ Ошибка загрузки: {e}")
        return None
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        return None

if __name__ == "__main__":
    # Тест OAuth интеграции
    print("🧪 Тестирование OAuth интеграции...")
    
    # Создаем тестовый файл
    test_file = "test_oauth.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("Тестовый файл для OAuth Google Drive интеграции")
    
    # Загружаем в Google Drive
    link = upload_to_google_drive_oauth(test_file)
    
    if link:
        print(f"🎉 Успех! Файл доступен по ссылке: {link}")
        os.remove(test_file)  # Удаляем тестовый файл
    else:
        print("❌ Ошибка загрузки")