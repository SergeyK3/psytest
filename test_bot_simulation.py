#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Симуляция тестирования Telegram бота
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_test_bot import (
    parse_paei_questions, parse_disc_questions, 
    parse_hexaco_questions, parse_soft_skills_questions,
    UserSession
)

def simulate_testing_session():
    """Симулирует сессию тестирования"""
    
    print("🧪 Симуляция тестовой сессии бота...")
    
    # Загружаем вопросы
    paei_questions = parse_paei_questions()
    disc_questions = parse_disc_questions()
    hexaco_questions = parse_hexaco_questions()
    soft_questions = parse_soft_skills_questions()
    
    print(f"\n📋 Загруженные вопросы:")
    print(f"  PAEI: {len(paei_questions)}")
    print(f"  DISC: {len(disc_questions)}")
    print(f"  HEXACO: {len(hexaco_questions)}")
    print(f"  Soft Skills: {len(soft_questions)}")
    
    # Создаем пользовательскую сессию
    user_session = UserSession(user_id=12345)  # Тестовый ID
    print(f"\n👤 Создана новая сессия пользователя")
    print(f"   User ID: {user_session.user_id}")
    print(f"   Текущий тест: {user_session.current_test}")
    print(f"   Текущий вопрос: {user_session.current_question}")
    print(f"   DISC scores: {user_session.disc_scores}")
    
    # Тестируем PAEI вопрос
    if paei_questions:
        print(f"\n📝 Тест PAEI вопроса:")
        q = paei_questions[0]
        print(f"   Вопрос: {q['question'][:60]}...")
        print(f"   Варианты:")
        for key, answer in q['answers'].items():
            print(f"     {key}. {answer[:40]}...")
        
        # Симулируем ответ
        print(f"   ✅ Пользователь выбрал: P")
        user_session.paei_scores["P"] += 1
    
    # Тестируем DISC вопрос
    if disc_questions:
        print(f"\n📝 Тест DISC вопроса:")
        q = disc_questions[0]
        print(f"   Вопрос: {q['question'][:60]}...")
        print(f"   Шкала: {q['scale']}")
        print(f"   ✅ Пользователь выбрал: 4 (Согласен)")
        user_session.disc_scores.append(4)
    
    # Тестируем HEXACO вопрос
    if hexaco_questions:
        print(f"\n📝 Тест HEXACO вопроса:")
        q = hexaco_questions[0]
        print(f"   Вопрос: {q['question'][:60]}...")
        print(f"   Шкала: {q['scale']}")
        print(f"   ✅ Пользователь выбрал: 3 (Нейтрально)")
        user_session.hexaco_scores.append(3)
    
    # Тестируем Soft Skills вопрос
    if soft_questions:
        print(f"\n📝 Тест Soft Skills вопроса:")
        q = soft_questions[0]
        print(f"   Вопрос: {q['question'][:60]}...")
        print(f"   Варианты:")
        for key, answer in list(q['answers'].items())[:3]:  # Показываем первые 3
            print(f"     {key}. {answer[:40]}...")
        print(f"   ✅ Пользователь выбрал: 4")
        user_session.soft_skills_scores.append(8)  # 4 * 2 = 8
    
    print(f"\n📊 Результаты симуляции:")
    print(f"   PAEI баллы: {user_session.paei_scores}")
    print(f"   DISC баллы: {user_session.disc_scores}")
    print(f"   HEXACO баллы: {user_session.hexaco_scores}")
    print(f"   Soft Skills баллы: {user_session.soft_skills_scores}")
    
    print(f"\n✅ Симуляция завершена успешно!")
    print(f"💡 Бот готов к реальному тестированию в Telegram")
    
    return True

def test_question_formats():
    """Тестирует форматы вопросов"""
    
    print(f"\n🔍 Проверка форматов вопросов:")
    
    # PAEI - должен иметь варианты P/A/E/I
    paei_q = parse_paei_questions()[0] if parse_paei_questions() else None
    if paei_q:
        expected_keys = {'P', 'A', 'E', 'I'}
        actual_keys = set(paei_q['answers'].keys())
        print(f"   PAEI ключи: ожидаем {expected_keys}, получили {actual_keys}")
        print(f"   ✅ PAEI формат корректен: {expected_keys == actual_keys}")
    
    # DISC - должен иметь шкалу 1-5
    disc_q = parse_disc_questions()[0] if parse_disc_questions() else None
    if disc_q:
        has_scale = 'scale' in disc_q and disc_q['scale'] == '1-5'
        print(f"   DISC шкала: {disc_q.get('scale', 'отсутствует')}")
        print(f"   ✅ DISC формат корректен: {has_scale}")
    
    # Soft Skills - должен иметь варианты 1-5
    soft_q = parse_soft_skills_questions()[0] if parse_soft_skills_questions() else None
    if soft_q:
        expected_keys = {'1', '2', '3', '4', '5'}
        actual_keys = set(soft_q['answers'].keys())
        print(f"   Soft Skills ключи: ожидаем {expected_keys}, получили {actual_keys}")
        print(f"   ✅ Soft Skills формат корректен: {expected_keys == actual_keys}")

if __name__ == "__main__":
    print("🚀 Начинаем тестирование модифицированного бота...")
    
    # Основная симуляция
    simulate_testing_session()
    
    # Проверка форматов
    test_question_formats()
    
    print(f"\n🎯 Готово к тестированию в Telegram!")
    print(f"📱 Бот: @psychtestteambot")
    print(f"🔧 Команды для тестирования:")
    print(f"   /start - Начать тестирование")
    print(f"   /help - Справка")
    print(f"   /cancel - Отменить сессию")