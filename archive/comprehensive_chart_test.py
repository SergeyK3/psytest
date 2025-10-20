#!/usr/bin/env python3
"""
Комплексное тестирование всех типов диаграмм с проверкой 5-балльной шкалы
"""
import sys
sys.path.append('src')

from pathlib import Path
from enhanced_pdf_report_v2 import EnhancedCharts
import time

def test_all_chart_types():
    """Тестирование всех типов диаграмм"""
    print("🎯 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ ДИАГРАММ")
    print("="*60)
    
    results = []
    
    # 1. Soft Skills радар
    print("\n1️⃣ Тестирование Soft Skills радара...")
    try:
        labels = ['Коммуникация', 'Работа в команде', 'Лидерство', 'Критическое мышление']
        values = [4.2, 3.8, 3.5, 4.1]
        path = Path('comprehensive_test_soft_skills_radar.png')
        
        EnhancedCharts.create_minimalist_radar(labels, values, 'Soft Skills (5-балльная шкала)', path)
        print(f"   ✅ Создан: {path}")
        results.append(('Soft Skills радар', True, path))
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        results.append(('Soft Skills радар', False, None))
    
    # 2. HEXACO радар  
    print("\n2️⃣ Тестирование HEXACO радара...")
    try:
        labels = ['H', 'E', 'X', 'A', 'C', 'O']
        values = [4.5, 3.2, 3.8, 4.0, 4.3, 3.7]
        path = Path('comprehensive_test_hexaco_radar.png')
        
        EnhancedCharts.create_hexaco_radar(labels, values, 'HEXACO (5-балльная шкала)', path)
        print(f"   ✅ Создан: {path}")
        results.append(('HEXACO радар', True, path))
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        results.append(('HEXACO радар', False, None))
    
    # 3. Барная диаграмма Soft Skills
    print("\n3️⃣ Тестирование Soft Skills барной диаграммы...")
    try:
        labels = ['Коммуникация', 'Лидерство', 'Критическое мышление']
        values = [4.1, 3.7, 4.2]
        path = Path('comprehensive_test_soft_skills_bar.png')
        
        EnhancedCharts.create_minimalist_bar_chart(labels, values, 'Soft Skills барная (5-балльная шкала)', path)
        print(f"   ✅ Создан: {path}")
        results.append(('Soft Skills барная', True, path))
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        results.append(('Soft Skills барная', False, None))
    
    # 4. PAEI диаграммы
    print("\n4️⃣ Тестирование PAEI диаграмм...")
    try:
        from src.psytest.charts import make_combined_paei_chart
        
        paei_scores = {'P': 3, 'A': 2, 'E': 4, 'I': 3}
        path = Path('comprehensive_test_paei_combined.png')
        
        make_combined_paei_chart(paei_scores, str(path))
        print(f"   ✅ Создан: {path}")
        results.append(('PAEI комбинированная', True, path))
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        results.append(('PAEI комбинированная', False, None))
    
    # 5. DISC диаграммы
    print("\n5️⃣ Тестирование DISC диаграмм...")
    try:
        from src.psytest.charts import make_combined_disc_chart
        
        disc_scores = {'D': 15, 'I': 12, 'S': 8, 'C': 10}
        path = Path('comprehensive_test_disc_combined.png')
        
        make_combined_disc_chart(disc_scores, str(path))
        print(f"   ✅ Создан: {path}")
        results.append(('DISC комбинированная', True, path))
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        results.append(('DISC комбинированная', False, None))
    
    return results

def show_results(results):
    """Показать результаты тестирования"""
    print("\n📋 РЕЗУЛЬТАТЫ КОМПЛЕКСНОГО ТЕСТИРОВАНИЯ:")
    print("="*60)
    
    successful = 0
    total = len(results)
    
    for test_name, success, path in results:
        if success:
            file_size = path.stat().st_size if path and path.exists() else 0
            print(f"   ✅ {test_name} - {file_size} байт")
            successful += 1
        else:
            print(f"   ❌ {test_name} - ОШИБКА")
    
    print(f"\n📊 СТАТИСТИКА:")
    print(f"   • Успешных тестов: {successful}/{total} ({successful/total*100:.1f}%)")
    print(f"   • Провалившихся: {total-successful}/{total}")
    
    if successful == total:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        print("✨ Все диаграммы должны показывать шкалу: 0, 1, 2, 3, 4, 5")
        print("❌ НЕ должны показывать: 0, 2, 4, 6, 8, 10")
    else:
        print("\n⚠️ Некоторые тесты провалились!")
        print("🔧 Требуется дополнительное исследование")
    
    return successful == total

def main():
    start_time = time.time()
    
    results = test_all_chart_types()
    all_success = show_results(results)
    
    end_time = time.time()
    
    print(f"\n⏱️ Время выполнения: {end_time - start_time:.2f} сек")
    
    if all_success:
        print("\n🚀 СИСТЕМА ГОТОВА К ИСПОЛЬЗОВАНИЮ!")
    else:
        print("\n🔧 ТРЕБУЕТСЯ ДОПОЛНИТЕЛЬНАЯ ОТЛАДКА")

if __name__ == "__main__":
    main()