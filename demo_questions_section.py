#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрационный скрипт для тестирования новой функциональности
включения раздела с вопросами, ответами и баллами в PDF отчет
"""

from pathlib import Path
from datetime import datetime
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from questions_answers_section import create_sample_data_for_testing


def demonstrate_questions_section():
    """
    Демонстрирует работу раздела с вопросами и ответами
    """
    print("🧪 ДЕМОНСТРАЦИЯ РАЗДЕЛА С ВОПРОСАМИ И ОТВЕТАМИ")
    print("=" * 60)
    
    # === СОЗДАНИЕ ОТЧЕТА БЕЗ РАЗДЕЛА ВОПРОСОВ ===
    print("\n1️⃣ Создание обычного отчета (БЕЗ раздела вопросов)...")
    
    # Инициализация генератора отчетов БЕЗ раздела вопросов
    report_generator_standard = EnhancedPDFReportV2(
        include_questions_section=False  # 🚫 Раздел отключен
    )
    
    # Образцы данных для тестирования
    sample_data = create_sample_data_for_testing()
    
    # Генерация стандартного отчета
    standard_report_path = Path("demo_report_standard.pdf")
    
    try:
        report_generator_standard.generate_enhanced_report(
            participant_name="Иванов Иван Иванович (Стандартный отчет)",
            test_date=datetime.now().strftime("%d.%m.%Y"),
            paei_scores=sample_data['paei_scores'],
            disc_scores=sample_data['disc_scores'],
            hexaco_scores=sample_data['hexaco_scores'],
            soft_skills_scores=sample_data['soft_skills_scores'],
            ai_interpretations={
                'paei': 'Образец интерпретации PAEI для демонстрации.',
                'soft_skills': 'Образец интерпретации Soft Skills для демонстрации.',
                'hexaco': 'Образец интерпретации HEXACO для демонстрации.',
                'disc': 'Образец интерпретации DISC для демонстрации.'
            },
            out_path=standard_report_path
        )
        print(f"✅ Стандартный отчет создан: {standard_report_path}")
        
    except Exception as e:
        print(f"❌ Ошибка при создании стандартного отчета: {e}")
    
    # === СОЗДАНИЕ ОТЧЕТА С РАЗДЕЛОМ ВОПРОСОВ ===
    print("\n2️⃣ Создание расширенного отчета (С разделом вопросов)...")
    
    # Инициализация генератора отчетов С разделом вопросов
    report_generator_extended = EnhancedPDFReportV2(
        include_questions_section=True  # ✅ Раздел включен
    )
    
    # Генерация расширенного отчета
    extended_report_path = Path("demo_report_with_questions.pdf")
    
    try:
        report_generator_extended.generate_enhanced_report(
            participant_name="Петрова Анна Сергеевна (Расширенный отчет)",
            test_date=datetime.now().strftime("%d.%m.%Y"),
            paei_scores=sample_data['paei_scores'],
            disc_scores=sample_data['disc_scores'],
            hexaco_scores=sample_data['hexaco_scores'],
            soft_skills_scores=sample_data['soft_skills_scores'],
            ai_interpretations={
                'paei': 'Детальная интерпретация PAEI с анализом доминирующей роли Производителя.',
                'soft_skills': 'Комплексный анализ мягких навыков с рекомендациями по развитию.',
                'hexaco': 'Психологический портрет личности на основе модели HEXACO.',
                'disc': 'Анализ поведенческих особенностей и стилей коммуникации.'
            },
            out_path=extended_report_path,
            user_answers={  # 🔑 КЛЮЧЕВОЙ ПАРАМЕТР - ответы пользователя
                'paei': sample_data['paei_answers'],
                'soft_skills': sample_data['soft_skills_answers'],
                'hexaco': sample_data['hexaco_answers'],
                'disc': sample_data['disc_answers']
            }
        )
        print(f"✅ Расширенный отчет создан: {extended_report_path}")
        
    except Exception as e:
        print(f"❌ Ошибка при создании расширенного отчета: {e}")
        import traceback
        traceback.print_exc()
    
    # === РЕЗУЛЬТАТЫ ДЕМОНСТРАЦИИ ===
    print("\n📊 РЕЗУЛЬТАТЫ ДЕМОНСТРАЦИИ:")
    print("-" * 40)
    
    if standard_report_path.exists():
        size_standard = standard_report_path.stat().st_size / 1024  # KB
        print(f"📄 Стандартный отчет: {size_standard:.1f} KB")
    
    if extended_report_path.exists():
        size_extended = extended_report_path.stat().st_size / 1024  # KB
        print(f"📄 Расширенный отчет: {size_extended:.1f} KB")
        
        if standard_report_path.exists():
            difference = size_extended - size_standard
            print(f"📈 Разница в размере: +{difference:.1f} KB")
    
    print("\n🎯 ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:")
    print("-" * 40)
    print("1️⃣ Для ОБЫЧНОГО отчета (без вопросов):")
    print("   report = EnhancedPDFReportV2(include_questions_section=False)")
    print("")
    print("2️⃣ Для РАСШИРЕННОГО отчета (с вопросами):")
    print("   report = EnhancedPDFReportV2(include_questions_section=True)")
    print("   # И обязательно передать user_answers в generate_enhanced_report()")
    print("")
    print("3️⃣ Для ЛЕГКОГО УДАЛЕНИЯ раздела:")
    print("   # Просто измените include_questions_section=False")
    print("   # Или закомментируйте соответствующие строки в коде")


def demonstrate_data_structure():
    """
    Показывает структуру данных для user_answers
    """
    print("\n\n📋 СТРУКТУРА ДАННЫХ user_answers:")
    print("=" * 50)
    
    sample_data = create_sample_data_for_testing()
    
    print("user_answers = {")
    print("    'paei': {")
    for q_id, answer in sample_data['paei_answers'].items():
        print(f"        '{q_id}': '{answer}',  # Вопрос {int(q_id)+1} -> выбрано {answer}")
    print("    },")
    
    print("    'soft_skills': {")
    for q_id, answer in list(sample_data['soft_skills_answers'].items())[:3]:
        print(f"        '{q_id}': {answer},  # Вопрос {int(q_id)+1} -> оценка {answer}/10")
    print("        # ... остальные вопросы")
    print("    },")
    
    print("    'hexaco': {")
    for q_id, answer in list(sample_data['hexaco_answers'].items())[:3]:
        print(f"        '{q_id}': {answer},  # Вопрос {int(q_id)+1} -> оценка {answer}/5")
    print("        # ... остальные вопросы")
    print("    },")
    
    print("    'disc': {")
    for q_id, answer in list(sample_data['disc_answers'].items())[:3]:
        print(f"        '{q_id}': {answer},  # Вопрос {int(q_id)+1} -> оценка {answer}/5")
    print("        # ... остальные вопросы")
    print("    }")
    print("}")


def test_questions_module():
    """
    Тестирует модуль questions_answers_section.py
    """
    print("\n\n🔍 ТЕСТИРОВАНИЕ МОДУЛЯ questions_answers_section.py:")
    print("=" * 55)
    
    try:
        from questions_answers_section import QuestionAnswerSection
        
        qa_section = QuestionAnswerSection()
        print(f"✅ Модуль загружен успешно")
        print(f"📊 Загружено вопросов:")
        print(f"   - PAEI: {len(qa_section.paei_questions)}")
        print(f"   - Soft Skills: {len(qa_section.soft_skills_questions)}")
        print(f"   - HEXACO: {len(qa_section.hexaco_questions)}")
        print(f"   - DISC: {len(qa_section.disc_questions)}")
        
        # Тест создания образцов данных
        sample_data = create_sample_data_for_testing()
        print(f"\n✅ Образцы данных созданы:")
        print(f"   - PAEI ответы: {len(sample_data['paei_answers'])}")
        print(f"   - Soft Skills ответы: {len(sample_data['soft_skills_answers'])}")
        print(f"   - HEXACO ответы: {len(sample_data['hexaco_answers'])}")
        print(f"   - DISC ответы: {len(sample_data['disc_answers'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования модуля: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 ЗАПУСК ДЕМОНСТРАЦИИ НОВОЙ ФУНКЦИОНАЛЬНОСТИ")
    print("=" * 60)
    
    # Тестируем модуль
    if test_questions_module():
        # Показываем структуру данных
        demonstrate_data_structure()
        
        # Запускаем основную демонстрацию
        demonstrate_questions_section()
        
        print("\n🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
        print("\n📝 Откройте созданные PDF файлы для сравнения:")
        print("   - demo_report_standard.pdf (обычный)")
        print("   - demo_report_with_questions.pdf (с вопросами)")
        
    else:
        print("❌ Демонстрация прервана из-за ошибок в модуле")