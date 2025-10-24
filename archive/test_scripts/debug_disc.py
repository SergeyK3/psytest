#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Отладка DISC интерпретации
"""

from interpretation_utils import generate_interpretations_from_prompt
from interpretation_formatter import format_ai_interpretations, parse_disc_sections

# Тестовые данные как в боте
paei_scores = {'P': 1, 'A': 1, 'E': 0, 'I': 3}
disc_scores = {'D': 4.0, 'I': 3.0, 'S': 2.5, 'C': 4.0}
hexaco_scores = {'H': 4, 'E': 1, 'X': 3, 'A': 2, 'C': 5, 'O': 3}
soft_skills_scores = [4, 4, 4, 4, 4, 4, 3, 4, 4, 3]

print("🔍 Тестируем генерацию DISC интерпретации...")
print(f"📊 DISC баллы: {disc_scores}")

# Генерируем интерпретации
interpretations = generate_interpretations_from_prompt(paei_scores, disc_scores, hexaco_scores, soft_skills_scores)

print("\n📝 Сырая DISC интерпретация:")
print("=" * 50)
print(interpretations.get('disc', 'НЕТ ДАННЫХ'))

print("\n🎨 Форматированная интерпретация:")
print("=" * 50)
formatted = format_ai_interpretations(interpretations)
print(formatted.get('disc', 'НЕТ ДАННЫХ'))

print("\n🔍 Секции DISC:")
print("=" * 50)
if 'disc' in formatted:
    sections = parse_disc_sections(formatted['disc'])
    for key, value in sections.items():
        print(f"'{key}':")
        print(f"  {value[:100]}...")
        print()
else:
    print("НЕТ DISC В ФОРМАТИРОВАННЫХ ДАННЫХ")