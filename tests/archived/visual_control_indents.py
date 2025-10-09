#!/usr/bin/env python3
"""
Отчетный файл для визуального контроля отступов списков
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from datetime import datetime

def create_visual_control_report():
    """Создает отчет для визуального контроля отступов"""
    print("👁️ СОЗДАНИЕ ОТЧЕТА ДЛЯ ВИЗУАЛЬНОГО КОНТРОЛЯ")
    print("=" * 60)
    print("🎯 Проверяем отступы списков в разделе 'Рекомендации'")
    print("📤 Загружаем в Google Drive для визуального контроля")
    print()
    
    # Создаем генератор отчетов
    report_generator = EnhancedPDFReportV2()
    
    # Тестовые данные для демонстрации
    participant_name = "ВИЗУАЛЬНЫЙ КОНТРОЛЬ ОТСТУПОВ"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    paei_scores = {
        "Предприниматель (E)": 95,
        "Администратор (A)": 82,
        "Производитель (P)": 88,
        "Интегратор (I)": 76
    }
    
    disc_scores = {
        "Доминирование (D)": 89,
        "Влияние (I)": 84,
        "Постоянство (S)": 71,
        "Соответствие (C)": 87
    }
    
    hexaco_scores = {
        "Честность": 93,
        "Эмоциональность": 64,
        "Экстраверсия": 81,
        "Доброжелательность": 89,
        "Добросовестность": 96,
        "Открытость опыту": 78
    }
    
    soft_skills_scores = {
        "Коммуникация": 91,
        "Лидерство": 88,
        "Командная работа": 85,
        "Адаптивность": 77,
        "Решение проблем": 97
    }
    
    ai_interpretations = {
        'paei': 'Выдающиеся предпринимательские способности с отличными производственными результатами. Сильные лидерские качества.',
        'disc': 'Доминирующий лидерский профиль с высоким влиянием и способностью к соответствию стандартам.',
        'hexaco': 'Исключительная добросовестность и честность. Высокие моральные принципы и надежность.',
        'soft_skills': 'Превосходные навыки решения проблем и коммуникации. Отличный потенциал для руководящих позиций.'
    }
    
    # Создаем имя файла
    out_path = Path(f"VISUAL_CONTROL_INDENTS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    print(f"👤 Участник: {participant_name}")
    print("📄 Генерация отчета для визуального контроля...")
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
    print("🔍 РЕЗУЛЬТАТ:")
    if isinstance(result, str) and result.startswith("https://"):
        print(f"✅ Отчет создан и загружен в Google Drive!")
        print(f"🔗 ССЫЛКА ДЛЯ ВИЗУАЛЬНОГО КОНТРОЛЯ:")
        print(f"🔗 {result}")
        print()
        print("👁️ ЧТО ПРОВЕРЯТЬ:")
        print("   1. Откройте PDF по ссылке выше")
        print("   2. Найдите раздел 'Рекомендации по профессиональному развитию'")
        print("   3. Проверьте отступы элементов списка:")
        print("      • (PAEI): Делегировать задачи...")
        print("      • (Soft Skills): Развивать решение проблем...")
        print("      • (DISC): Использовать доминирование...")
        print("   4. Элементы должны быть сдвинуты вправо относительно заголовков")
        print("   5. Структура должна соответствовать скриншоту")
        
        return result
    else:
        print(f"❌ Ошибка создания отчета: {result}")
        return None

if __name__ == "__main__":
    create_visual_control_report()