#!/usr/bin/env python3
"""Найти где находится папка 2025"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        print("🔍 Ищем все папки '2025'...")
        
        # Поиск всех папок с именем 2025
        query = "name='2025' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name, parents, webViewLink)").execute()
        folders = results.get('files', [])
        
        if folders:
            print(f"Найдено {len(folders)} папок '2025':")
            
            for i, folder in enumerate(folders, 1):
                print(f"\n{i}. 📁 2025 (ID: {folder['id']})")
                print(f"   🔗 {folder.get('webViewLink')}")
                
                # Найдем родительскую папку
                parents = folder.get('parents', [])
                if parents:
                    parent_id = parents[0]
                    try:
                        parent = service.files().get(fileId=parent_id, fields="id,name,webViewLink").execute()
                        print(f"   📂 Родительская: {parent.get('name')} (ID: {parent_id})")
                        print(f"   🔗 Родительская: {parent.get('webViewLink')}")
                        
                        # Проверим это наша целевая папка
                        if parent_id == "1Z77eo09GmcLuhsDGlb17E86vfb2p3jEM":
                            print(f"   ⭐ ЭТО НАША ЦЕЛЕВАЯ ПАПКА!")
                        
                    except Exception as e:
                        print(f"   ❌ Ошибка получения родителя: {e}")
                else:
                    print(f"   📂 Корневая папка")
                    
                # Проверим содержимое папки 2025
                query = f"'{folder['id']}' in parents and trashed=false"
                results = service.files().list(q=query, fields="files(id, name, mimeType)", pageSize=10).execute()
                contents = results.get('files', [])
                
                print(f"   📊 Содержимое ({len(contents)} элементов):")
                for item in contents[:5]:  # Показываем первые 5
                    icon = "📁" if item['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
                    print(f"      {icon} {item['name']}")
        else:
            print("❌ Папки '2025' не найдены")
            
        # Проверим что в нашей целевой папке
        target_id = "1Z77eo09GmcLuhsDGlb17E86vfb2p3jEM"
        print(f"\n🎯 Содержимое целевой папки ({target_id}):")
        
        query = f"'{target_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name, mimeType)", orderBy="name").execute()
        items = results.get('files', [])
        
        for item in items:
            icon = "📁" if item['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
            print(f"  {icon} {item['name']} (ID: {item['id']})")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()