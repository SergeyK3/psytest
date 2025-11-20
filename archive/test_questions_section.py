#!/usr/bin/env python3
"""
Тестовый скрипт для проверки модуля questions_answers_section.py
Проверяет загрузку вопросов и генерацию раздела с расшифровкой ответов
"""

import sys
from pathlib import Path

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent))

from questions_answers_section import QuestionAnswerSection, create_sample_data_for_testing

def test_questions_loading():
    """Тестирует загрузку вопросов"""
    print("🔄 Тестируем загрузку вопросов...")
    
    qa_section = QuestionAnswerSection()
    
    print(f"📊 Статистика загруженных вопросов:")
    print(f"  • PAEI: {len(qa_section.paei_questions)} вопросов")
    print(f"  • DISC: {len(qa_section.disc_questions)} вопросов")
    print(f"  • Soft Skills: {len(qa_section.soft_skills_questions)} вопросов")
    print(f"  • HEXACO: {len(qa_section.hexaco_questions)} вопросов")
    
    # Проверяем первый вопрос PAEI
    if qa_section.paei_questions:
        first_question = qa_section.paei_questions[0]
        print(f"\n🎯 Первый вопрос PAEI:")
        print(f"❓ {first_question['question']}")
        print(f"📝 Варианты ответов:")
        for key, answer in first_question['answers'].items():
            print(f"   {key}. {answer}")
        
        # Проверяем правильность вопроса
        expected_start = "Когда возникает сложная задача"
        if first_question['question'].startswith(expected_start):
            print(f"✅ Первый вопрос загружен корректно!")
        else:
            print(f"❌ Ошибка в первом вопросе!")
    else:
        print("❌ PAEI вопросы не загружены!")

def test_paei_section_generation():
    """Тестирует генерацию раздела PAEI"""
    print("\n🔄 Тестируем генерацию раздела PAEI...")
    
    qa_section = QuestionAnswerSection()
    sample_data = create_sample_data_for_testing()
    
    # Простые стили для тестирования
    class MockStyles:
        def __getitem__(self, key):
            return {"name": key}
    
    styles = MockStyles()
    
    # Генерируем раздел
    paei_elements = qa_section.generate_paei_questions_section(
        user_answers=sample_data['paei_answers'],
        final_scores=sample_data['paei_scores'],
        styles=styles
    )
    
    print(f"📊 Сгенерировано {len(paei_elements)} элементов для раздела PAEI")
    
    # Показываем первые несколько элементов
    print(f"\n📝 Первые элементы раздела:")
    for i, element in enumerate(paei_elements[:3]):
        if hasattr(element, 'text'):
            print(f"  {i+1}. {element.text[:100]}...")
        else:
            print(f"  {i+1}. {type(element).__name__}")

def test_complete_section_generation():
    """Тестирует генерацию полного раздела с вопросами"""
    print("\n🔄 Тестируем генерацию полного раздела...")
    
    qa_section = QuestionAnswerSection()
    sample_data = create_sample_data_for_testing()
    
    # Простые стили для тестирования
    class MockStyles:
        def __getitem__(self, key):
            return {"name": key}
    
    styles = MockStyles()
    
    # Генерируем полный раздел
    all_elements = qa_section.generate_complete_questions_section(
        paei_answers=sample_data['paei_answers'],
        soft_skills_answers=sample_data['soft_skills_answers'],
        hexaco_answers=sample_data['hexaco_answers'],
        disc_answers=sample_data['disc_answers'],
        paei_scores=sample_data['paei_scores'],
        soft_skills_scores=sample_data['soft_skills_scores'],
        hexaco_scores=sample_data['hexaco_scores'],
        disc_scores=sample_data['disc_scores'],
        styles=styles
    )
    
    print(f"📊 Сгенерировано {len(all_elements)} элементов для полного раздела")
    print(f"✅ Полный раздел готов к интеграции с PDF генератором")

def main():
    """Основная функция тестирования"""
    print("🚀 ТЕСТИРОВАНИЕ МОДУЛЯ QUESTIONS_ANSWERS_SECTION")
    print("=" * 50)
    
    test_questions_loading()
    test_paei_section_generation()
    test_complete_section_generation()
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено!")

if __name__ == "__main__":
    main()