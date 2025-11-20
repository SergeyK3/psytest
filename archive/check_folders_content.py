from oauth_google_drive import setup_oauth_google_drive

service = setup_oauth_google_drive()
if service:
    folders = [
        ("Папка 1", "1usUktKpJROojo3rT_Goi3AmNhnMRCFyh"),
        ("Папка 2", "1nKqYCUVx7O5O0OskVKn25KJ8-qWs3Lbr")
    ]
    
    for name, folder_id in folders:
        print(f"\n=== {name}: {folder_id} ===")
        try:
            # Получаем содержимое папки
            query = f"'{folder_id}' in parents"
            results = service.files().list(
                q=query, 
                fields="files(id, name, mimeType, modifiedTime)", 
                pageSize=10,
                orderBy="modifiedTime desc"
            ).execute()
            files = results.get('files', [])
            
            print(f"Файлов в папке: {len(files)}")
            for file in files:
                modified = file.get('modifiedTime', '')[:10] if file.get('modifiedTime') else 'Unknown'
                print(f"  - {file['name']} ({modified})")
                
        except Exception as e:
            print(f"Ошибка: {e}")