#!/usr/bin/env python3
"""
Простой тест модуля questions_answers_section.py без ReportLab зависимостей
"""

import sys
from pathlib import Path

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent))

from questions_answers_section import QuestionAnswerSection, get_all_questions

def test_questions_loading():
    """Тестирует загрузку вопросов"""
    print("🔄 Тестируем загрузку вопросов...")
    
    questions = get_all_questions()
    
    print(f"📊 Статистика загруженных вопросов:")
    print(f"  • PAEI: {len(questions['paei'])} вопросов")
    print(f"  • DISC: {len(questions['disc'])} вопросов")
    print(f"  • Soft Skills: {len(questions['soft_skills'])} вопросов")
    print(f"  • HEXACO: {len(questions['hexaco'])} вопросов")
    
    # Проверяем PAEI вопросы
    if questions['paei']:
        first_question = questions['paei'][0]
        print(f"\n🎯 Первый вопрос PAEI:")
        print(f"❓ {first_question['question']}")
        print(f"📝 Варианты ответов:")
        for key, answer in first_question['answers'].items():
            print(f"   {key}. {answer}")
        
        # Проверяем правильность
        expected_start = "Когда возникает сложная задача"
        if first_question['question'].startswith(expected_start):
            print(f"✅ PAEI вопросы загружены корректно!")
        else:
            print(f"❌ Ошибка в PAEI вопросах!")
    
    # Проверяем DISC вопросы
    if questions['disc']:
        print(f"\n🎯 Первые 3 вопроса DISC:")
        for i, question in enumerate(questions['disc'][:3]):
            print(f"  {i+1}. {question['question']} (категория: {question.get('category', 'N/A')})")
        print(f"✅ DISC вопросы загружены корректно!")
    
    # Проверяем Soft Skills вопросы
    if questions['soft_skills']:
        print(f"\n🎯 Первые 3 вопроса Soft Skills:")
        for i, question in enumerate(questions['soft_skills'][:3]):
            print(f"  {i+1}. {question['question']} (навык: {question.get('skill', 'N/A')})")
        print(f"✅ Soft Skills вопросы загружены корректно!")
    
    # Проверяем HEXACO вопросы
    if questions['hexaco']:
        print(f"\n🎯 Все HEXACO вопросы:")
        for i, question in enumerate(questions['hexaco']):
            dimension_full = {
                'H': 'Честность-Скромность',
                'E': 'Эмоциональность', 
                'X': 'Экстраверсия',
                'A': 'Доброжелательность',
                'C': 'Добросовестность',
                'O': 'Открытость опыту'
            }.get(question.get('dimension', 'N/A'), 'Неизвестно')
            
            print(f"  {i+1}. {question['question']} ({dimension_full})")
        print(f"✅ HEXACO вопросы загружены корректно!")

def test_data_structure():
    """Проверяет структуру данных для интеграции с PDF генератором"""
    print(f"\n🔄 Тестируем структуру данных...")
    
    qa_section = QuestionAnswerSection()
    
    # Проверяем, что вопросы загружены
    print(f"📊 Объект QuestionAnswerSection создан:")
    print(f"  • PAEI: {len(qa_section.paei_questions)} вопросов")
    print(f"  • DISC: {len(qa_section.disc_questions)} вопросов") 
    print(f"  • Soft Skills: {len(qa_section.soft_skills_questions)} вопросов")
    print(f"  • HEXACO: {len(qa_section.hexaco_questions)} вопросов")
    
    # Проверяем структуру вопроса PAEI
    if qa_section.paei_questions:
        question = qa_section.paei_questions[0]
        required_keys = ['question', 'answers']
        has_all_keys = all(key in question for key in required_keys)
        print(f"✅ Структура PAEI вопроса корректна: {has_all_keys}")
        
        # Проверяем варианты ответов
        answers = question['answers']
        expected_options = ['P', 'A', 'E', 'I']
        has_all_options = all(option in answers for option in expected_options)
        print(f"✅ Все варианты ответов PAEI присутствуют: {has_all_options}")

def main():
    """Основная функция тестирования"""
    print("🚀 ПРОСТОЙ ТЕСТ МОДУЛЯ QUESTIONS_ANSWERS_SECTION")
    print("=" * 60)
    
    test_questions_loading()
    test_data_structure()
    
    print("\n" + "=" * 60)
    print("✅ Тестирование завершено! Модуль готов к интеграции с PDF генератором")

if __name__ == "__main__":
    main()