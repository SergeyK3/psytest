#!/usr/bin/env python3
"""
Тестирование исправления расчетов по методике Адизеса
"""

import sys
from pathlib import Path

# Добавляем путь к модулям проекта
sys.path.append(str(Path(__file__).parent))

from telegram_test_bot import UserSession, UserAnswersCollector
from scale_normalizer import ScaleNormalizer

def test_paei_calculations():
    """Тестирует правильность расчетов PAEI после исправления"""
    
    print("🧮 ТЕСТ РАСЧЕТОВ АДИЗЕСА (PAEI)")
    print("=" * 50)
    
    # Создаем тестовую сессию
    session = UserSession(user_id=123)
    session.name = "Тестовый Пользователь"
    
    # Симулируем ваши ответы: P=0, A=3, E=1, I=1
    print("📝 Симуляция ответов пользователя:")
    test_answers = [
        (0, "A", "Вопрос 1: выбран A"),
        (1, "A", "Вопрос 2: выбран A"), 
        (2, "A", "Вопрос 3: выбран A"),
        (3, "E", "Вопрос 4: выбран E"),
        (4, "I", "Вопрос 5: выбран I")
    ]
    
    # Обрабатываем ответы как в реальном боте
    for q_num, answer, description in test_answers:
        session.paei_scores[answer] += 1  # Добавляем балл
        session.answers_collector.add_paei_answer(q_num, answer)
        print(f"   ✅ {description}")
    
    print(f"\n📊 Результаты подсчета (после обработки):")
    print(f"   P = {session.paei_scores['P']}")
    print(f"   A = {session.paei_scores['A']}")
    print(f"   E = {session.paei_scores['E']}")
    print(f"   I = {session.paei_scores['I']}")
    print(f"   Сумма = {sum(session.paei_scores.values())}")
    
    # Проверяем нормализацию
    print(f"\n🔄 Проверка нормализации через ScaleNormalizer:")
    normalized, method = ScaleNormalizer.auto_normalize("PAEI", session.paei_scores)
    
    print(f"   Исходные: {session.paei_scores}")
    print(f"   Нормализованные: {normalized}")
    print(f"   Метод: {method}")
    print(f"   Сумма после нормализации: {sum(normalized.values())}")
    
    # Проверка корректности
    expected = {"P": 0, "A": 3, "E": 1, "I": 1}
    expected_sum = 5
    
    print(f"\n🎯 ПРОВЕРКА КОРРЕКТНОСТИ:")
    print(f"   Ожидаем: {expected} (сумма = {expected_sum})")
    print(f"   Получили: {normalized} (сумма = {sum(normalized.values())})")
    
    is_correct = (
        normalized == expected and 
        sum(normalized.values()) == expected_sum
    )
    
    if is_correct:
        print("   ✅ ТЕСТ ПРОЙДЕН! Расчеты корректны по методике Адизеса")
    else:
        print("   ❌ ТЕСТ НЕ ПРОЙДЕН! Есть проблемы в расчетах")
    
    return is_correct

def test_various_paei_cases():
    """Тестирует различные случаи PAEI расчетов"""
    
    print(f"\n🧪 ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ:")
    print("=" * 50)
    
    test_cases = [
        {"name": "Все P", "answers": ["P", "P", "P", "P", "P"], "expected": {"P": 5, "A": 0, "E": 0, "I": 0}},
        {"name": "Сбалансированный", "answers": ["P", "A", "E", "I", "P"], "expected": {"P": 2, "A": 1, "E": 1, "I": 1}},
        {"name": "Доминирование A", "answers": ["A", "A", "A", "I", "E"], "expected": {"P": 0, "A": 3, "E": 1, "I": 1}},
    ]
    
    all_passed = True
    
    for case in test_cases:
        print(f"\n📋 Тест: {case['name']}")
        session = UserSession(user_id=123)
        session.name = "Test"
        
        # Обрабатываем ответы
        for answer in case['answers']:
            session.paei_scores[answer] += 1
        
        # Нормализуем
        normalized, method = ScaleNormalizer.auto_normalize("PAEI", session.paei_scores)
        
        # Проверяем
        is_correct = normalized == case['expected']
        status = "✅ PASS" if is_correct else "❌ FAIL"
        
        print(f"   Ответы: {case['answers']}")
        print(f"   Ожидаем: {case['expected']}")
        print(f"   Получили: {normalized}")
        print(f"   Результат: {status}")
        
        if not is_correct:
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("🎯 ПРОВЕРКА ИСПРАВЛЕНИЯ РАСЧЕТОВ ПО АДИЗЕСУ\n")
    
    # Основной тест
    main_test_passed = test_paei_calculations()
    
    # Дополнительные тесты
    additional_tests_passed = test_various_paei_cases()
    
    print(f"\n" + "=" * 50)
    print("🏆 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print(f"   Основной тест: {'✅ PASS' if main_test_passed else '❌ FAIL'}")
    print(f"   Доп. тесты: {'✅ PASS' if additional_tests_passed else '❌ FAIL'}")
    
    if main_test_passed and additional_tests_passed:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Расчеты по Адизесу исправлены!")
        print("💡 Теперь результаты соответствуют оригинальной методике:")
        print("   • 1 балл за каждый выбранный ответ")
        print("   • Сумма баллов = количество вопросов (5)")
        print("   • Без искусственного масштабирования")
    else:
        print("\n❌ Есть проблемы, требуется дополнительная проверка")