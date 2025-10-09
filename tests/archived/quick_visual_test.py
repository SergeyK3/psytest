#!/usr/bin/env python3
"""
Быстрый тест для визуального контроля объединенного раздела
"""

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from datetime import datetime
from pathlib import Path

def visual_control_unified():
    """Создание PDF для визуального контроля объединенного раздела"""
    print("👁️ ВИЗУАЛЬНЫЙ КОНТРОЛЬ ОБЪЕДИНЕННОГО РАЗДЕЛА")
    print("=" * 60)
    print("🔗 Объединены: 'Ключевые характеристики' + 'Использованные методики'")
    print("📤 Загрузка в Google Drive для проверки...")
    print()
    
    report_generator = EnhancedPDFReportV2()
    
    # Тестовые данные
    participant_name = "ВИЗУАЛЬНЫЙ КОНТРОЛЬ ОБЪЕДИНЕНИЯ"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    paei_scores = {
        "Предприниматель (E)": 85,
        "Администратор (A)": 70,
        "Производитель (P)": 92,
        "Интегратор (I)": 68
    }
    
    disc_scores = {
        "Доминирование (D)": 78,
        "Влияние (I)": 82,
        "Постоянство (S)": 65,
        "Соответствие (C)": 90
    }
    
    hexaco_scores = {
        "Честность": 88,
        "Эмоциональность": 62,
        "Экстраверсия": 75,
        "Доброжелательность": 80,
        "Добросовестность": 93,
        "Открытость опыту": 72
    }
    
    soft_skills_scores = {
        "Коммуникация": 86,
        "Лидерство": 81,
        "Командная работа": 78,
        "Адаптивность": 74,
        "Решение проблем": 91
    }
    
    ai_interpretations = {
        'paei': 'Сильные производственные способности с предпринимательскими качествами.',
        'disc': 'Высокие показатели соответствия и влияния, сбалансированный профиль.',
        'hexaco': 'Отличная добросовестность и честность.',
        'soft_skills': 'Превосходные навыки решения проблем и коммуникации.'
    }
    
    out_path = Path(f"visual_unified_control_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    print(f"👤 Участник: {participant_name}")
    print("📄 Генерация PDF с объединенным разделом...")
    
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
    if isinstance(result, str) and result.startswith("https://"):
        print("✅ PDF создан и загружен в Google Drive!")
        print(f"🔗 ССЫЛКА ДЛЯ ВИЗУАЛЬНОГО КОНТРОЛЯ:")
        print(f"🔗 {result}")
        print()
        print("👁️ ЧТО ПРОВЕРИТЬ:")
        print("   1. Раздел 'Ключевые характеристики профиля и использованные методики'")
        print("   2. Объединенная информация в одном блоке")
        print("   3. Компактная верстка без дублирования")
        print("   4. Имя участника по центру без 'Имя сотрудника:'")
    else:
        print(f"⚠️ Проблема: {result}")
    
    print()
    print("✅ ГОТОВО ДЛЯ ВИЗУАЛЬНОГО КОНТРОЛЯ!")

if __name__ == "__main__":
    visual_control_unified()