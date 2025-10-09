#!/usr/bin/env python3
"""
Тест отступов для списков рекомендаций (как на скриншоте)
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from datetime import datetime

def test_list_indents():
    """Тест отступов для элементов списка в рекомендациях"""
    print("📋 ТЕСТ ОТСТУПОВ ДЛЯ СПИСКОВ")
    print("=" * 60)
    print("✅ Проверяем отступы для элементов списка как на скриншоте")
    print("✅ Элементы списка должны быть с отступом вправо")
    print()
    
    # Создаем генератор отчетов
    report_generator = EnhancedPDFReportV2()
    
    # Тестовые данные
    participant_name = "ТЕСТ ОТСТУПОВ СПИСКОВ"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    paei_scores = {
        "Предприниматель (E)": 92,
        "Администратор (A)": 78,
        "Производитель (P)": 89,
        "Интегратор (I)": 73
    }
    
    disc_scores = {
        "Доминирование (D)": 86,
        "Влияние (I)": 81,
        "Постоянство (S)": 69,
        "Соответствие (C)": 84
    }
    
    hexaco_scores = {
        "Честность": 91,
        "Эмоциональность": 62,
        "Экстраверсия": 79,
        "Доброжелательность": 87,
        "Добросовестность": 93,
        "Открытость опыту": 76
    }
    
    soft_skills_scores = {
        "Коммуникация": 88,
        "Лидерство": 85,
        "Командная работа": 82,
        "Адаптивность": 74,
        "Решение проблем": 96
    }
    
    ai_interpretations = {
        'paei': 'Выдающиеся предпринимательские качества с сильными производственными навыками.',
        'disc': 'Лидерский профиль с высоким доминированием и влиянием на команду.',
        'hexaco': 'Исключительная добросовестность и честность - идеальные качества руководителя.',
        'soft_skills': 'Превосходные навыки решения проблем и коммуникации.'
    }
    
    # Создаем имя файла
    out_path = Path(f"list_indents_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    print(f"👤 Участник: {participant_name}")
    print("📄 Генерация PDF с правильными отступами...")
    print()
    
    # Генерируем отчет
    result = report_generator.generate_enhanced_report(
        participant_name=participant_name,
        test_date=test_date,
        paei_scores=paei_scores,
        disc_scores=disc_scores,
        hexaco_scores=hexaco_scores,
        soft_skills_scores=soft_skills_scores,
        ai_interpretations=ai_interpretations,
        out_path=out_path
    )
    
    print()
    print("🔍 ПРОВЕРКА РЕЗУЛЬТАТОВ:")
    if isinstance(result, str) and result.startswith("https://"):
        print(f"✅ PDF создан и загружен в Google Drive!")
        print(f"🔗 Ссылка: {result}")
        print()
        print("👁️ ЧТО ПРОВЕРИТЬ В PDF:")
        print("   1. Раздел 'Рекомендации по профессиональному развитию'")
        print("   2. Элементы списка должны иметь отступ вправо")
        print("   3. Формат: '• (ТЕСТ): Описание' с отступом")
        print("   4. Три подраздела: Сильные стороны, Развитие, Карьера")
        print("   5. Четкая структура как на скриншоте")
    else:
        print(f"⚠️ Проблема с загрузкой: {result}")
    
    print()
    print("✅ ТЕСТ ЗАВЕРШЕН!")

if __name__ == "__main__":
    test_list_indents()