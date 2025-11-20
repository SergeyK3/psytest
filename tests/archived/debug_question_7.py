#!/usr/bin/env python3
"""
Отладка парсинга 7-го вопроса Soft Skills
"""

import sys
sys.path.append("d:/MyActivity/MyInfoBusiness/MyPythonApps/07 PsychTest")

from telegram_test_bot import parse_soft_skills_questions

def debug_question_7():
    """Отладка 7-го вопроса о критике"""
    print("🔍 Отладка парсинга 7-го вопроса Soft Skills...")
    
    questions = parse_soft_skills_questions()
    print(f"📊 Всего найдено вопросов: {len(questions)}")
    
    if len(questions) >= 7:
        question_7 = questions[6]  # 7-й вопрос (индекс 6)
        print(f"\n❓ 7-й вопрос:")
        print(f"   Текст: {question_7['question']}")
        print(f"   Количество ответов: {len(question_7.get('answers', {}))}")
        
        if 'answers' in question_7:
            print(f"   Варианты ответов:")
            for key, value in question_7['answers'].items():
                print(f"     {key}. {value}")
                
            # Проверяем наличие всех ответов 1-5
            expected_keys = {'1', '2', '3', '4', '5'}
            actual_keys = set(question_7['answers'].keys())
            
            print(f"\n🎯 Анализ:")
            print(f"   Ожидаемые ключи: {sorted(expected_keys)}")
            print(f"   Фактические ключи: {sorted(actual_keys)}")
            
            missing_keys = expected_keys - actual_keys
            extra_keys = actual_keys - expected_keys
            
            if missing_keys:
                print(f"   ❌ Отсутствуют ключи: {sorted(missing_keys)}")
            if extra_keys:
                print(f"   ⚠️  Лишние ключи: {sorted(extra_keys)}")
            if not missing_keys and not extra_keys:
                print(f"   ✅ Все ключи на месте")
                
        else:
            print("   ❌ Нет вариантов ответов!")
    else:
        print("❌ 7-й вопрос не найден!")
        
    # Проверим все вопросы на наличие всех ответов
    print(f"\n📋 Проверка всех вопросов:")
    for i, question in enumerate(questions, 1):
        answers = question.get('answers', {})
        keys = set(answers.keys())
        expected = {'1', '2', '3', '4', '5'}
        
        if keys == expected:
            status = "✅"
        else:
            status = "❌"
            
        print(f"   {status} Вопрос {i}: {len(keys)}/5 ответов, ключи: {sorted(keys)}")

def main():
    debug_question_7()

if __name__ == "__main__":
    main()