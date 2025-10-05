#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест загрузки существующего PDF в Google Drive
"""

import os
from oauth_google_drive import upload_to_google_drive_oauth

def test_upload_existing_pdf():
    """Загружает существующий PDF в Google Drive"""
    
    # Проверяем наличие отладочного файла
    debug_file = "debug_page_numbers.pdf"
    
    if not os.path.exists(debug_file):
        print(f"❌ Файл {debug_file} не найден!")
        return
    
    print(f"📤 Загружаем {debug_file} в Google Drive...")
    
    # Загружаем в Google Drive
    try:
        web_link = upload_to_google_drive_oauth(
            file_path=debug_file,
            folder_name="PsychTest Reports", 
            use_monthly_structure=True
        )
        
        if web_link:
            print(f"✅ Файл успешно загружен!")
            print(f"🔗 Прямая ссылка: {web_link}")
            return web_link
        else:
            print("❌ Ошибка загрузки")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_upload_existing_pdf()