#!/usr/bin/env python3
"""
Отчетный файл для визуального контроля динамических интерпретаций тестов
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from datetime import datetime

def create_visual_control_ai_interpretations():
    """Создает отчет для визуального контроля динамических интерпретаций"""
    print("🤖 СОЗДАНИЕ ОТЧЕТА С ДИНАМИЧЕСКИМИ ИНТЕРПРЕТАЦИЯМИ")
    print("=" * 60)
    print("🎯 Проверяем AI интерпретации под диаграммами")
    print("📋 Используем промпты *_system_res.txt для генерации")
    print("📤 Загружаем в Google Drive для визуального контроля")
    print()
    
    # Создаем генератор отчетов
    report_generator = EnhancedPDFReportV2()
    
    # Демонстрационные данные
    participant_name = "ВИЗУАЛЬНЫЙ КОНТРОЛЬ AI ИНТЕРПРЕТАЦИЙ"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    paei_scores = {
        "Предприниматель (E)": 94,
        "Администратор (A)": 89,
        "Производитель (P)": 93,
        "Интегратор (I)": 86
    }
    
    disc_scores = {
        "Доминирование (D)": 92,
        "Влияние (I)": 87,
        "Постоянство (S)": 79,
        "Соответствие (C)": 91
    }
    
    hexaco_scores = {
        "Честность": 97,
        "Эмоциональность": 71,
        "Экстраверсия": 88,
        "Доброжелательность": 93,
        "Добросовестность": 99,
        "Открытость опыту": 84
    }
    
    soft_skills_scores = {
        "Коммуникация": 96,
        "Лидерство": 93,
        "Командная работа": 90,
        "Адаптивность": 86,
        "Решение проблем": 100
    }
    
    # Фиктивные интерпретации (будут заменены на динамические AI)
    ai_interpretations = {
        'paei': 'Будет заменено на AI интерпретацию с adizes_system_res.txt',
        'disc': 'Будет заменено на AI интерпретацию с disk_system_res.txt',
        'hexaco': 'Будет заменено на AI интерпретацию с hexaco_system_res.txt',
        'soft_skills': 'Будет заменено на AI интерпретацию с soft_system_res.txt'
    }
    
    # Создаем имя файла
    out_path = Path(f"VISUAL_AI_INTERPRETATIONS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    print(f"👤 Участник: {participant_name}")
    print("📄 Генерация отчета с AI интерпретациями...")
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
        print("   2. Найдите каждый раздел тестирования:")
        print()
        print("   🤖 1. ТЕСТ АДИЗЕСА (PAEI) - УПРАВЛЕНЧЕСКИЕ РОЛИ")
        print("      ✓ Описание теста под заголовком")
        print("      ✓ Диаграмма PAEI")
        print("      ✓ 'Интерпретация:' с динамическим AI анализом")
        print()
        print("   🤖 2. SOFT SKILLS - ОЦЕНКА МЯГКИХ НАВЫКОВ")
        print("      ✓ Описание теста под заголовком")
        print("      ✓ Диаграмма Soft Skills")
        print("      ✓ 'Интерпретация:' с динамическим AI анализом")
        print()
        print("   🤖 3. ТЕСТ HEXACO - МОДЕЛЬ ЛИЧНОСТИ")
        print("      ✓ Описание теста под заголовком")
        print("      ✓ Диаграмма HEXACO")
        print("      ✓ 'Интерпретация:' с динамическим AI анализом")
        print()
        print("   🤖 4. ТЕСТ DISC - МОДЕЛЬ ПОВЕДЕНИЯ")
        print("      ✓ Описание теста под заголовком")
        print("      ✓ Диаграмма DISC")
        print("      ✓ 'Интерпретация:' с динамическим AI анализом")
        print()
        print("   ⚡ ОЖИДАНИЯ:")
        print("   - Интерпретации генерируются AI с помощью промптов *_system_res.txt")
        print("   - Интерпретации детальные и персонализированные")
        print("   - Если AI недоступен - используются статические интерпретации")
        
        return result
    else:
        print(f"❌ Ошибка создания отчета: {result}")
        return None

if __name__ == "__main__":
    create_visual_control_ai_interpretations()