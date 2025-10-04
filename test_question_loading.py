#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест для проверки загрузки вопросов из файлов "_user.txt"
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_test_bot import parse_paei_questions, parse_disc_questions, parse_hexaco_questions, parse_soft_skills_questions

def test_question_loading():
    """Тестирует загрузку всех типов вопросов"""
    
    print("🚀 Тестирование загрузки вопросов из промптов...")
    
    # Тест PAEI
    print("\n--- ТЕСТ PAEI ---")
    paei_questions = parse_paei_questions()
    print(f"Количество вопросов PAEI: {len(paei_questions)}")
    
    if paei_questions:
        first_q = paei_questions[0]
        print(f"Первый вопрос: {first_q['question'][:50]}...")
        print(f"Варианты ответов: {list(first_q['answers'].keys())}")
    
    # Тест DISC  
    print("\n--- ТЕСТ DISC ---")
    disc_questions = parse_disc_questions()
    print(f"Количество вопросов DISC: {len(disc_questions)}")
    
    if disc_questions:
        first_q = disc_questions[0]
        print(f"Первый вопрос: {first_q['question'][:50]}...")
        print(f"Шкала: {first_q.get('scale', 'не указана')}")
    
    # Тест HEXACO
    print("\n--- ТЕСТ HEXACO ---")
    hexaco_questions = parse_hexaco_questions()
    print(f"Количество вопросов HEXACO: {len(hexaco_questions)}")
    
    if hexaco_questions:
        first_q = hexaco_questions[0]
        print(f"Первый вопрос: {first_q['question'][:50]}...")
        print(f"Шкала: {first_q.get('scale', 'не указана')}")
    
    # Тест Soft Skills
    print("\n--- ТЕСТ SOFT SKILLS ---")
    soft_questions = parse_soft_skills_questions()
    print(f"Количество вопросов Soft Skills: {len(soft_questions)}")
    
    if soft_questions:
        first_q = soft_questions[0]
        print(f"Первый вопрос: {first_q['question'][:50]}...")
        if 'answers' in first_q:
            print(f"Варианты ответов: {list(first_q['answers'].keys())}")
        else:
            print("Варианты ответов: шкала 1-5")
    
    # Проверка общих результатов
    print(f"\n📊 ИТОГО:")
    print(f"PAEI: {len(paei_questions)} вопросов")
    print(f"DISC: {len(disc_questions)} вопросов") 
    print(f"HEXACO: {len(hexaco_questions)} вопросов")
    print(f"Soft Skills: {len(soft_questions)} вопросов")
    
    total_questions = len(paei_questions) + len(disc_questions) + len(hexaco_questions) + len(soft_questions)
    print(f"Всего загружено: {total_questions} вопросов")
    
    # Проверки корректности
    success = True
    
    if len(paei_questions) == 0:
        print("❌ PAEI: вопросы не загружены")
        success = False
    
    if len(disc_questions) == 0:
        print("❌ DISC: вопросы не загружены")
        success = False
        
    if len(hexaco_questions) == 0:
        print("❌ HEXACO: вопросы не загружены")
        success = False
        
    if len(soft_questions) == 0:
        print("❌ Soft Skills: вопросы не загружены")
        success = False
    
    # Проверка форматов PAEI
    if paei_questions:
        for i, q in enumerate(paei_questions):
            if 'question' not in q or 'answers' not in q:
                print(f"❌ PAEI вопрос {i+1}: неправильный формат")
                success = False
            elif not all(k in q['answers'] for k in ['P', 'A', 'E', 'I']):
                print(f"❌ PAEI вопрос {i+1}: отсутствуют варианты P/A/E/I")
                success = False
    
    if success:
        print("\n✅ Все вопросы загружены успешно!")
    else:
        print("\n❌ Обнаружены проблемы с загрузкой вопросов!")
    
    return success

def test_question_samples():
    """Показывает примеры загруженных вопросов"""
    
    print("\n🔍 Примеры загруженных вопросов:")
    
    paei_questions = parse_paei_questions()
    if paei_questions:
        print(f"\n--- ПРИМЕР PAEI ---")
        q = paei_questions[0]
        print(f"Вопрос: {q['question']}")
        for key, answer in q['answers'].items():
            print(f"  {key}. {answer}")
    
    disc_questions = parse_disc_questions()
    if disc_questions:
        print(f"\n--- ПРИМЕР DISC ---")
        q = disc_questions[0]
        print(f"Вопрос: {q['question']}")
        print(f"Шкала: {q.get('scale', '1-5')}")
    
    hexaco_questions = parse_hexaco_questions()
    if hexaco_questions:
        print(f"\n--- ПРИМЕР HEXACO ---")
        q = hexaco_questions[0]
        print(f"Вопрос: {q['question']}")
        print(f"Шкала: {q.get('scale', '1-5')}")
    
    soft_questions = parse_soft_skills_questions()
    if soft_questions:
        print(f"\n--- ПРИМЕР SOFT SKILLS ---")
        q = soft_questions[0]
        print(f"Вопрос: {q['question']}")
        if 'answers' in q:
            for key, answer in q['answers'].items():
                print(f"  {key}. {answer}")

if __name__ == "__main__":
    print("🔄 Запуск тестирования загрузки вопросов...")
    
    # Основной тест
    success = test_question_loading()
    
    # Показать примеры
    test_question_samples()
    
    if success:
        print("\n🎉 Тестирование завершено успешно!")
    else:
        print("\n❌ Тестирование выявило проблемы!")
        exit(1)