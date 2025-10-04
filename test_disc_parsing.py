#!/usr/bin/env python3
"""
Тест парсинга DISC вопросов
"""

import sys
sys.path.append("d:/MyActivity/MyInfoBusiness/MyPythonApps/07 PsychTest")

from src.psytest.prompts import load_prompt

def parse_disc_questions(prompt_text):
    """Парсинг вопросов DISC из текста промпта"""
    lines = prompt_text.strip().split('\n')
    questions = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Ищем строки вида "1.1 текст", "2.2 текст" и т.д.
        if len(line) > 4 and line[1] == '.' and line[3] == ' ':
            try:
                category = int(line[0])  # 1, 2, 3, 4
                subcategory = int(line[2])  # 1 или 2
                text = line[4:]  # Текст после "1.1 "
                
                questions.append({
                    'category': category,
                    'subcategory': subcategory,
                    'text': text
                })
            except ValueError:
                continue
    
    return questions

def main():
    print("🔄 Тестируем парсинг DISC вопросов...")
    
    # Загружаем промпт
    prompt_text = load_prompt("disc_user.txt")
    print(f"📄 Промпт загружен, размер: {len(prompt_text)} символов")
    print(f"📝 Первые 200 символов: {prompt_text[:200]}...")
    
    # Парсим вопросы
    questions = parse_disc_questions(prompt_text)
    print(f"📊 Найдено вопросов: {len(questions)}")
    
    if questions:
        print(f"\n🎯 ВСЕ ВОПРОСЫ DISC:")
        for i, q in enumerate(questions, 1):
            print(f"{i}. Категория {q['category']}.{q['subcategory']}: {q['text']}")
        
        # Проверяем первый вопрос
        first_question = questions[0]
        expected_start = "Я предпочитаю брать на себя ответственность"
        if first_question['text'].startswith(expected_start):
            print(f"\n✅ УСПЕХ! Первый вопрос правильный")
            print(f"✅ Начинается с: '{expected_start}'")
        else:
            print(f"\n❌ ПРОБЛЕМА! Ожидался вопрос, начинающийся с: '{expected_start}'")
            print(f"❌ Получен: '{first_question['text'][:50]}...'")
    else:
        print("❌ ОШИБКА! Вопросы не найдены")

if __name__ == "__main__":
    main()