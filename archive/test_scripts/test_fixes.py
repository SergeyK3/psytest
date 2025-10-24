#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест исправлений DISC и Soft Skills форматирования
"""

import os
import sys
from pathlib import Path

# Добавляем src в путь
sys.path.append(str(Path(__file__).parent / "src"))

from enhanced_pdf_report_v2 import EnhancedPDFReportV2

# Тестовые данные
test_data = {
    'paei_scores': {'P': 1, 'A': 1, 'E': 0, 'I': 3},
    'disc_scores': {'D': 4.0, 'I': 3.0, 'S': 2.5, 'C': 4.0},
    'hexaco_scores': {'H': 4, 'E': 1, 'X': 3, 'A': 2, 'C': 5, 'O': 3},
    'soft_skills_scores': {
        'Коммуникация': 4.0,
        'Работа в команде': 4.0,
        'Лидерство': 4.0,
        'Критическое мышление': 4.0,
        'Управление временем': 4.0,
        'Стрессоустойчивость': 4.0,
        'Восприимчивость к критике': 3.0,
        'Адаптивность': 4.0,
        'Решение проблем': 4.0,
        'Креативность': 3.0
    }
}

print("🚀 Тестируем исправления в PDF генерации...")
print(f"📊 Тестовые данные готовы")

try:
    # Создаем генератор отчетов
    pdf_generator = EnhancedPDFReportV2()
    
    # Генерируем тестовый отчет
    output_path = "test_fixed_formatting.pdf"
    
    print("📄 Генерируем PDF отчет...")
    
    pdf_path, _ = pdf_generator.generate_enhanced_report(
        participant_name="Тест Исправлений",
        test_date="2025-10-24",
        paei_scores=test_data['paei_scores'],
        disc_scores=test_data['disc_scores'],
        hexaco_scores=test_data['hexaco_scores'],
        soft_skills_scores=test_data['soft_skills_scores'],
        ai_interpretations={},  # Пустые AI интерпретации для простоты
        out_path=Path(output_path),
        user_answers={}  # Пустые ответы для простоты
    )
    
    print(f"✅ PDF успешно создан: {pdf_path}")
    print("\n🔍 Проверьте следующие исправления:")
    print("1. ✅ DISC интерпретация не должна быть пустой")
    print("2. ✅ Soft Skills без нумерации (без 1., 2., 3.)")
    print(f"\n📁 Файл сохранен как: {os.path.abspath(pdf_path)}")
    
except Exception as e:
    print(f"❌ Ошибка при генерации PDF: {e}")
    import traceback
    traceback.print_exc()