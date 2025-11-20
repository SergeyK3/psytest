#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест парсинга PAEI/Adizes вопросов из файла
"""

import re

def parse_adizes_questions(filepath="data/prompts/adizes_user.txt"):
    """Парсит вопросы PAEI/Adizes из файла"""
    try:
        questions = []
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Разбиваем на блоки вопросов (ищем паттерн с номером)
        question_blocks = re.split(r'\n(?=\d+\.)', content)
        
        for block in question_blocks:
            if not block.strip() or not re.match(r'^\d+\.', block.strip()):
                continue
                
            lines = block.strip().split('\n')
            question_text = lines[0].strip()
            
            # Извлекаем сам вопрос (убираем номер)
            question_text = re.sub(r'^\d+\.\s*', '', question_text)
            
            answers = {}
            for line in lines[1:]:
                line = line.strip()
                if re.match(r'^[PAEI]\.', line):
                    code = line[0]  # P, A, E, или I
                    answer_text = re.sub(r'^[PAEI]\.\s*', '', line)
                    answers[code] = answer_text
            
            if question_text and len(answers) == 4:  # Должно быть 4 ответа
                questions.append({
                    "question": question_text,
                    "answers": answers
                })
        
        print(f"📊 Загружено {len(questions)} PAEI вопросов из {filepath}")
        return questions
        
    except Exception as e:
        print(f"❌ Ошибка при загрузке PAEI вопросов: {e}")
        return []

if __name__ == "__main__":
    print("🧪 Тестирование парсинга PAEI вопросов...")
    questions = parse_adizes_questions()
    
    print(f"\n📋 Результат: {len(questions)} вопросов")
    
    for i, q in enumerate(questions, 1):
        print(f"\n{i}. {q['question']}")
        for code, answer in q['answers'].items():
            print(f"   {code}. {answer}")
    
    print("\n🎯 Тест завершен!")