#!/usr/bin/env python3
"""
Тест динамических AI интерпретаций под диаграммами
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from datetime import datetime

def test_dynamic_ai_interpretations():
    """Тест динамических AI интерпретаций под каждой диаграммой"""
    print("🤖 ТЕСТ ДИНАМИЧЕСКИХ AI ИНТЕРПРЕТАЦИЙ")
    print("=" * 60)
    print("✅ Генерируем интерпретации с помощью AI используя промпты *_system_res.txt")
    print("✅ Размещаем интерпретации под каждой диаграммой")
    print("📤 Загружаем в Google Drive для визуального контроля")
    print()
    
    # Создаем генератор отчетов
    report_generator = EnhancedPDFReportV2()
    
    # Тестовые данные для демонстрации AI интерпретаций
    participant_name = "ТЕСТ ДИНАМИЧЕСКИХ AI ИНТЕРПРЕТАЦИЙ"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    # Разнообразные данные для интересных интерпретаций
    paei_scores = {
        "Предприниматель (E)": 94,  # Очень высокий
        "Администратор (A)": 67,    # Средний
        "Производитель (P)": 89,    # Высокий
        "Интегратор (I)": 73        # Выше среднего
    }
    
    disc_scores = {
        "Доминирование (D)": 91,    # Очень высокий
        "Влияние (I)": 78,          # Высокий
        "Постоянство (S)": 62,      # Ниже среднего
        "Соответствие (C)": 85      # Высокий
    }
    
    hexaco_scores = {
        "Честность": 95,            # Очень высокий
        "Эмоциональность": 58,      # Ниже среднего
        "Экстраверсия": 86,         # Высокий
        "Доброжелательность": 92,   # Очень высокий
        "Добросовестность": 98,     # Максимальный
        "Открытость опыту": 74      # Выше среднего
    }
    
    soft_skills_scores = {
        "Коммуникация": 93,         # Очень высокий
        "Лидерство": 96,            # Максимальный
        "Командная работа": 88,     # Высокий
        "Адаптивность": 79,         # Высокий
        "Решение проблем": 97       # Максимальный
    }
    
    # НЕ передаем ai_interpretations - они будут сгенерированы динамически!
    ai_interpretations = {}  # Пустой словарь - AI сам сгенерирует
    
    # Создаем имя файла
    out_path = Path(f"DYNAMIC_AI_INTERPRETATIONS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    print(f"👤 Участник: {participant_name}")
    print("🤖 Генерация PDF с динамическими AI интерпретациями...")
    print("📋 AI будет использовать промпты: adizes_system_res.txt, soft_system_res.txt, hexaco_system_res.txt, disk_system_res.txt")
    print()
    
    # Генерируем отчет с динамическими AI интерпретациями
    result = report_generator.generate_enhanced_report(
        participant_name=participant_name,
        test_date=test_date,
        paei_scores=paei_scores,
        disc_scores=disc_scores,
        hexaco_scores=hexaco_scores,
        soft_skills_scores=soft_skills_scores,
        ai_interpretations=ai_interpretations,  # Пустой - AI сгенерирует сам
        out_path=out_path
    )
    
    print()
    print("🔍 РЕЗУЛЬТАТ:")
    if isinstance(result, str) and result.startswith("https://"):
        print(f"✅ PDF с динамическими AI интерпретациями создан!")
        print(f"🔗 ССЫЛКА ДЛЯ ВИЗУАЛЬНОГО КОНТРОЛЯ:")
        print(f"🔗 {result}")
        print()
        print("👁️ ЧТО ПРОВЕРИТЬ В PDF:")
        print("   1. Откройте PDF по ссылке выше")
        print("   2. Найдите разделы с тестами и диаграммами:")
        print()
        print("   🤖 1. ТЕСТ АДИЗЕСА (PAEI)")
        print("      ↳ После диаграммы должна быть секция 'Интерпретация:'")
        print("      ↳ Текст сгенерирован AI на основе adizes_system_res.txt")
        print()
        print("   🤖 2. SOFT SKILLS")
        print("      ↳ После диаграммы должна быть секция 'Интерпретация:'")
        print("      ↳ Текст сгенерирован AI на основе soft_system_res.txt")
        print()
        print("   🤖 3. ТЕСТ HEXACO")
        print("      ↳ После диаграммы должна быть секция 'Интерпретация:'")
        print("      ↳ Текст сгенерирован AI на основе hexaco_system_res.txt")
        print()
        print("   🤖 4. ТЕСТ DISC")
        print("      ↳ После диаграммы должна быть секция 'Интерпретация:'")
        print("      ↳ Текст сгенерирован AI на основе disk_system_res.txt")
        print()
        print("   ✅ Интерпретации должны быть уникальными и соответствовать результатам")
        
        return result
    else:
        print(f"❌ Ошибка создания отчета: {result}")
        return None

if __name__ == "__main__":
    test_dynamic_ai_interpretations()