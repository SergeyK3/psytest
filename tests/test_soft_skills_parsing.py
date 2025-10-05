#!/usr/bin/env python3
"""
Тест парсинга Soft Skills вопросов из telegram_test_bot.py
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from telegram_test_bot import parse_soft_skills_questions

def main():
    print("🔄 Тестируем парсинг Soft Skills вопросов...")
    
    # Парсим вопросы через функцию из бота
    questions = parse_soft_skills_questions()
    print(f"📊 Найдено вопросов: {len(questions)}")
    
    if questions:
        print(f"\n🎯 ВСЕ ВОПРОСЫ SOFT SKILLS:")
        for i, q in enumerate(questions, 1):
            print(f"{i}. [{q.get('skill', 'Неизвестно')}] {q['question']}")
            
            if 'answers' in q and q['answers']:
                print(f"   Варианты ответов:")
                for answer in q['answers']:
                    print(f"   {answer['value']}: {answer['text']}")
            else:
                print(f"   Шкала: {q.get('scale', '1-5')}")
            print()
        
        # Проверяем структуру
        first_question = questions[0]
        print(f"✅ СТРУКТУРА первого вопроса: {first_question}")
        
        # Ищем проблемный вопрос 7
        if len(questions) >= 7:
            question_7 = questions[6]  # Индекс 6 для 7-го вопроса
            print(f"\n🔍 ВОПРОС 7 (проблемный): {question_7['question']}")
            print(f"✅ Навык: {question_7.get('skill', 'Неизвестно')}")
            
            if 'answers' in question_7 and question_7['answers']:
                print(f"✅ Количество вариантов ответов: {len(question_7['answers'])}")
                for answer in question_7['answers']:
                    print(f"   {answer['value']}: {answer['text']}")
            else:
                print(f"❌ Варианты ответов не найдены")
        
    else:
        print("❌ ОШИБКА! Вопросы не найдены")

if __name__ == "__main__":
    main()