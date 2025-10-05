#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест нумерации страниц - создает короткий PDF для быстрой проверки видимости нумерации
"""

from final_full_numbered_generator import FinalFullVolumeGenerator

def test_page_numbering():
    """Создает короткий PDF для проверки нумерации"""
    
    print("🔢 Тест видимости нумерации страниц...")
    
    # Создаем отчет БЕЗ загрузки в Google Drive для быстрой проверки
    generator = FinalFullVolumeGenerator()
    
    file_path, gdrive_link = generator.generate_full_volume_report(
        participant_name="ТЕСТ НУМЕРАЦИИ",
        filename="test_page_numbering.pdf",
        upload_to_gdrive=False  # Отключаем загрузку для быстроты
    )
    
    print(f"✅ Тестовый PDF создан: {file_path}")
    print("🔍 Проверьте правый верхний угол каждой страницы!")
    print("📌 Должно быть видно: 'Стр. X из N' с увеличенным шрифтом")
    
    # Открываем файл правильной командой
    import subprocess
    try:
        subprocess.run(['cmd', '/c', 'start', '', file_path], shell=False)
        print(f"📖 Открываем PDF: {file_path}")
    except Exception as e:
        print(f"⚠️ Не удалось открыть PDF автоматически: {e}")
        print(f"📁 Откройте файл вручную: {file_path}")

if __name__ == "__main__":
    test_page_numbering()