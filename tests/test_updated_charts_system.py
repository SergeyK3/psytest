#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование обновленной системы сбалансированных диаграмм
"""
import sys
from pathlib import Path

# Добавляем src в путь для импорта
sys.path.insert(0, str(Path(__file__).parent / "src"))

from psytest.charts import make_radar, make_bar_chart

def test_updated_charts():
    """Тестируем обновленную систему диаграмм"""
    print("🎨 ТЕСТИРОВАНИЕ ОБНОВЛЕННОЙ СИСТЕМЫ ДИАГРАММ")
    print("=" * 60)
    
    # Создаем папку для результатов
    test_dir = Path("test_updated_charts")
    test_dir.mkdir(exist_ok=True)
    
    # Тестовые случаи с проблемными данными
    test_cases = [
        {
            "name": "PAEI - Экстремальный A",
            "labels": ["P", "A", "E", "I"],
            "values": [1.0, 10.0, 1.0, 1.0],
            "type": "PAEI"
        },
        {
            "name": "DISC - Доминирующий D",
            "labels": ["D", "I", "S", "C"],
            "values": [7.8, 1.0, 3.2, 1.0],
            "type": "DISC"
        },
        {
            "name": "Сбалансированный профиль",
            "labels": ["A", "B", "C", "D"],
            "values": [6.0, 7.0, 5.0, 6.0],
            "type": "Balanced"
        },
        {
            "name": "Средний дисбаланс", 
            "labels": ["X", "Y", "Z", "W"],
            "values": [2.0, 8.0, 3.0, 4.0],
            "type": "Medium"
        }
    ]
    
    results = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📊 Тест {i}: {case['name']}")
        print(f"Значения: {case['values']}")
        
        # Тестируем с нормализацией (по умолчанию)
        radar_norm = test_dir / f"radar_{i}_normalized.png"
        bar_norm = test_dir / f"bar_{i}_normalized.png"
        
        make_radar(case['labels'], case['values'], radar_norm, 
                  title=f"{case['name']} - Радар (Норм)", normalize=True)
        
        make_bar_chart(case['labels'], case['values'], bar_norm,
                      title=f"{case['name']} - Столбцы (Норм)", normalize=True)
        
        # Тестируем без нормализации для сравнения
        radar_orig = test_dir / f"radar_{i}_original.png"
        bar_orig = test_dir / f"bar_{i}_original.png"
        
        make_radar(case['labels'], case['values'], radar_orig,
                  title=f"{case['name']} - Радар (Ориг)", normalize=False, max_value=10)
        
        make_bar_chart(case['labels'], case['values'], bar_orig,
                      title=f"{case['name']} - Столбцы (Ориг)", normalize=False, max_value=10)
        
        print(f"  ✅ Создано: {radar_norm.name}, {bar_norm.name}")
        print(f"  ✅ Для сравнения: {radar_orig.name}, {bar_orig.name}")
        
        results.append({
            "case": case['name'],
            "values": case['values'],
            "normalized": [radar_norm, bar_norm],
            "original": [radar_orig, bar_orig]
        })
    
    print(f"\n🎉 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"Создано {len(results) * 4} диаграмм в папке: {test_dir}")
    print("\n💡 СРАВНИТЕ РЕЗУЛЬТАТЫ:")
    print("- *_normalized.png - С автоматической нормализацией (сбалансированные)")
    print("- *_original.png - Исходные данные (могут быть несбалансированными)")
    print("\nНормализованные диаграммы должны быть визуально более сбалансированными!")
    
    return results

def test_normalization_methods():
    """Тестируем разные методы нормализации"""
    print(f"\n🔬 ТЕСТИРОВАНИЕ МЕТОДОВ НОРМАЛИЗАЦИИ")
    print("=" * 60)
    
    # Создаем папку для результатов
    methods_dir = Path("test_normalization_methods")
    methods_dir.mkdir(exist_ok=True)
    
    # Проблемный случай
    labels = ["P", "A", "E", "I"]
    values = [1.0, 10.0, 1.0, 1.0]
    methods = ["adaptive", "sqrt", "log", "minmax", "none"]
    
    print(f"Тестовые данные: {dict(zip(labels, values))}")
    
    for method in methods:
        print(f"\n🔧 Метод: {method}")
        
        radar_path = methods_dir / f"radar_method_{method}.png"
        bar_path = methods_dir / f"bar_method_{method}.png"
        
        if method == "none":
            make_radar(labels, values, radar_path,
                      title=f"Радар - {method}", normalize=False, max_value=10)
            make_bar_chart(labels, values, bar_path,
                          title=f"Столбцы - {method}", normalize=False, max_value=10)
        else:
            make_radar(labels, values, radar_path,
                      title=f"Радар - {method}", normalize=True, normalize_method=method)
            make_bar_chart(labels, values, bar_path,
                          title=f"Столбцы - {method}", normalize=True, normalize_method=method)
        
        print(f"  ✅ Создано: {radar_path.name}, {bar_path.name}")
    
    print(f"\n📁 Результаты в папке: {methods_dir}")
    print("Сравните визуальный баланс разных методов!")

if __name__ == "__main__":
    print("🚀 ТЕСТИРОВАНИЕ ОБНОВЛЕННОЙ СИСТЕМЫ ДИАГРАММ")
    print("=" * 70)
    
    try:
        # Основные тесты
        test_updated_charts()
        
        # Тесты методов нормализации
        test_normalization_methods()
        
        print(f"\n✨ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
        print("Проверьте созданные диаграммы - они должны быть более сбалансированными!")
        
    except Exception as e:
        print(f"\n❌ Ошибка во время тестирования: {e}")
        import traceback
        traceback.print_exc()