#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой тест для Soft Skills
"""

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.psytest.prompts import load_prompt

try:
    content = load_prompt("soft_user.txt")
    print(f"Контент загружен: {len(content)} символов")
    
    lines = content.split('\n')
    print(f"Строк: {len(lines)}")
    
    for i, line in enumerate(lines[:15], 1):
        if line.strip():
            print(f"{i}: {repr(line)}")
            if re.match(r'^([1-9]|10)\.\s+', line.strip()):
                print(f"  -> ВОПРОС НАЙДЕН!")
    
    # Тест парсинга  
    questions = []
    current_question = None
    current_answers = {}
    
    for line in lines:
        line_original = line
        line = line.strip()
        
        if not line:
            continue
            
        # Основные вопросы (1-10, БЕЗ отступа в начале)
        if re.match(r'^([1-9]|10)\.\s+[А-Я]', line_original):  # line_original вместо line!
            if current_question and current_answers:
                questions.append({"question": current_question, "answers": current_answers.copy()})
                current_answers.clear()
            
            current_question = re.sub(r'^([1-9]|10)\.\s+', '', line)
            print(f"ВОПРОС: {current_question[:30]}...")
            
        # Варианты ответов
        elif re.match(r'^\s+[1-5]\.\s*', line_original) and current_question:
            answer_match = re.match(r'^\s+([1-5])\.\s*(.*)', line_original)
            if answer_match:
                key = answer_match.group(1)
                text = answer_match.group(2).strip()
                current_answers[key] = text
                print(f"  ОТВЕТ {key}: {text[:20]}...")
    
    if current_question and current_answers:
        questions.append({"question": current_question, "answers": current_answers.copy()})
    
    print(f"ИТОГО: {len(questions)} вопросов")
    
except Exception as e:
    print(f"ОШИБКА: {e}")
    import traceback
    traceback.print_exc()