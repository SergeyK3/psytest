#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Анализ и исправление проблем с пропорциональностью диаграмм
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from src.psytest.charts import make_radar, make_bar_chart

def analyze_diagram_issues():
    """Анализируем потенциальные проблемы с диаграммами"""
    print("🔍 АНАЛИЗ ПРОБЛЕМ С ДИАГРАММАМИ")
    print("=" * 50)
    
    # Создаем тестовые папки
    test_dir = Path("test_charts_analysis")
    test_dir.mkdir(exist_ok=True)
    
    # Проблемные данные из ваших примеров
    test_cases = [
        {
            "name": "PAEI - Несбалансированный (A доминирует)",
            "type": "paei",
            "labels": ["P", "A", "E", "I"],
            "values": [1.0, 10.0, 1.0, 1.0],
            "issues": ["Крайне несбалансированные значения", "Один параметр в 10 раз больше других"]
        },
        {
            "name": "DISC - Доминирующий D",
            "type": "disc", 
            "labels": ["D", "I", "S", "C"],
            "values": [7.8, 1.0, 3.2, 1.0],
            "issues": ["D сильно доминирует", "Большая разница между максимумом и минимумом"]
        },
        {
            "name": "DISC - Сбалансированный",
            "type": "disc",
            "labels": ["D", "I", "S", "C"], 
            "values": [6.0, 7.0, 5.0, 6.0],
            "issues": ["Хорошо сбалансированный профиль"]
        },
        {
            "name": "PAEI - Сбалансированный",
            "type": "paei",
            "labels": ["P", "A", "E", "I"],
            "values": [6.0, 7.0, 5.0, 6.0], 
            "issues": ["Хорошо сбалансированный профиль"]
        }
    ]
    
    problems_found = []
    
    for i, case in enumerate(test_cases):
        print(f"\n📊 Анализ: {case['name']}")
        print(f"Значения: {case['values']}")
        print(f"Проблемы: {', '.join(case['issues'])}")
        
        # Создаем диаграммы
        radar_path = test_dir / f"radar_{i+1}_{case['type']}.png"
        bar_path = test_dir / f"bar_{i+1}_{case['type']}.png"
        
        try:
            # Радарная диаграмма
            make_radar(case['labels'], case['values'], radar_path, 
                      title=f"{case['name']} (Радар)", max_value=10)
            
            # Столбчатая диаграмма
            make_bar_chart(case['labels'], case['values'], bar_path,
                          title=f"{case['name']} (Столбцы)", max_value=10)
            
            print(f"✅ Диаграммы созданы: {radar_path.name}, {bar_path.name}")
            
            # Анализ пропорций
            max_val = max(case['values'])
            min_val = min(case['values'])
            ratio = max_val / min_val if min_val > 0 else float('inf')
            
            print(f"📏 Соотношение макс/мин: {ratio:.1f}")
            
            if ratio > 5:
                problem = f"Высокое соотношение {ratio:.1f}:1 может создавать визуальный дисбаланс"
                problems_found.append({
                    "case": case['name'],
                    "problem": problem,
                    "ratio": ratio,
                    "suggestion": "Логарифмическое масштабирование или нормализация"
                })
                print(f"⚠️  {problem}")
            
            if max_val == 10.0 and min_val == 1.0:
                problem = "Использование крайних значений шкалы (1 и 10)"
                problems_found.append({
                    "case": case['name'], 
                    "problem": problem,
                    "suggestion": "Пересмотреть алгоритм подсчета баллов"
                })
                print(f"⚠️  {problem}")
                
        except Exception as e:
            print(f"❌ Ошибка создания диаграмм: {e}")
    
    # Выводим общий анализ
    print(f"\n📋 ОБЩИЙ АНАЛИЗ ПРОБЛЕМ:")
    print(f"Всего проблем найдено: {len(problems_found)}")
    
    for problem in problems_found:
        print(f"\n🔸 {problem['case']}")
        print(f"  Проблема: {problem['problem']}")
        print(f"  Рекомендация: {problem['suggestion']}")
    
    return problems_found, test_dir

def suggest_improvements():
    """Предлагаем улучшения для диаграмм"""
    print(f"\n💡 РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ:")
    print("=" * 50)
    
    suggestions = [
        {
            "issue": "Крайние значения (1 и 10)",
            "solutions": [
                "Использовать более мягкие пределы (2-8)",
                "Нормализация к среднему значению",
                "Адаптивное масштабирование по данным"
            ]
        },
        {
            "issue": "Высокие соотношения (>5:1)",
            "solutions": [
                "Логарифмическое масштабирование",
                "Квадратный корень из значений",
                "Процентильная нормализация"
            ]
        },
        {
            "issue": "Визуальный дисбаланс",
            "solutions": [
                "Изменить цветовую схему",
                "Добавить фоновые концентрические круги",
                "Улучшить пропорции осей"
            ]
        },
        {
            "issue": "Радарные диаграммы",
            "solutions": [
                "Фиксированные максимальные значения для каждого теста",
                "Равномерное распределение осей",
                "Улучшенная читаемость меток"
            ]
        }
    ]
    
    for suggestion in suggestions:
        print(f"\n🎯 {suggestion['issue']}:")
        for i, solution in enumerate(suggestion['solutions'], 1):
            print(f"  {i}. {solution}")
    
    return suggestions

if __name__ == "__main__":
    print("🔧 АНАЛИЗ ПРОБЛЕМ С ПРОПОРЦИОНАЛЬНОСТЬЮ ДИАГРАММ")
    print("=" * 70)
    
    try:
        problems, test_dir = analyze_diagram_issues()
        suggestions = suggest_improvements()
        
        print(f"\n📁 Тестовые диаграммы сохранены в: {test_dir}")
        print(f"\n🎉 Анализ завершен! Найдено {len(problems)} проблем.")
        print("Изучите созданные диаграммы для визуального анализа.")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()