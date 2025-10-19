#!/usr/bin/env python3
"""
Отчетный файл для визуального контроля размещения описаний тестов под заголовками
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from datetime import datetime

def create_visual_control_descriptions():
    """Создает отчет для визуального контроля описаний под заголовками"""
    print("📝 СОЗДАНИЕ ОТЧЕТА ДЛЯ ВИЗУАЛЬНОГО КОНТРОЛЯ")
    print("=" * 60)
    print("🎯 Проверяем размещение описаний тестов под заголовками")
    print("📋 Как показано на скриншоте в красных рамках")
    print("📤 Загружаем в Google Drive для визуального контроля")
    print()
    
    # Создаем генератор отчетов
    report_generator = EnhancedPDFReportV2()
    
    # Демонстрационные данные
    participant_name = "ВИЗУАЛЬНЫЙ КОНТРОЛЬ ОПИСАНИЙ"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    paei_scores = {
        "Предприниматель (E)": 93,
        "Администратор (A)": 87,
        "Производитель (P)": 91,
        "Интегратор (I)": 82
    }
    
    disc_scores = {
        "Доминирование (D)": 90,
        "Влияние (I)": 85,
        "Постоянство (S)": 77,
        "Соответствие (C)": 92
    }
    
    hexaco_scores = {
        "Честность": 96,
        "Эмоциональность": 68,
        "Экстраверсия": 84,
        "Доброжелательность": 91,
        "Добросовестность": 97,
        "Открытость опыту": 81
    }
    
    soft_skills_scores = {
        "Коммуникация": 94,
        "Лидерство": 91,
        "Командная работа": 88,
        "Адаптивность": 83,
        "Решение проблем": 98
    }
    
    ai_interpretations = {
        'paei': 'Выдающиеся предпринимательские и производственные способности. Отличные лидерские качества для руководящих позиций.',
        'disc': 'Сильный лидерский профиль с высоким соответствием стандартам и доминированием в принятии решений.',
        'hexaco': 'Исключительная добросовестность и честность. Высочайшие моральные принципы и надежность в работе.',
        'soft_skills': 'Превосходные навыки решения проблем и коммуникации. Идеальный кандидат для руководящих позиций.'
    }
    
    # Создаем имя файла
    out_path = Path(f"VISUAL_CONTROL_DESCRIPTIONS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
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
        print("📋 ЧТО ПРОВЕРЯТЬ В PDF:")
        print("   1. Откройте PDF по ссылке выше")
        print("   2. Найдите разделы с тестами:")
        print()
        print("   📝 1. ТЕСТ АДИЗЕСА (PAEI) - УПРАВЛЕНЧЕСКИЕ РОЛИ")
        print("      ↳ Сразу под заголовком должно быть:")
        print("        'Тест Адизеса (PAEI) - оценка управленческих ролей и стилей руководства (5 вопросов по 4 типам).'")
        print()
        print("   📝 2. SOFT SKILLS - ОЦЕНКА МЯГКИХ НАВЫКОВ")
        print("      ↳ Сразу под заголовком должно быть:")
        print("        'Оценка Soft Skills - анализ надпрофессиональных компетенций (10 вопросов по 5-балльной шкале).'")
        print()
        print("   📝 3. ТЕСТ HEXACO - МОДЕЛЬ ЛИЧНОСТИ")
        print("      ↳ Сразу под заголовком должно быть:")
        print("        'HEXACO - современная шестифакторная модель личности (10 вопросов по 5-балльной шкале).'")
        print()
        print("   📝 4. ТЕСТ DISC - МОДЕЛЬ ПОВЕДЕНИЯ")
        print("      ↳ Сразу под заголовком должно быть:")
        print("        'DISC - методика оценки поведенческих особенностей и стилей (8 вопросов по 4 типам).'")
        print()
        print("   ✅ Каждое описание должно быть в красной рамке как на скриншоте")
        
        return result
    else:
        print(f"❌ Ошибка создания отчета: {result}")
        return None

if __name__ == "__main__":
    create_visual_control_descriptions()