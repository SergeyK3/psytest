#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для загрузки вопросов тестов без циклических импортов
Содержит только функции парсинга и константы вопросов
"""

import re
from pathlib import Path
from typing import Dict, List


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


def parse_disc_questions(filepath="data/prompts/disc_user.txt"):
    """Парсит вопросы DISC из файла"""
    try:
        questions = []
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ищем блоки вопросов по номерам
        question_blocks = re.split(r'\n(?=\d+\.)', content)
        
        for block in question_blocks:
            if not block.strip() or not re.match(r'^\d+\.', block.strip()):
                continue
            
            lines = block.strip().split('\n')
            question_text = lines[0].strip()
            question_text = re.sub(r'^\d+\.\s*', '', question_text)
            
            if question_text:
                questions.append({
                    "question": question_text,
                    "scale": "1-5"
                })
        
        print(f"📊 Загружено {len(questions)} DISC вопросов из {filepath}")
        return questions
        
    except Exception as e:
        print(f"❌ Ошибка при загрузке DISC вопросов: {e}")
        return []


def parse_hexaco_questions():
    """Возвращает стандартные вопросы HEXACO"""
    return [
        {
            "question": "Я предпочитаю говорить правду, даже если это неудобно",
            "scale": "1-5",
            "dimension": "H"  # Honesty-Humility
        },
        {
            "question": "Я часто чувствую беспокойство о будущем",
            "scale": "1-5", 
            "dimension": "E"  # Emotionality
        },
        {
            "question": "Я люблю быть в центре внимания",
            "scale": "1-5",
            "dimension": "X"  # eXtraversion
        },
        {
            "question": "Я стараюсь следовать своим планам, даже если они сложные",
            "scale": "1-5",
            "dimension": "A"  # Agreeableness
        },
        {
            "question": "Мне легко найти общий язык с другими людьми",
            "scale": "1-5",
            "dimension": "C"  # Conscientiousness
        },
        {
            "question": "Я наслаждаюсь изучением новых идей и концепций",
            "scale": "1-5",
            "dimension": "O"  # Openness to experience
        }
    ]


def parse_soft_skills_questions(filepath="data/prompts/soft_user.txt"):
    """Парсит вопросы Soft Skills из файла"""
    try:
        questions = []
        current_question = None
        answers = {}
        
        # Маппинг номеров вопросов на навыки
        skills_mapping = {
            1: "Коммуникация",
            2: "Работа в команде", 
            3: "Лидерство",
            4: "Критическое мышление",
            5: "Управление временем",
            6: "Стрессоустойчивость",
            7: "Эмоциональный интеллект",
            8: "Адаптивность",
            9: "Решение проблем",
            10: "Креативность"
        }
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_original in lines:
            line = line_original.strip()
            
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            
            # Ищем номерованный вопрос
            question_match = re.match(r'^\s*(\d+)\.\s*(.*)', line_original)
            if question_match:
                # Сохраняем предыдущий вопрос
                if current_question and answers:
                    question_num = len(questions) + 1
                    skill = skills_mapping.get(question_num, "Общие навыки")
                    questions.append({
                        'question': current_question,
                        'scale': "1-10",
                        'skill': skill,
                        'answers': answers.copy()
                    })
                
                # Начинаем новый вопрос
                current_question = question_match.group(2).strip()
                answers = {}
                continue
                
            # Ищем варианты ответов (если есть)
            if current_question:
                answer_match = re.match(r'^\s+([1-9]|10)\.\s*(.*)', line_original)
                if answer_match:
                    key = answer_match.group(1)
                    text = answer_match.group(2).strip()
                    answers[key] = text
                    continue
        
        # Добавляем последний вопрос
        if current_question and answers:
            question_num = len(questions) + 1
            skill = skills_mapping.get(question_num, "Общие навыки")
            questions.append({
                'question': current_question,
                'scale': "1-10",
                'skill': skill,
                'answers': answers.copy()
            })
        
        if questions:
            print(f"📊 Загружено {len(questions)} Soft Skills вопросов из {filepath}")
        else:
            print(f"❌ Не удалось загрузить Soft Skills вопросы из {filepath}")
        
        return questions
        
    except Exception as e:
        print(f"❌ Ошибка при загрузке Soft Skills вопросов: {e}")
        return []


def get_all_questions():
    """Загружает все вопросы всех тестов"""
    return {
        'paei': parse_adizes_questions(),
        'disc': parse_disc_questions(),
        'hexaco': parse_hexaco_questions(),
        'soft_skills': parse_soft_skills_questions()
    }


# Константы с вопросами
PAEI_QUESTIONS = parse_adizes_questions()
DISC_QUESTIONS = parse_disc_questions()
HEXACO_QUESTIONS = parse_hexaco_questions()
SOFT_SKILLS_QUESTIONS = parse_soft_skills_questions()


if __name__ == "__main__":
    print("🧪 Тестирование загрузки вопросов...")
    
    all_questions = get_all_questions()
    
    print(f"\n📊 Результаты загрузки:")
    print(f"  - PAEI: {len(all_questions['paei'])} вопросов")
    print(f"  - DISC: {len(all_questions['disc'])} вопросов")
    print(f"  - HEXACO: {len(all_questions['hexaco'])} вопросов")
    print(f"  - Soft Skills: {len(all_questions['soft_skills'])} вопросов")
    
    print(f"\n✅ Модуль test_questions_loader.py готов к использованию!")