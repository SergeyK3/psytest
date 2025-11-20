#!/usr/bin/env python3
"""
Тест парсинга DISC вопросов из telegram_test_bot.py
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from telegram_test_bot import parse_disc_questions

def main():
    print("🔄 Тестируем парсинг DISC вопросов из telegram_test_bot.py...")
    
    # Парсим вопросы через функцию из бота
    questions = parse_disc_questions()
    print(f"📊 Найдено вопросов: {len(questions)}")
    
    if questions:
        print(f"\n🎯 ВСЕ ВОПРОСЫ DISC:")
        for i, q in enumerate(questions, 1):
            print(f"{i}. Структура вопроса: {q}")
            print()
        
        # Проверяем структуру
        first_question = questions[0]
        print(f"✅ СТРУКТУРА первого вопроса: {first_question}")
        print(f"✅ Ключи: {list(first_question.keys())}")
    else:
        print("❌ ОШИБКА! Вопросы не найдены")

if __name__ == "__main__":
    main()