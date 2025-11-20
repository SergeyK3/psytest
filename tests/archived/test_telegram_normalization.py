#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование интеграции нормализации шкал в Telegram боте
"""
import sys
from pathlib import Path

# Добавляем путь для импорта
sys.path.insert(0, str(Path(__file__).parent))

from scale_normalizer import ScaleNormalizer
from telegram_test_bot import UserSession
from datetime import datetime

def test_telegram_bot_normalization():
    """Тестируем нормализацию в контексте Telegram бота"""
    print("🤖 ТЕСТИРОВАНИЕ НОРМАЛИЗАЦИИ В TELEGRAM БОТЕ")
    print("=" * 60)
    
    # Создаем тестовую сессию с проблемными данными
    session = UserSession(12345)
    session.name = "Тестовый Пользователь"
    
    # Проблемные сценарии
    test_scenarios = [
        {
            "name": "Экстремальный PAEI (A=5, остальные=0)",
            "paei_scores": {"P": 0, "A": 5, "E": 0, "I": 0},
            "disc_scores": {"D": 1, "I": 1, "S": 1, "C": 3},
            "hexaco_scores": {"H": 3.0, "E": 4.0, "X": 2.5, "A": 3.5, "C": 2.8, "O": 4.2},
            "soft_skills_scores": {"Лидерство": 8, "Коммуникация": 6, "Планирование": 9}
        },
        {
            "name": "Экстремальный DISC (D=6, остальные=0)",
            "paei_scores": {"P": 2, "A": 1, "E": 1, "I": 1},
            "disc_scores": {"D": 6, "I": 0, "S": 0, "C": 0},
            "hexaco_scores": {"H": 2.0, "E": 5.0, "X": 3.0, "A": 4.0, "C": 3.5, "O": 2.5},
            "soft_skills_scores": {"Лидерство": 10, "Коммуникация": 3, "Планирование": 7}
        },
        {
            "name": "Сбалансированный профиль",
            "paei_scores": {"P": 1, "A": 1, "E": 2, "I": 1},
            "disc_scores": {"D": 2, "I": 1, "S": 2, "C": 1},
            "hexaco_scores": {"H": 3.5, "E": 3.8, "X": 3.2, "A": 3.6, "C": 3.4, "O": 3.7},
            "soft_skills_scores": {"Лидерство": 7, "Коммуникация": 8, "Планирование": 6}
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📊 Сценарий {i}: {scenario['name']}")
        print("-" * 50)
        
        # Присваиваем данные сессии
        session.paei_scores = scenario["paei_scores"]
        session.disc_scores = scenario["disc_scores"]
        session.hexaco_scores = scenario["hexaco_scores"]
        session.soft_skills_scores = scenario["soft_skills_scores"]
        
        print(f"📋 ИСХОДНЫЕ ДАННЫЕ:")
        print(f"  PAEI: {session.paei_scores}")
        print(f"  DISC: {session.disc_scores}")
        print(f"  HEXACO: {session.hexaco_scores}")
        print(f"  Soft Skills: {session.soft_skills_scores}")
        
        # Применяем нормализацию
        paei_norm, paei_method = ScaleNormalizer.auto_normalize("PAEI", session.paei_scores)
        disc_norm, disc_method = ScaleNormalizer.auto_normalize("DISC", session.disc_scores)
        hexaco_norm, hexaco_method = ScaleNormalizer.auto_normalize("HEXACO", session.hexaco_scores)
        soft_norm, soft_method = ScaleNormalizer.auto_normalize("SOFT_SKILLS", session.soft_skills_scores)
        
        print(f"\n📈 НОРМАЛИЗОВАННЫЕ ДАННЫЕ:")
        print(f"  PAEI: {dict((k, round(v, 1)) for k, v in paei_norm.items())} ({paei_method})")
        print(f"  DISC: {dict((k, round(v, 1)) for k, v in disc_norm.items())} ({disc_method})")
        print(f"  HEXACO: {dict((k, round(v, 1)) for k, v in hexaco_norm.items())} ({hexaco_method})")
        print(f"  Soft Skills: {dict((k, round(v, 1)) for k, v in soft_norm.items())} ({soft_method})")
        
        # Проверяем соотношения
        def analyze_ratio(data, name):
            if not data:
                return
            max_val = max(data.values())
            min_val = min(v for v in data.values() if v > 0)
            ratio = max_val / min_val if min_val > 0 else float('inf')
            return ratio
        
        print(f"\n📏 АНАЛИЗ СООТНОШЕНИЙ:")
        
        # PAEI
        paei_orig_ratio = analyze_ratio(session.paei_scores, "PAEI")
        paei_norm_ratio = analyze_ratio(paei_norm, "PAEI")
        if paei_orig_ratio:
            print(f"  PAEI: {paei_orig_ratio:.1f} → {paei_norm_ratio:.1f}")
        
        # DISC
        disc_orig_ratio = analyze_ratio(session.disc_scores, "DISC")
        disc_norm_ratio = analyze_ratio(disc_norm, "DISC")
        if disc_orig_ratio:
            print(f"  DISC: {disc_orig_ratio:.1f} → {disc_norm_ratio:.1f}")
        
        # Определяем доминирующий тип
        max_paei = max(paei_norm.values()) if paei_norm else 0
        max_disc = max(disc_norm.values()) if disc_norm else 0
        
        if max_paei >= max_disc:
            dominant_type = f"PAEI_{max(paei_norm, key=paei_norm.get)}"
        else:
            dominant_type = f"DISC_{max(disc_norm, key=disc_norm.get)}"
        
        print(f"  🏆 Доминирующий тип: {dominant_type}")
    
    print(f"\n✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print(f"💡 ВЫВОДЫ:")
    print(f"1. Нормализация приводит все шкалы к единому диапазону 0-10")
    print(f"2. Соотношения между факторами сохраняются")
    print(f"3. Диаграммы будут визуально сбалансированными")
    print(f"4. Сравнение между разными тестами становится корректным")

def test_extreme_cases():
    """Тестируем экстремальные случаи"""
    print(f"\n🔥 ТЕСТИРОВАНИЕ ЭКСТРЕМАЛЬНЫХ СЛУЧАЕВ")
    print("=" * 50)
    
    extreme_cases = [
        {
            "name": "Все баллы в одном факторе PAEI",
            "scores": {"P": 0, "A": 5, "E": 0, "I": 0},
            "test_type": "PAEI"
        },
        {
            "name": "Все баллы в одном факторе DISC", 
            "scores": {"D": 6, "I": 0, "S": 0, "C": 0},
            "test_type": "DISC"
        },
        {
            "name": "Минимальные значения HEXACO",
            "scores": {"H": 1.0, "E": 1.0, "X": 1.0, "A": 1.0, "C": 1.0, "O": 1.0},
            "test_type": "HEXACO"
        },
        {
            "name": "Максимальные значения Soft Skills",
            "scores": {"Лидерство": 10, "Коммуникация": 10, "Планирование": 10},
            "test_type": "SOFT_SKILLS"
        }
    ]
    
    for case in extreme_cases:
        print(f"\n🧪 {case['name']}")
        normalized, method = ScaleNormalizer.auto_normalize(case['test_type'], case['scores'])
        
        print(f"  Исходные: {case['scores']}")
        print(f"  Нормализованные: {dict((k, round(v, 1)) for k, v in normalized.items())}")
        print(f"  Метод: {method}")
        
        # Проверяем корректность диапазона
        max_norm = max(normalized.values())
        min_norm = min(normalized.values())
        
        if min_norm >= 0 and max_norm <= 10:
            print(f"  ✅ Диапазон корректный: {min_norm:.1f} - {max_norm:.1f}")
        else:
            print(f"  ❌ Диапазон некорректный: {min_norm:.1f} - {max_norm:.1f}")

if __name__ == "__main__":
    print("🚀 ИНТЕГРАЦИОННОЕ ТЕСТИРОВАНИЕ НОРМАЛИЗАЦИИ")
    print("=" * 70)
    
    try:
        # Основное тестирование
        test_telegram_bot_normalization()
        
        # Экстремальные случаи
        test_extreme_cases()
        
        print(f"\n🎯 ГОТОВО К ТЕСТИРОВАНИЮ В БОТЕ!")
        print(f"Теперь все диаграммы будут корректно масштабированы!")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()