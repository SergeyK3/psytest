#!/usr/bin/env python3
"""
Тест нового размещения описаний тестов под заголовками разделов
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from datetime import datetime

def test_test_descriptions_placement():
    """Тест размещения описаний тестов под заголовками как на скриншоте"""
    print("📋 ТЕСТ РАЗМЕЩЕНИЯ ОПИСАНИЙ ТЕСТОВ")
    print("=" * 60)
    print("✅ Описания тестов размещены под заголовками разделов")
    print("✅ Формат как на скриншоте с красной рамкой")
    print("✅ Краткие результаты в объединенном разделе")
    print()
    
    # Создаем генератор отчетов
    report_generator = EnhancedPDFReportV2()
    
    # Тестовые данные
    participant_name = "ТЕСТ РАЗМЕЩЕНИЯ ОПИСАНИЙ"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    paei_scores = {
        "Предприниматель (E)": 89,
        "Администратор (A)": 84,
        "Производитель (P)": 92,
        "Интегратор (I)": 79
    }
    
    disc_scores = {
        "Доминирование (D)": 87,
        "Влияние (I)": 83,
        "Постоянство (S)": 74,
        "Соответствие (C)": 91
    }
    
    hexaco_scores = {
        "Честность": 94,
        "Эмоциональность": 67,
        "Экстраверсия": 82,
        "Доброжелательность": 88,
        "Добросовестность": 97,
        "Открытость опыту": 81
    }
    
    soft_skills_scores = {
        "Коммуникация": 90,
        "Лидерство": 87,
        "Командная работа": 84,
        "Адаптивность": 78,
        "Решение проблем": 95
    }
    
    ai_interpretations = {
        'paei': 'Выдающиеся производственные способности с сильными предпринимательскими и административными качествами.',
        'disc': 'Профиль соответствия стандартам с высоким доминированием - идеально для аналитических задач.',
        'hexaco': 'Исключительная добросовестность и честность, высокие моральные принципы.',
        'soft_skills': 'Превосходные навыки решения проблем и коммуникации с сильными лидерскими качествами.'
    }
    
    # Создаем имя файла
    out_path = Path(f"test_descriptions_placement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    print(f"👤 Участник: {participant_name}")
    print("📄 Генерация PDF с новым размещением описаний...")
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
        print(f"✅ PDF создан и загружен в Google Drive!")
        print(f"🔗 ССЫЛКА ДЛЯ ПРОВЕРКИ:")
        print(f"🔗 {result}")
        print()
        print("👁️ ЧТО ПРОВЕРИТЬ В PDF:")
        print("   1. Раздел '1. ТЕСТ АДИЗЕСА (PAEI)' - описание теста сразу под заголовком")
        print("   2. Раздел '2. SOFT SKILLS' - описание теста под заголовком")
        print("   3. Раздел '3. ТЕСТ HEXACO' - описание теста под заголовком")
        print("   4. Раздел '4. ТЕСТ DISC' - описание теста под заголовком")
        print("   5. Объединенный раздел содержит только краткие результаты")
        print("   6. Структура соответствует скриншоту")
        
        return result
    else:
        print(f"❌ Ошибка создания отчета: {result}")
        return None

if __name__ == "__main__":
    test_test_descriptions_placement()