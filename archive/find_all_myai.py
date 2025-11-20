#!/usr/bin/env python3
"""Поиск всех доступных папок MyAiProjects"""

from oauth_google_drive import setup_oauth_google_drive

def main():
    try:
        service = setup_oauth_google_drive()
        if not service:
            print("Не удалось получить доступ к Google Drive")
            return

        print("🔍 Поиск всех папок MyAiProjects...")
        
        # Ищем все папки MyAiProjects
        query = "mimeType='application/vnd.google-apps.folder' and name='MyAiProjects'"
        results = service.files().list(q=query, fields="files(id, name, webViewLink, createdTime)", orderBy="createdTime desc").execute()
        folders = results.get('files', [])
        
        if folders:
            print(f"Найдено {len(folders)} папок MyAiProjects:")
            
            for i, folder in enumerate(folders, 1):
                print(f"\n{i}. 📁 {folder['name']} (ID: {folder['id']})")
                print(f"   🔗 {folder.get('webViewLink')}")
                print(f"   📅 Создана: {folder.get('createdTime', 'Неизвестно')}")
                
                # Проверяем содержимое каждой папки
                folder_id = folder['id']
                query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
                results = service.files().list(q=query, fields="files(id, name)", pageSize=10).execute()
                subfolders = results.get('files', [])
                
                print(f"   📊 Подпапки ({len(subfolders)}):")
                for subfolder in subfolders:
                    icon = "⭐" if "PsychTest" in subfolder['name'] else "📁"
                    print(f"      {icon} {subfolder['name']} (ID: {subfolder['id']})")
                    
                    # Если это PsychTest Reports old, проверим его содержимое
                    if subfolder['name'] == 'PsychTest Reports old':
                        print(f"      🎯 Найдена целевая папка! ID: {subfolder['id']}")
        else:
            print("❌ Папки MyAiProjects не найдены")
            
            # Покажем все доступные папки
            print("\nВсе доступные папки:")
            query = "mimeType='application/vnd.google-apps.folder'"
            results = service.files().list(q=query, fields="files(id, name)", pageSize=20).execute()
            all_folders = results.get('files', [])
            
            for folder in all_folders:
                print(f"  📁 {folder['name']} (ID: {folder['id']})")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()