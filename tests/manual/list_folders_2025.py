import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
"""
Скрипт выводит все папки с именем '2025' в Google Drive, их ID и родителей.
"""

from oauth_google_drive import setup_oauth_google_drive

def list_folders_named_2025():
    service = setup_oauth_google_drive()
    query = "name='2025' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name, parents, owners)").execute()
    folders = results.get('files', [])
    print(f"Найдено папок с именем '2025': {len(folders)}")
    for f in folders:
        print(f"- ID: {f['id']}, parents: {f.get('parents')}, owners: {f.get('owners')}, name: {f['name']}")

if __name__ == "__main__":
    list_folders_named_2025()
