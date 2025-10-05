#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест улучшенного формата нумерации страниц: "Стр. X из N"
"""

import sys
import os
from pathlib import Path
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from oauth_google_drive import upload_to_google_drive_oauth

def test_enhanced_numbering():
    """Тестирует новый формат нумерации страниц"""
    
    print("🔢 ТЕСТ УЛУЧШЕННОЙ НУМЕРАЦИИ СТРАНИЦ")
    print("=" * 60)
    print("🎯 Формат: 'Стр. X из N'")
    print("📤 Загрузка в Google Drive для контроля")
    print()
    
    # Тестовые данные
    test_participant = "ТЕСТ ФОРМАТА НУМЕРАЦИИ"
    test_scores = {
        'paei': {'P': 85, 'A': 75, 'E': 90, 'I': 70},
        'disc': {'D': 80, 'I': 85, 'S': 70, 'C': 75},
        'hexaco': {
            'Честность-Скромность': 82,
            'Эмоциональность': 68, 
            'Экстраверсия': 90,
            'Доброжелательность': 85,
            'Добросовестность': 88,
            'Открытость опыту': 92
        },
        'soft_skills': {
            'Коммуникация': 88,
            'Лидерство': 85,
            'Командная работа': 90,
            'Адаптивность': 82,
            'Критическое мышление': 87,
            'Управление временем': 83,
            'Эмоциональный интеллект': 86,
            'Креативность': 89
        }
    }
    
    # Создаем генератор отчета
    generator = EnhancedPDFReportV2()
    
    # Генерируем отчет
    print(f"📄 Создание отчета с улучшенной нумерацией...")
    
    # Путь для сохранения
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"enhanced_numbering_{timestamp}.pdf")
    
    # Простые AI интерпретации для теста
    ai_interpretations = {
        'paei': 'Тестовая интерпретация PAEI для проверки нумерации страниц.',
        'disc': 'Тестовая интерпретация DISC для проверки нумерации страниц.',
        'hexaco': 'Тестовая интерпретация HEXACO для проверки нумерации страниц.',
        'soft_skills': 'Тестовая интерпретация Soft Skills для проверки нумерации страниц.'
    }
    
    pdf_path = generator.generate_enhanced_report(
        participant_name=test_participant,
        test_date="2025-10-05",
        paei_scores=test_scores['paei'],
        disc_scores=test_scores['disc'],
        hexaco_scores=test_scores['hexaco'],
        soft_skills_scores=test_scores['soft_skills'],
        ai_interpretations=ai_interpretations,
        out_path=output_path
    )
    
    # Получаем размер файла
    file_size = os.path.getsize(pdf_path)
    print(f"📊 Размер файла: {file_size} байт ({file_size/1024:.1f} KB)")
    
    # Загружаем в Google Drive
    print("📤 Загрузка в Google Drive...")
    try:
        drive_link = upload_to_google_drive_oauth(pdf_path, "ТЕСТ ФОРМАТА НУМЕРАЦИИ")
        if drive_link:
            print("✅ Успешно загружено в Google Drive!")
            print(f"🔗 Ссылка: {drive_link}")
        else:
            print("❌ Ошибка загрузки в Google Drive")
    except Exception as e:
        print(f"❌ Ошибка Google Drive: {e}")
    
    print()
    print("✅ ТЕСТ ЗАВЕРШЕН!")
    print(f"📄 Локальный файл: {pdf_path}")
    if 'drive_link' in locals():
        print(f"🔗 Google Drive: {drive_link}")
    print()
    print("👁️ ЧТО ПРОВЕРИТЬ:")
    print("   1. Откройте PDF файл")
    print("   2. На КАЖДОЙ странице в верхнем правом углу")
    print("   3. Должно быть: 'Стр. 1 из N', 'Стр. 2 из N', и т.д.")
    print("   4. Где N - общее количество страниц")
    print("   5. Убедитесь что цифра общих страниц одинакова на всех страницах")

if __name__ == "__main__":
    test_enhanced_numbering()