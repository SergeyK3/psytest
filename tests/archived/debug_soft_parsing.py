#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Отладочный скрипт для анализа soft_user.txt
"""

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.psytest.prompts import load_prompt

def debug_soft_parsing():
    """Отлаживает парсинг soft_user.txt"""
    
    print("🔍 Отладка парсинга soft_user.txt...")
    
    try:
        content = load_prompt("soft_user.txt")
        print(f"📄 Загружен контент длиной {len(content)} символов")
        
        lines = content.split('\n')
        print(f"📋 Всего строк: {len(lines)}")
        
        print("\n--- ПЕРВЫЕ 20 СТРОК ---")
        for i, line in enumerate(lines[:20]):
            if line.strip():
                print(f"{i+1:2d}: '{line}'")
                
                # Проверяем паттерны
                if re.match(r'^\d+\.\s+[А-Я]', line.strip()):
                    print(f"    ✅ НАЙДЕН ВОПРОС: {line.strip()[:30]}...")
                
                if re.match(r'^\s+[1-5]\.\s*', line):
                    print(f"    ✅ НАЙДЕН ОТВЕТ: {line[:30]}...")
        
        # Тестируем конкретный парсинг
        print("\n--- ТЕСТИРОВАНИЕ ПАРСИНГА ---")
        current_question = None
        current_answers = {}
        questions = []
        
        for line_num, line in enumerate(lines, 1):
            line_original = line
            line = line.strip()
            
            if not line or line.startswith('Вот список') or line.startswith('Предоставь') or line.startswith('Ни в коем'):
                continue
            
            # Ищем начало вопроса
            if re.match(r'^\d+\.\s+[А-Я]', line):
                print(f"Строка {line_num}: НАЙДЕН ВОПРОС - {line[:50]}...")
                
                # Сохраняем предыдущий вопрос
                if current_question and current_answers:
                    questions.append({
                        "question": current_question,
                        "answers": current_answers.copy()
                    })
                    print(f"  💾 Сохранен предыдущий вопрос с {len(current_answers)} ответами")
                    current_answers.clear()
                
                # Начинаем новый вопрос
                current_question = re.sub(r'^\d+\.\s+', '', line)
                print(f"  📝 Новый вопрос: {current_question[:30]}...")
                
            # Ищем варианты ответов
            elif re.match(r'^\s+[1-5]\.\s*', line_original):
                answer_match = re.match(r'^\s+([1-5])\.\s*(.*)', line_original)
                if answer_match:
                    answer_key = answer_match.group(1)
                    answer_text = answer_match.group(2).strip()
                    current_answers[answer_key] = answer_text
                    print(f"Строка {line_num}: ОТВЕТ {answer_key} - {answer_text[:30]}...")
        
        # Добавляем последний вопрос
        if current_question and current_answers:
            questions.append({
                "question": current_question,
                "answers": current_answers.copy()
            })
            print(f"💾 Сохранен последний вопрос с {len(current_answers)} ответами")
        
        print(f"\n📊 ИТОГО НАЙДЕНО: {len(questions)} вопросов")
        
        for i, q in enumerate(questions):
            print(f"Вопрос {i+1}: {q['question'][:50]}... ({len(q['answers'])} ответов)")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_soft_parsing()