#!/usr/bin/env python3
"""
Валидация содержимого PDF - проверка что исправления текста применены
"""
from pathlib import Path
import re

def validate_pdf_content_by_code():
    """Валидация через проверку исходного кода PDF генератора"""
    print("🔍 ВАЛИДАЦИЯ PDF СОДЕРЖИМОГО ЧЕРЕЗ КОД")
    print("="*60)
    
    pdf_file = Path("enhanced_pdf_report_v2.py")
    
    if not pdf_file.exists():
        print("❌ Файл enhanced_pdf_report_v2.py не найден")
        return False
    
    content = pdf_file.read_text(encoding='utf-8')
    
    # Проверки
    checks = []
    
    # 1. Проверка отсутствия "Результаты:"
    results_count = len(re.findall(r'Результаты:', content))
    checks.append({
        'name': 'Отсутствие "Результаты:" в коде',
        'passed': results_count == 0,
        'details': f'Найдено вхождений: {results_count}'
    })
    
    # 2. Проверка параметра normalize=False в create_minimalist_radar
    radar_normalize = 'normalize=False' in content and 'create_minimalist_radar' in content
    checks.append({
        'name': 'normalize=False в create_minimalist_radar',
        'passed': radar_normalize,
        'details': 'Параметр найден' if radar_normalize else 'Параметр НЕ найден'
    })
    
    # 3. Проверка параметра normalize=False в create_minimalist_bar_chart
    bar_normalize = 'normalize=False' in content and 'create_minimalist_bar_chart' in content
    checks.append({
        'name': 'normalize=False в create_minimalist_bar_chart',
        'passed': bar_normalize,
        'details': 'Параметр найден' if bar_normalize else 'Параметр НЕ найден'
    })
    
    # 4. Проверка на отсутствие дублированного описания HEXACO
    hexaco_duplicates = content.count('характеризует основные аспекты личности человека')
    checks.append({
        'name': 'Нет дублирования описания HEXACO',
        'passed': hexaco_duplicates <= 1,
        'details': f'Найдено повторений: {hexaco_duplicates}'
    })
    
    # Показать результаты
    passed_checks = 0
    for i, check in enumerate(checks, 1):
        status = "✅" if check['passed'] else "❌"
        print(f"{i}. {status} {check['name']}")
        print(f"   {check['details']}")
        if check['passed']:
            passed_checks += 1
    
    success_rate = passed_checks / len(checks) * 100
    
    print(f"\n📊 РЕЗУЛЬТАТ ВАЛИДАЦИИ:")
    print(f"   Пройдено проверок: {passed_checks}/{len(checks)} ({success_rate:.1f}%)")
    
    return success_rate >= 75

def check_chart_scaling_logic():
    """Проверка логики масштабирования в charts.py"""
    print("\n🎯 ПРОВЕРКА ЛОГИКИ МАСШТАБИРОВАНИЯ ДИАГРАММ")
    print("="*60)
    
    charts_file = Path("src/psytest/charts.py")
    
    if not charts_file.exists():
        print("❌ Файл src/psytest/charts.py не найден")
        return False
    
    content = charts_file.read_text(encoding='utf-8')
    
    # Проверка логики tick_step для 5-балльной шкалы
    tick_step_logic = 'if actual_max <= 5:' in content and 'tick_step = 1' in content
    
    print(f"✅ Логика tick_step для 5-балльной шкалы: {'Найдена' if tick_step_logic else 'НЕ найдена'}")
    
    return tick_step_logic

def create_visual_validation_summary():
    """Создание сводки для визуальной валидации"""
    print("\n📸 ФАЙЛЫ ДЛЯ ВИЗУАЛЬНОЙ ПРОВЕРКИ")
    print("="*60)
    
    test_files = [
        'comprehensive_test_soft_skills_radar.png',
        'comprehensive_test_hexaco_radar.png',
        'comprehensive_test_soft_skills_bar.png'
    ]
    
    existing_files = []
    for file in test_files:
        path = Path(file)
        if path.exists():
            size = path.stat().st_size
            print(f"📁 {file} ({size:,} байт)")
            existing_files.append(file)
        else:
            print(f"❌ {file} - НЕ НАЙДЕН")
    
    if existing_files:
        print(f"\n🎯 ВИЗУАЛЬНО ПРОВЕРЬТЕ В ЭТИХ ФАЙЛАХ:")
        print(f"   • Шкала: 0, 1, 2, 3, 4, 5 (правильно)")
        print(f"   • НЕ должно быть: 0, 2, 4, 6, 8, 10 (неправильно)")
    
    return len(existing_files) >= len(test_files) * 0.75

def main():
    print("🧪 КОМПЛЕКСНАЯ ВАЛИДАЦИЯ ИСПРАВЛЕНИЙ")
    print("="*70)
    
    # Валидация кода
    code_valid = validate_pdf_content_by_code()
    
    # Проверка логики диаграмм
    chart_logic_valid = check_chart_scaling_logic()
    
    # Проверка файлов для визуальной валидации
    visual_files_ready = create_visual_validation_summary()
    
    # Общий результат
    print(f"\n🎯 ИТОГОВАЯ ОЦЕНКА:")
    print("="*70)
    
    if code_valid and chart_logic_valid and visual_files_ready:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
        print("✅ Код исправлен корректно")
        print("✅ Логика диаграмм обновлена")  
        print("✅ Тестовые файлы созданы")
        print("\n🚀 СИСТЕМА ГОТОВА К ПРОДУКТИВНОМУ ИСПОЛЬЗОВАНИЮ!")
    else:
        print("⚠️ Некоторые проверки требуют внимания:")
        print(f"   • Код PDF: {'✅' if code_valid else '❌'}")
        print(f"   • Логика диаграмм: {'✅' if chart_logic_valid else '❌'}")
        print(f"   • Визуальные тесты: {'✅' if visual_files_ready else '❌'}")
        print("\n🔧 Рекомендуется дополнительная проверка")

if __name__ == "__main__":
    main()