📋 ИНСТРУКЦИЯ: Установка Google Drive credentials

После скачивания JSON файла из Google Cloud Console:

1. Найдите скачанный файл (обычно в папке Downloads)
   Название будет примерно: psychteamtest-[случайные-символы].json

2. ПЕРЕИМЕНУЙТЕ файл в: google_drive_credentials.json

3. ПЕРЕМЕСТИТЕ файл в корневую папку проекта:
   📁 Целевая папка: d:\MyActivity\MyInfoBusiness\MyPythonApps\07 PsychTest\
   📄 Итоговый путь: d:\MyActivity\MyInfoBusiness\MyPythonApps\07 PsychTest\google_drive_credentials.json

4. Проверьте, что файл находится рядом с файлами:
   - enhanced_pdf_report_v2.py
   - telegram_test_bot.py
   - test_google_drive.py

⚠️ ВАЖНО: НЕ загружайте этот файл в git репозиторий! 
   Он уже добавлен в .gitignore для безопасности.

После установки файла можно будет протестировать интеграцию:
python test_google_drive.py