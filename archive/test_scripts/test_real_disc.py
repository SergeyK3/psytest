#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрый тест DISC интерпретации - создание только DISC отчёта
"""

from interpretation_utils import generate_interpretations_from_prompt

# Тестовые данные DISC - точно такие же как в реальном тесте
paei_scores = {'P': 1, 'A': 1, 'E': 0, 'I': 3}
disc_scores = {'D': 4.0, 'I': 3.0, 'S': 2.5, 'C': 3.5}  # из логов последнего теста
hexaco_scores = {'H': 4, 'E': 1, 'X': 3, 'A': 2, 'C': 5, 'O': 3}  
soft_skills_scores = [4, 4, 4, 4, 4, 4, 3, 4, 4, 3]

print("🎯 Тестируем РЕАЛЬНЫЕ данные из последнего прогона бота:")
print(f"📊 DISC баллы: {disc_scores}")

# Генерируем интерпретации
interpretations = generate_interpretations_from_prompt(paei_scores, disc_scores, hexaco_scores, soft_skills_scores)

print("\n📝 РЕАЛЬНАЯ DISC интерпретация которая попадёт в PDF:")
print("=" * 60)
print(interpretations.get('disc', 'НЕТ ДАННЫХ'))
print("=" * 60)

# Проверяем наличие ключевых фраз из старого отчёта
key_phrases = [
    "Сумма баллов по доминированию",
    "Сумма баллов по влиянию", 
    "Сумма баллов по устойчивости",
    "Сумма баллов по подчинению правилам",
    "Общий вывод"
]

print("\n🔍 Проверка ключевых фраз:")
disc_text = interpretations.get('disc', '')
for phrase in key_phrases:
    if phrase in disc_text:
        print(f"✅ Найдено: '{phrase}'")
    else:
        print(f"❌ НЕ найдено: '{phrase}'")

print(f"\n📏 Общая длина DISC интерпретации: {len(disc_text)} символов")
if len(disc_text) > 100:
    print("✅ Интерпретация не пустая - исправление работает!")
else:
    print("❌ Интерпретация слишком короткая или пустая")