#!/usr/bin/env python3
"""Тест загрузки с отладкой"""

import os
from oauth_google_drive import upload_to_google_drive_oauth

def main():
    # Создаем тестовый файл
    test_file = "debug_test.pdf"
    with open(test_file, 'w') as f:
        f.write("Тест загрузки")
    
    print("🔧 Параметры загрузки:")
    print("   folder_id: 1BFT4qQHJjS--qAx0Y7-3nJgKjlVl3grb")
    print("   use_monthly_structure: False")
    print("   Должен загружаться прямо в папку 2025")
    
    # Загружаем с явными параметрами
    result = upload_to_google_drive_oauth(
        file_path=test_file,
        folder_id="1BFT4qQHJjS--qAx0Y7-3nJgKjlVl3grb",  # Папка 2025
        use_monthly_structure=False  # НЕ создавать подпапки
    )
    
    if result:
        print(f"✅ Успех! Ссылка: {result}")
    else:
        print("❌ Ошибка загрузки")
    
    # Удаляем тестовый файл
    if os.path.exists(test_file):
        os.remove(test_file)

if __name__ == "__main__":
    main()