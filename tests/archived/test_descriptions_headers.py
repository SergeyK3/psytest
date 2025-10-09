#!/usr/bin/env python3
"""
Проверка размещения описаний тестов под заголовками разделов
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from datetime import datetime

def test_descriptions_under_headers():
    """Тест размещения описаний тестов под заголовками"""
    print("📝 ПРОВЕРКА ОПИСАНИЙ ПОД ЗАГОЛОВКАМИ")
    print("=" * 60)
    print("✅ Проверяем что описания тестов размещены под заголовками")
    print("✅ Как показано на скриншоте в красных рамках")
    print()
    
    # Создаем генератор отчетов
    report_generator = EnhancedPDFReportV2()
    
    # Тестовые данные
    participant_name = "ПРОВЕРКА ОПИСАНИЙ ТЕСТОВ"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    paei_scores = {
        "Предприниматель (E)": 90,
        "Администратор (A)": 85,
        "Производитель (P)": 92,
        "Интегратор (I)": 78
    }
    
    disc_scores = {
        "Доминирование (D)": 88,
        "Влияние (I)": 82,
        "Постоянство (S)": 75,
        "Соответствие (C)": 89
    }
    
    hexaco_scores = {
        "Честность": 94,
        "Эмоциональность": 66,
        "Экстраверсия": 83,
        "Доброжелательность": 90,
        "Добросовестность": 95,
        "Открытость опыту": 79
    }
    
    soft_skills_scores = {
        "Коммуникация": 92,
        "Лидерство": 89,
        "Командная работа": 86,
        "Адаптивность": 80,
        "Решение проблем": 96
    }
    
    ai_interpretations = {
        'paei': 'Выдающиеся производственные способности с сильными предпринимательскими качествами.',
        'disc': 'Сбалансированный профиль с акцентом на соответствие и доминирование.',
        'hexaco': 'Исключительная добросовестность и честность. Высокие моральные стандарты.',
        'soft_skills': 'Превосходные навыки решения проблем и коммуникации.'
    }
    
    # Создаем имя файла
    out_path = Path(f"test_descriptions_headers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    print(f"👤 Участник: {participant_name}")
    print("📄 Генерация PDF с описаниями под заголовками...")
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
        print(f"🔗 Ссылка: {result}")
        print()
        print("👁️ ЧТО ПРОВЕРИТЬ В PDF:")
        print("   1. Под заголовком '1. ТЕСТ АДИЗЕСА (PAEI)' есть описание:")
        print("      'Тест Адизеса (PAEI) - оценка управленческих ролей...'")
        print("   2. Под заголовком '2. SOFT SKILLS' есть описание:")
        print("      'Оценка Soft Skills - анализ надпрофессиональных...'")
        print("   3. Под заголовком '3. ТЕСТ HEXACO' есть описание:")
        print("      'HEXACO - современная шестифакторная модель...'")
        print("   4. Под заголовком '4. ТЕСТ DISC' есть описание:")
        print("      'DISC - методика оценки поведенческих...'")
        print("   5. Описания размещены как в красных рамках на скриншоте")
        
        return result
    else:
        print(f"❌ Ошибка создания отчета: {result}")
        return None

if __name__ == "__main__":
    test_descriptions_under_headers()