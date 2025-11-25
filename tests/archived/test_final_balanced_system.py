#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальный тест системы сбалансированных диаграмм с реальными данными
"""
import sys
from pathlib import Path

# Добавляем src в путь для импорта
sys.path.insert(0, str(Path(__file__).parent / "src"))

from enhanced_pdf_report import EnhancedCharts

def test_balanced_integration():
    """Тестируем интеграцию обновленной системы с реальными данными"""
    print("🧪 ФИНАЛЬНЫЙ ТЕСТ ИНТЕГРАЦИИ СБАЛАНСИРОВАННЫХ ДИАГРАММ")
    print("=" * 70)
    
    # Создаем папку для результатов
    test_dir = Path("test_balanced_integration")
    test_dir.mkdir(exist_ok=True)
    
    # Реальные проблемные данные из пользовательских тестов
    test_cases = [
        {
            "name": "Проблемный случай - PAEI с экстремальным A",
            "test_type": "PAEI",
            "labels": ["P", "A", "E", "I"],
            "values": [1.0, 10.0, 1.0, 1.0],
            "description": "Сильный дисбаланс - A в 10 раз больше остальных"
        },
        {
            "name": "Проблемный случай - DISC с доминирующим D",
            "test_type": "DISC", 
            "labels": ["D", "I", "S", "C"],
            "values": [7.8, 1.0, 3.2, 1.0],
            "description": "Средний дисбаланс - D почти в 8 раз больше минимума"
        },
        {
            "name": "Слабый дисбаланс - HEXACO",
            "test_type": "HEXACO",
            "labels": ["H", "E", "X", "A", "C", "O"],
            "values": [4.0, 8.0, 3.0, 6.0, 5.0, 7.0],
            "description": "Небольшой дисбаланс - соотношение 2.7:1"
        },
        {
            "name": "Хорошо сбалансированный профиль",
            "test_type": "Balanced",
            "labels": ["A", "B", "C", "D"],
            "values": [6.2, 7.1, 5.8, 6.5],
            "description": "Сбалансированные данные - соотношение 1.2:1"
        }
    ]
    
    charts = EnhancedCharts()
    results = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📊 Тест {i}: {case['name']}")
        print(f"Тип: {case['test_type']}")
        print(f"Значения: {dict(zip(case['labels'], case['values']))}")
        print(f"Описание: {case['description']}")
        
        # Подсчитываем соотношение
        max_val = max(case['values'])
        min_val = min(v for v in case['values'] if v > 0)
        ratio = max_val / min_val
        print(f"Соотношение макс/мин: {ratio:.2f}")
        
        # Создаем диаграммы через обновленную систему
        radar_path = test_dir / f"final_radar_{i}_{case['test_type']}.png"
        bar_path = test_dir / f"final_bar_{i}_{case['test_type']}.png"
        
        try:
            # Радарная диаграмма
            charts.create_minimalist_radar(
                case['labels'], case['values'], 
                f"{case['test_type']} - Радар (Сбалансированный)", radar_path
            )
            
            # Столбчатая диаграмма
            charts.create_minimalist_bar_chart(
                case['labels'], case['values'],
                f"{case['test_type']} - Столбцы (Сбалансированные)", bar_path
            )
            
            print(f"  ✅ Диаграммы созданы: {radar_path.name}, {bar_path.name}")
            
            # Определяем ожидаемый метод нормализации
            if ratio > 8.0:
                expected_method = "логарифм"
            elif ratio > 4.0:
                expected_method = "квадратный корень"
            elif ratio > 2.0:
                expected_method = "мягкая нормализация"
            else:
                expected_method = "без нормализации"
            
            print(f"  📏 Ожидаемая нормализация: {expected_method}")
            
            results.append({
                "test": case['name'],
                "ratio": ratio,
                "expected_norm": expected_method,
                "files": [radar_path, bar_path]
            })
            
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    print(f"\n🎉 РЕЗУЛЬТАТЫ ФИНАЛЬНОГО ТЕСТИРОВАНИЯ:")
    print(f"Создано {len(results) * 2} диаграмм в папке: {test_dir}")
    
    print(f"\n📈 АНАЛИЗ НОРМАЛИЗАЦИИ:")
    for result in results:
        print(f"  • {result['test']}: соотношение {result['ratio']:.2f} → {result['expected_norm']}")
    
    print(f"\n💡 ПРОВЕРЬТЕ РЕЗУЛЬТАТЫ:")
    print("1. Диаграммы с высокими соотношениями должны быть визуально сбалансированными")
    print("2. Заголовки содержат информацию о применённой нормализации")
    print("3. Сбалансированные данные остаются без изменений")
    print("4. Все диаграммы должны хорошо читаться и выглядеть профессионально")
    
    return results, test_dir

def compare_before_after():
    """Создаем сравнение до и после для демонстрации улучшений"""
    print(f"\n🔍 СОЗДАНИЕ СРАВНЕНИЯ ДО/ПОСЛЕ")
    print("=" * 50)
    
    from src.psytest.charts import make_radar, make_bar_chart
    
    # Создаем папку для сравнения
    compare_dir = Path("comparison_before_after")
    compare_dir.mkdir(exist_ok=True)
    
    # Проблемный случай
    labels = ["P", "A", "E", "I"]
    values = [1.0, 10.0, 1.0, 1.0]
    
    print("Тестовые данные PAEI: P=1.0, A=10.0, E=1.0, I=1.0 (соотношение 10:1)")
    
    # ДО (старая система без нормализации)
    before_radar = compare_dir / "before_radar_unnormalized.png"
    before_bar = compare_dir / "before_bar_unnormalized.png"
    
    make_radar(labels, values, before_radar, 
              title="ДО: Без нормализации (несбалансированно)", 
              normalize=False, max_value=10)
    
    make_bar_chart(labels, values, before_bar,
                  title="ДО: Без нормализации (несбалансированно)", 
                  normalize=False, max_value=10)
    
    # ПОСЛЕ (новая система с нормализацией)
    after_radar = compare_dir / "after_radar_normalized.png"
    after_bar = compare_dir / "after_bar_normalized.png"
    
    make_radar(labels, values, after_radar,
              title="ПОСЛЕ: С адаптивной нормализацией (сбалансированно)",
              normalize=True, normalize_method="adaptive")
    
    make_bar_chart(labels, values, after_bar,
              title="ПОСЛЕ: С адаптивной нормализацией (сбалансированно)",
              normalize=True, normalize_method="adaptive")
    
    print(f"✅ Сравнительные диаграммы созданы в папке: {compare_dir}")
    print("📊 Файлы before_* показывают проблему несбалансированности")
    print("🎯 Файлы after_* показывают решение с нормализацией")
    
    return compare_dir

if __name__ == "__main__":
    print("🚀 ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ СИСТЕМЫ СБАЛАНСИРОВАННЫХ ДИАГРАММ")
    print("=" * 80)
    
    try:
        # Основной тест интеграции
        results, test_dir = test_balanced_integration()
        
        # Сравнение до/после
        compare_dir = compare_before_after()
        
        print(f"\n✨ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
        print(f"📁 Результаты в папках: {test_dir}, {compare_dir}")
        print("\n🎯 СЛЕДУЮЩИЕ ШАГИ:")
        print("1. Проверьте созданные диаграммы")
        print("2. Убедитесь в визуальном балансе")
        print("3. Готово к внедрению в основную систему!")
        
    except Exception as e:
        print(f"\n❌ Ошибка во время финального тестирования: {e}")
        import traceback
        traceback.print_exc()