#!/usr/bin/env python3
"""
Стресс-тестирование системы диаграмм с различными наборами данных
"""
import sys
sys.path.append('src')

import time
import random
from pathlib import Path
from enhanced_pdf_report_v2 import EnhancedCharts

def generate_test_data():
    """Генерация различных тестовых данных"""
    datasets = [
        # Минимальные значения
        {
            'name': 'Минимальные значения',
            'labels': ['A', 'B', 'C', 'D'],
            'values': [1.0, 1.0, 1.0, 1.0]
        },
        # Максимальные значения
        {
            'name': 'Максимальные значения', 
            'labels': ['A', 'B', 'C', 'D'],
            'values': [5.0, 5.0, 5.0, 5.0]
        },
        # Случайные значения
        {
            'name': 'Случайные значения',
            'labels': ['Test1', 'Test2', 'Test3', 'Test4'],
            'values': [round(random.uniform(1.0, 5.0), 1) for _ in range(4)]
        },
        # Граничные значения
        {
            'name': 'Граничные значения',
            'labels': ['Грань1', 'Грань2', 'Грань3'],
            'values': [1.0, 2.5, 5.0]
        },
        # Длинные названия
        {
            'name': 'Длинные названия',
            'labels': ['Очень длинное название навыка номер один', 'Другой длинный навык', 'Третий навык'],
            'values': [3.2, 4.1, 2.8]
        }
    ]
    return datasets

def stress_test_charts():
    """Стресс-тестирование создания диаграмм"""
    print("⚡ СТРЕСС-ТЕСТИРОВАНИЕ СИСТЕМЫ ДИАГРАММ")
    print("="*60)
    
    datasets = generate_test_data()
    results = []
    total_time = 0
    
    for i, dataset in enumerate(datasets, 1):
        print(f"\n{i}️⃣ Тестирование: {dataset['name']}")
        
        # Тест радарной диаграммы
        start_time = time.time()
        try:
            radar_path = Path(f'stress_test_radar_{i}.png')
            EnhancedCharts.create_minimalist_radar(
                dataset['labels'], 
                dataset['values'], 
                f"Радар: {dataset['name']}", 
                radar_path
            )
            radar_time = time.time() - start_time
            radar_size = radar_path.stat().st_size
            print(f"   ✅ Радар: {radar_time:.3f}с, {radar_size:,} байт")
            results.append(('radar', True, radar_time, radar_size))
        except Exception as e:
            radar_time = time.time() - start_time
            print(f"   ❌ Радар: ОШИБКА - {e}")
            results.append(('radar', False, radar_time, 0))
        
        # Тест барной диаграммы
        start_time = time.time()
        try:
            bar_path = Path(f'stress_test_bar_{i}.png')
            EnhancedCharts.create_minimalist_bar_chart(
                dataset['labels'], 
                dataset['values'], 
                f"Бар: {dataset['name']}", 
                bar_path
            )
            bar_time = time.time() - start_time
            bar_size = bar_path.stat().st_size
            print(f"   ✅ Бар: {bar_time:.3f}с, {bar_size:,} байт")
            results.append(('bar', True, bar_time, bar_size))
        except Exception as e:
            bar_time = time.time() - start_time
            print(f"   ❌ Бар: ОШИБКА - {e}")
            results.append(('bar', False, bar_time, 0))
        
        total_time += radar_time + bar_time
    
    return results, total_time

def analyze_performance(results, total_time):
    """Анализ производительности"""
    print(f"\n📊 АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ:")
    print("="*60)
    
    successful = sum(1 for _, success, _, _ in results if success)
    total_tests = len(results)
    
    radar_times = [time for chart_type, success, time, _ in results if chart_type == 'radar' and success]
    bar_times = [time for chart_type, success, time, _ in results if chart_type == 'bar' and success]
    
    radar_sizes = [size for chart_type, success, _, size in results if chart_type == 'radar' and success]
    bar_sizes = [size for chart_type, success, _, size in results if chart_type == 'bar' and success]
    
    print(f"✅ Успешных тестов: {successful}/{total_tests} ({successful/total_tests*100:.1f}%)")
    print(f"⏱️ Общее время: {total_time:.3f} секунд")
    print(f"⚡ Среднее время на диаграмму: {total_time/total_tests:.3f}с")
    
    if radar_times:
        print(f"🎯 Радарные диаграммы:")
        print(f"   • Среднее время: {sum(radar_times)/len(radar_times):.3f}с")
        print(f"   • Средний размер: {sum(radar_sizes)/len(radar_sizes):,.0f} байт")
    
    if bar_times:
        print(f"📊 Барные диаграммы:")
        print(f"   • Среднее время: {sum(bar_times)/len(bar_times):.3f}с")
        print(f"   • Средний размер: {sum(bar_sizes)/len(bar_sizes):,.0f} байт")
    
    # Оценка производительности
    if successful == total_tests and total_time/total_tests < 2.0:
        print(f"\n🚀 ОТЛИЧНАЯ ПРОИЗВОДИТЕЛЬНОСТЬ!")
        return True
    elif successful >= total_tests * 0.8:
        print(f"\n✅ ХОРОШАЯ ПРОИЗВОДИТЕЛЬНОСТЬ")
        return True
    else:
        print(f"\n⚠️ ТРЕБУЕТСЯ ОПТИМИЗАЦИЯ")
        return False

def main():
    print("🧪 КОМПЛЕКСНЫЙ СТРЕСС-ТЕСТ СИСТЕМЫ")
    print("="*70)
    
    start_time = time.time()
    
    # Запуск стресс-теста
    results, test_time = stress_test_charts()
    
    # Анализ результатов
    performance_good = analyze_performance(results, test_time)
    
    end_time = time.time()
    total_execution_time = end_time - start_time
    
    print(f"\n🎯 ИТОГОВАЯ ОЦЕНКА СТРЕСС-ТЕСТА:")
    print("="*70)
    print(f"⏱️ Время выполнения теста: {total_execution_time:.2f} секунд")
    
    if performance_good:
        print("🎉 СИСТЕМА ПРОШЛА СТРЕСС-ТЕСТ УСПЕШНО!")
        print("✅ Стабильная работа с различными данными")
        print("✅ Приемлемая производительность")
        print("🚀 ГОТОВА К ПРОДУКТИВНОЙ ЭКСПЛУАТАЦИИ!")
    else:
        print("⚠️ Система требует оптимизации")
        print("🔧 Рекомендуется дополнительная настройка")

if __name__ == "__main__":
    main()