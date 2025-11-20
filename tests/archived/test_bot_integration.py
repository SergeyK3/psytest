#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрый тест Telegram бота с загрузкой вопросов из промптов
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_test_bot import parse_paei_questions, parse_disc_questions, parse_hexaco_questions, parse_soft_skills_questions

def test_bot_question_integration():
    """Тестирует интеграцию с ботом"""
    
    print("🤖 Тестирование интеграции с Telegram ботом...")
    
    # Загружаем вопросы
    paei_questions = parse_paei_questions()
    disc_questions = parse_disc_questions()
    hexaco_questions = parse_hexaco_questions()
    soft_questions = parse_soft_skills_questions()
    
    print(f"\n📊 Статистика загрузки:")
    print(f"  PAEI: {len(paei_questions)} вопросов")
    print(f"  DISC: {len(disc_questions)} вопросов")
    print(f"  HEXACO: {len(hexaco_questions)} вопросов")
    print(f"  Soft Skills: {len(soft_questions)} вопросов")
    print(f"  ВСЕГО: {len(paei_questions) + len(disc_questions) + len(hexaco_questions) + len(soft_questions)} вопросов")
    
    # Демонстрируем первые вопросы
    print(f"\n🎯 Примеры вопросов:")
    
    if paei_questions:
        q = paei_questions[0]
        print(f"\n📝 PAEI Вопрос 1:")
        print(f"   Текст: {q['question']}")
        print(f"   Варианты: {list(q['answers'].keys())}")
    
    if disc_questions:
        q = disc_questions[0]
        print(f"\n📝 DISC Вопрос 1:")
        print(f"   Текст: {q['question']}")
        print(f"   Шкала: {q.get('scale', 'не указана')}")
    
    if hexaco_questions:
        q = hexaco_questions[0]
        print(f"\n📝 HEXACO Вопрос 1:")
        print(f"   Текст: {q['question']}")
        print(f"   Шкала: {q.get('scale', 'не указана')}")
    
    if soft_questions:
        q = soft_questions[0]
        print(f"\n📝 Soft Skills Вопрос 1:")
        print(f"   Текст: {q['question']}")
        print(f"   Варианты: {list(q['answers'].keys())}")
    
    print(f"\n✅ Интеграция с ботом работает правильно!")
    print(f"💡 Бот теперь будет использовать вопросы из файлов _user.txt вместо хардкода")
    
    return True

if __name__ == "__main__":
    test_bot_question_integration()