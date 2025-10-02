#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Drive интеграция для корпоративных отчетов
"""

import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from typing import Optional

class CorporateGDriveManager:
    """Менеджер Google Drive для корпоративных отчетов"""
    
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    def __init__(self, credentials_file: str = "gdrive_credentials.json"):
        self.credentials_file = credentials_file
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Аутентификация в Google Drive API"""
        creds = None
        
        # Файл token.json хранит токены доступа и обновления
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        
        # Если нет действительных учетных данных, позволяем пользователю войти в систему
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Сохраняем учетные данные для следующего запуска
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return build('drive', 'v3', credentials=creds)
    
    def create_company_folder(self, company_name: str) -> dict:
        """Создает папку для компании"""
        folder_metadata = {
            'name': f"Отчеты_{company_name}_{datetime.now().strftime('%Y%m%d')}",
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        folder = self.service.files().create(body=folder_metadata, fields='id,name,webViewLink').execute()
        
        # Делаем папку общедоступной для чтения
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        self.service.permissions().create(fileId=folder['id'], body=permission).execute()
        
        return {
            'id': folder['id'],
            'name': folder['name'],
            'link': folder['webViewLink']
        }
    
    def upload_pdf_report(self, pdf_path: str, folder_id: str, employee_name: str) -> dict:
        """Загружает PDF отчет в папку компании"""
        file_metadata = {
            'name': f"Отчет_{employee_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            'parents': [folder_id]
        }
        
        media = MediaFileUpload(pdf_path, mimetype='application/pdf')
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink'
        ).execute()
        
        # Делаем файл общедоступным для чтения
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        self.service.permissions().create(fileId=file['id'], body=permission).execute()
        
        return {
            'id': file['id'],
            'name': file['name'],
            'link': file['webViewLink'],
            'download_link': f"https://drive.google.com/uc?export=download&id={file['id']}"
        }
    
    def get_folder_files(self, folder_id: str) -> list:
        """Получает список файлов в папке"""
        query = f"'{folder_id}' in parents and trashed=false"
        results = self.service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, createdTime, webViewLink)"
        ).execute()
        
        return results.get('files', [])

# === ИСПОЛЬЗОВАНИЕ В БОТЕ ===

class BotGDriveIntegration:
    """Интеграция Google Drive в Telegram бота"""
    
    def __init__(self):
        self.gdrive = CorporateGDriveManager()
        self.company_folders = {}  # кеш папок компаний
    
    async def setup_company_storage(self, company_id: str, company_name: str) -> str:
        """Настраивает хранилище для новой компании"""
        folder_info = self.gdrive.create_company_folder(company_name)
        self.company_folders[company_id] = folder_info
        
        return folder_info['link']
    
    async def store_employee_report(self, company_id: str, pdf_path: str, employee_name: str) -> tuple:
        """Сохраняет отчет сотрудника"""
        if company_id not in self.company_folders:
            raise ValueError(f"Папка для компании {company_id} не найдена")
        
        folder_id = self.company_folders[company_id]['id']
        file_info = self.gdrive.upload_pdf_report(pdf_path, folder_id, employee_name)
        
        return file_info['link'], file_info['download_link']
    
    async def get_company_reports_link(self, company_id: str) -> str:
        """Возвращает ссылку на папку с отчетами компании"""
        if company_id in self.company_folders:
            return self.company_folders[company_id]['link']
        return None

# === НАСТРОЙКА GOOGLE DRIVE API ===

"""
Шаги для настройки Google Drive API:

1. Создать проект в Google Cloud Console
2. Включить Google Drive API
3. Создать OAuth 2.0 credentials
4. Скачать credentials.json
5. Запустить первую аутентификацию

Команды для установки:
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""

if __name__ == "__main__":
    # Пример использования
    from datetime import datetime
    
    # Инициализация
    gdrive_manager = CorporateGDriveManager()
    
    # Создание папки для компании
    company_folder = gdrive_manager.create_company_folder("ООО Тест")
    print(f"Создана папка: {company_folder['name']}")
    print(f"Ссылка: {company_folder['link']}")
    
    # Загрузка тестового PDF (если есть)
    # pdf_info = gdrive_manager.upload_pdf_report("test_report.pdf", company_folder['id'], "Иванов_Иван")
    # print(f"Загружен файл: {pdf_info['name']}")
    # print(f"Ссылка для просмотра: {pdf_info['link']}")