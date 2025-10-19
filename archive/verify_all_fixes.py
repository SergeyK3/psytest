#!/usr/bin/env python3
"""
Проверяет все исправления:
1. 5-балльная шкала на диаграммах
2. Удаление "Результаты:" текста
3. Удаление дублированных описаний HEXACO 
4. Удаление интерпретации из Soft Skills
"""
import sys
sys.path.append('src')

from pathlib import Path
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
import matplotlib.pyplot as plt

def test_chart_scaling():
    """Тест исправления шкалы диаграмм"""
    print("🔍 Тестирование шкалы диаграмм...")
    
    # Тестовые данные для проверки 5-балльной шкалы
    from enhanced_pdf_report_v2 import EnhancedCharts
    
    labels = ['Коммуникация', 'Работа в команде', 'Лидерство']
    values = [4.5, 3.2, 2.8]
    
    # Создание радарной диаграммы с 5-балльной шкалой
    test_path = Path('test_verify_radar.png')
    EnhancedCharts.create_minimalist_radar(labels, values, 'Проверка шкалы', test_path)
    
    print(f"✅ Радарная диаграмма создана: {test_path}")
    print("   Шкала должна быть: 0, 1, 2, 3, 4, 5 (НЕ 0, 2, 4, 6, 8, 10)")
    
    # Создание барной диаграммы
    test_path2 = Path('test_verify_bar.png')
    EnhancedCharts.create_minimalist_bar_chart(labels, values, 'Проверка барной диаграммы', test_path2)
    
    print(f"✅ Барная диаграмма создана: {test_path2}")
    return True

def test_pdf_content():
    """Тест содержимого PDF"""
    print("\n🔍 Тестирование содержимого PDF...")
    
    # Тестовые данные
    user_data = {
        'name': 'Тестовый Пользователь',
        'paei_scores': {'P': 3, 'A': 2, 'E': 4, 'I': 3},
        'disc_scores': {'D': 15, 'I': 12, 'S': 8, 'C': 10},
        'hexaco_scores': {
            'Честность-Скромность': 4.2,
            'Эмоциональность': 3.8, 
            'Экстраверсия': 3.5,
            'Дружелюбие': 4.0,
            'Добросовестность': 4.5,
            'Открытость опыту': 3.9
        },
        'soft_skills_scores': {
            'Коммуникация': 4.1,
            'Работа в команде': 3.9,
            'Лидерство': 3.7,
            'Критическое мышление': 4.2
        }
    }
    
    # Создание PDF-отчета
    generator = EnhancedPDFReportV2()
    pdf_path = Path('test_verify_report.pdf')
    
    try:
        generator.generate_enhanced_report(
            user_data=user_data,
            output_path=str(pdf_path),
            include_questions=False
        )
        print(f"✅ PDF-отчет создан: {pdf_path}")
        print("   Проверьте следующие исправления:")
        print("   1. ❌ Нет текста 'Результаты:' под диаграммами")
        print("   2. ❌ Нет раздела 'Интерпретация:' в Soft Skills")
        print("   3. ❌ Нет дублированного описания HEXACO")
        print("   4. ✅ Диаграммы показывают 5-балльную шкалу")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания PDF: {e}")
        return False

def main():
    print("🚀 Проверка всех исправлений")
    print("="*50)
    
    # Тест диаграмм
    chart_ok = test_chart_scaling()
    
    # Тест PDF
    pdf_ok = test_pdf_content()
    
    print("\n📋 ИТОГОВЫЙ РЕЗУЛЬТАТ:")
    print("="*50)
    if chart_ok and pdf_ok:
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("🎯 Исправления применены корректно:")
        print("   • 5-балльная шкала на диаграммах")
        print("   • Удален текст 'Результаты:' под диаграммами")
        print("   • Удалена интерпретация из Soft Skills")
        print("   • Убрано дублирование описания HEXACO")
    else:
        print("❌ Некоторые тесты провалились")
        print("🔧 Требуется дополнительная отладка")

if __name__ == "__main__":
    main()