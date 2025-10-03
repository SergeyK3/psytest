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

def upload_to_google_drive_oauth(file_path: str, folder_name: str = "PsychTest Reports") -> Optional[str]:
    """Загружает файл в Google Drive используя OAuth"""
    
    service = setup_oauth_google_drive()
    if not service:
        return None
    
    try:
        from googleapiclient.http import MediaFileUpload
        from googleapiclient.errors import HttpError
        
        # Ищем или создаем папку
        folder_id = None
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