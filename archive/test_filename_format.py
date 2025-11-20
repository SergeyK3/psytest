#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест формата имен файлов
"""

from pathlib import Path
from datetime import datetime

def test_filename_format():
    """Тестируем новый формат имен файлов"""
    
    # Имитируем данные сессии
    class MockSession:
        def __init__(self):
            self.name = "Ким Сергей"
            self.user_id = 300398364
    
    session = MockSession()
    
    # Формируем имена как в коде
    docs_dir = Path("docs")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    user_name_part = session.name.replace(' ', '_') if session.name else 'TelegramUser'
    
    # Пути для двух отчетов
    pdf_path_user = docs_dir / f"{timestamp}_{user_name_part}.pdf"                           # Для пользователя (чистое имя)
    pdf_path_gdrive = docs_dir / f"{timestamp}_{user_name_part}_(tg_{session.user_id})_full.pdf"    # Для Google Drive (с ID)
    
    print("🧪 Тест формата имен файлов:")
    print(f"👤 Для пользователя: {pdf_path_user.name}")
    print(f"☁️ Для Google Drive:  {pdf_path_gdrive.name}")
    
    # Проверяем формат
    user_correct = not "_tg_" in pdf_path_user.name
    gdrive_correct = f"_(tg_{session.user_id})_full.pdf" in pdf_path_gdrive.name
    
    print(f"\n✅ Формат пользователя правильный: {user_correct}")
    print(f"✅ Формат Google Drive правильный: {gdrive_correct}")
    
    if user_correct and gdrive_correct:
        print("\n🎯 Все форматы корректны!")
        return True
    else:
        print("\n❌ Есть проблемы с форматами!")
        return False

if __name__ == "__main__":
    test_filename_format()