#!/usr/bin/env python3
"""
Тест для проверки первого вопроса PAEI из prompts
"""

import sys
sys.path.append("d:/MyActivity/MyInfoBusiness/MyPythonApps/07 PsychTest")

from src.psytest.prompts import load_prompt

def parse_paei_questions(prompt_text):
    """Парсинг вопросов PAEI из текста промпта"""
    lines = prompt_text.strip().split('\n')
    questions = []
    current_question = None
    current_options = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Проверяем, начинается ли строка с номера (1. 2. и т.д.)
        if line[0].isdigit() and line[1:3] == '. ':
            # Если есть текущий вопрос, сохраняем его
            if current_question:
                questions.append({
                    'question': current_question,
                    'options': current_options
                })
            
            # Начинаем новый вопрос
            current_question = line[3:]  # Убираем "1. "
            current_options = []
        
        # Проверяем варианты ответов (P. A. E. I.)
        elif line.startswith(('P. ', 'A. ', 'E. ', 'I. ')):
            option_letter = line[0]
            option_text = line[3:]  # Убираем "P. "
            current_options.append({
                'letter': option_letter,
                'text': option_text
            })
    
    # Добавляем последний вопрос
    if current_question:
        questions.append({
            'question': current_question,
            'options': current_options
        })
    
    return questions

def main():
    print("🔄 Тестируем загрузку первого вопроса PAEI...")
    
    # Загружаем промпт
    prompt_text = load_prompt("adizes_user.txt")
    print(f"📄 Промпт загружен, размер: {len(prompt_text)} символов")
    
    # Парсим вопросы
    questions = parse_paei_questions(prompt_text)
    print(f"📊 Найдено вопросов: {len(questions)}")
    
    if questions:
        first_question = questions[0]
        print(f"\n🎯 ПЕРВЫЙ ВОПРОС PAEI:")
        print(f"❓ {first_question['question']}")
        print(f"\n📝 Варианты ответов:")
        for option in first_question['options']:
            print(f"  {option['letter']}. {option['text']}")
        
        # Проверяем, что это правильный вопрос
        expected_start = "Когда возникает сложная задача"
        if first_question['question'].startswith(expected_start):
            print(f"\n✅ УСПЕХ! Первый вопрос правильный")
            print(f"✅ Начинается с: '{expected_start}'")
        else:
            print(f"\n❌ ОШИБКА! Ожидался вопрос, начинающийся с: '{expected_start}'")
            print(f"❌ Получен: '{first_question['question'][:50]}...'")
    else:
        print("❌ ОШИБКА! Вопросы не найдены")

if __name__ == "__main__":
    main()