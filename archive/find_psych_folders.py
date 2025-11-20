from oauth_google_drive import setup_oauth_google_drive

service = setup_oauth_google_drive()
if service:
    # Ищем папки с PsychTest в названии
    query = "mimeType='application/vnd.google-apps.folder' and name contains 'PsychTest'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])
    
    print(f"Найдено {len(folders)} папок с 'PsychTest':")
    for folder in folders:
        print(f"  {folder['name']}: {folder['id']}")
    
    if not folders:
        print("Папки с PsychTest не найдены. Показываю все папки:")
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder'", 
            fields="files(id, name)", 
            pageSize=20
        ).execute()
        all_folders = results.get('files', [])
        for folder in all_folders:
            print(f"  {folder['name']}: {folder['id']}")