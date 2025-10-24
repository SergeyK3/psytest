#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Проверка Soft Skills форматирования
"""

from src.psytest.ai_system_integration import AiIntegration
import json

# Тестовые данные
soft_skills_scores = {
    'Коммуникация': 4.0,
    'Работа в команде': 4.0,
    'Лидерство': 4.0,
    'Критическое мышление': 4.0,
    'Управление временем': 4.0,
    'Стрессоустойчивость': 4.0,
    'Восприимчивость к критике': 3.0,
    'Адаптивность': 4.0,
    'Решение проблем': 4.0,
    'Креативность': 3.0
}

print("🎯 Тестируем AI интерпретацию Soft Skills...")
print(f"📊 Soft Skills баллы: {json.dumps(soft_skills_scores, ensure_ascii=False, indent=2)}")

try:
    ai = AiIntegration()
    result = ai.interpret_soft_skills(soft_skills_scores)
    print("\n📝 AI результат Soft Skills:")
    print("=" * 50)
    print(result)
    print("=" * 50)
    
    # Анализируем на предмет проблем с числами
    lines = result.split('\n')
    for i, line in enumerate(lines):
        if any(char.isdigit() for char in line):
            print(f"Строка {i+1} с числами: '{line}'")
            
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()