#!/usr/bin/env python3
"""Поиск и восстановление файлов из корзины Google Drive"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        print("🔍 Ищем файлы в корзине...")
        
        # Поиск файлов в корзине (trashed=true)
        query = "trashed=true"
        results = service.files().list(
            q=query, 
            fields="files(id, name, mimeType, trashedTime, parents)", 
            orderBy="trashedTime desc",
            pageSize=50
        ).execute()
        files = results.get('files', [])
        
        if not files:
            print("❌ Корзина пуста")
            return
        
        print(f"📊 Найдено файлов в корзине: {len(files)}")
        
        # Ищем папки PsychTest
        psychtest_folders = [f for f in files if f['mimeType'] == 'application/vnd.google-apps.folder' and 'PsychTest' in f['name']]
        
        if psychtest_folders:
            print(f"\n📁 Папки PsychTest в корзине ({len(psychtest_folders)} шт.):")
            for folder in psychtest_folders:
                print(f"  📁 {folder['name']} (ID: {folder['id']})")
                print(f"     Удалена: {folder.get('trashedTime', 'Неизвестно')}")
                
                # Пробуем восстановить
                print(f"     🔄 Попытка восстановления...")
                try:
                    body = {'trashed': False}
                    restored = service.files().update(fileId=folder['id'], body=body).execute()
                    print(f"     ✅ Восстановлена: {restored.get('name')}")
                    
                    # Получаем ссылку на восстановленную папку
                    folder_info = service.files().get(fileId=folder['id'], fields="webViewLink").execute()
                    print(f"     🔗 Ссылка: {folder_info.get('webViewLink')}")
                    
                except Exception as e:
                    print(f"     ❌ Ошибка восстановления: {e}")
        else:
            print("\n❌ Папки PsychTest в корзине не найдены")
            
            # Покажем что есть в корзине
            print(f"\nВ корзине найдено:")
            for file in files[:10]:  # Показываем первые 10
                icon = "📁" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
                print(f"  {icon} {file['name']} (ID: {file['id']})")
        
        # Проверим доступность целевой папки после восстановления
        target_id = "1TI-P8ZGj0IOjw97OmEpjyVc7jAW_hsy2"
        print(f"\n🎯 Проверяем целевую папку: {target_id}")
        try:
            folder = service.files().get(fileId=target_id, fields="id,name,webViewLink").execute()
            print(f"✅ Папка доступна: {folder.get('name')}")
            print(f"🔗 Ссылка: {folder.get('webViewLink')}")
            return target_id
        except Exception as e:
            print(f"❌ Папка все еще недоступна: {e}")
            return None
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n🎉 Папка восстановлена! ID: {result}")
        print("Теперь можно обновить код для использования восстановленной папки")
    else:
        print("\n❌ Не удалось восстановить папку")