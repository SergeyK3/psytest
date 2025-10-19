#!/usr/bin/env python3
"""Проверяем текущий OAuth аккаунт"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        # Получаем информацию о текущем пользователе
        about = service.about().get(fields="user").execute()
        user = about.get('user', {})
        
        print("Текущий OAuth аккаунт:")
        print(f"  Email: {user.get('emailAddress', 'Неизвестно')}")
        print(f"  Имя: {user.get('displayName', 'Неизвестно')}")
        
        # Проверяем, есть ли доступ к нужной папке
        target_folder_id = "1TI-P8ZGj0IOjw97OmEpjyVc7jAW_hsy2"
        print(f"\nПроверяем доступ к папке: {target_folder_id}")
        
        try:
            folder = service.files().get(fileId=target_folder_id, fields="id,name").execute()
            print(f"✅ Папка доступна: {folder.get('name')}")
        except Exception as e:
            print(f"❌ Папка недоступна: {e}")
            print(f"\nНужно авторизоваться под аккаунтом: uz1.nursultan@gmail.com")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()