#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест правильности форматирования секции детализации ответов
"""

import sys
from pathlib import Path
from questions_answers_section import QuestionAnswerSection, create_sample_data_for_testing
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4

def test_formatting():
    """Тестирует правильность форматирования"""
    
    # Создаем экземпляр класса
    qa_section = QuestionAnswerSection()
    
    # Получаем тестовые данные
    sample_data = create_sample_data_for_testing()
    
    # Исправляем тестовые данные на правильные диапазоны
    # Soft Skills: диапазон 1-5 (не 1-10)
    sample_data['soft_skills_answers'] = {str(i): (i % 5) + 1 for i in range(10)}
    sample_data['soft_skills_scores'] = {
        "Коммуникация": 4, "Работа в команде": 3, "Лидерство": 5, 
        "Критическое мышление": 2, "Управление временем": 4,
        "Стрессоустойчивость": 3, "Эмоциональный интеллект": 4,
        "Адаптивность": 5, "Решение проблем": 3, "Креативность": 4
    }
    
    # HEXACO: диапазон 1-5 (уже правильный)
    sample_data['hexaco_scores'] = {"H": 4.2, "E": 3.1, "X": 3.8, "A": 4.0, "C": 3.5, "O": 4.1}
    
    # Настройка стилей
    styles = getSampleStyleSheet()
    styles.add(styles['Heading1'].clone('MainTitle'))
    styles.add(styles['Heading2'].clone('SectionTitle'))
    styles.add(styles['Heading3'].clone('SubTitle'))
    styles.add(styles['Normal'].clone('Body'))
    styles.add(styles['Normal'].clone('ListWithIndent'))
    
    print("=== ТЕСТ ФОРМАТИРОВАНИЯ SOFT SKILLS ===")
    soft_elements = qa_section.generate_soft_skills_questions_section(
        sample_data['soft_skills_answers'],
        sample_data['soft_skills_scores'],
        styles
    )
    print(f"Создано {len(soft_elements)} элементов для Soft Skills")
    
    print("\n=== ТЕСТ ФОРМАТИРОВАНИЯ HEXACO ===")
    hexaco_elements = qa_section.generate_hexaco_questions_section(
        sample_data['hexaco_answers'],
        sample_data['hexaco_scores'],
        styles
    )
    print(f"Создано {len(hexaco_elements)} элементов для HEXACO")
    
    print("\n=== СОЗДАНИЕ ТЕСТОВОГО PDF ===")
    # Создаем тестовый PDF для проверки
    output_path = Path("test_questions_formatting.pdf")
    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    
    story = []
    story.extend(soft_elements)
    story.extend(hexaco_elements)
    
    try:
        doc.build(story)
        print(f"✅ Тестовый PDF создан: {output_path}")
        print(f"📄 Проверьте форматирование в файле {output_path}")
        
        # Выводим информацию о форматировании
        print("\n=== ОЖИДАЕМОЕ ФОРМАТИРОВАНИЕ ===")
        print("Soft Skills:")
        print("  - Ответ: X/5 баллов (интерпретация)")
        print("  - Интерпретация для шкалы 1-5:")
        print("    * 4-5: Выше среднего уровня")
        print("    * 3: Средний уровень")
        print("    * 2: Ниже среднего уровня")
        print("    * 1: Требует значительного развития")
        
        print("\nHEXACO:")
        print("  - Ответ: X/5 баллов (интерпретация)")
        print("  - Итоговые баллы: H=4.2, E=3.1, X=3.8 и т.д. (без нормализации к 10)")
        
    except Exception as e:
        print(f"❌ Ошибка создания PDF: {e}")

if __name__ == "__main__":
    test_formatting()