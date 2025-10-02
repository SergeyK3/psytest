#!/usr/bin/env python3
"""
Тестовый скрипт для проверки интеграции всех четырех тестов в Telegram боте
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_test_bot import UserSession, PAEI_QUESTIONS, DISC_QUESTIONS, HEXACO_QUESTIONS, SOFT_SKILLS_QUESTIONS
from enhanced_pdf_report_v2 import EnhancedPDFReportV2

def test_complete_integration():
    """Тестирует полную интеграцию всех тестов"""
    
    print("🧪 Тест интеграции всех четырех психологических тестов")
    print("=" * 60)
    
    # Создаем тестовую сессию пользователя
    session = UserSession("Тестов Иван Иванович")
    session.user_name = "Тестов Иван Иванович"  # Добавляем явно атрибут
    
    # === ПРОВЕРКА 1: Количество вопросов ===
    print(f"📊 Количество вопросов по тестам:")
    print(f"   PAEI: {len(PAEI_QUESTIONS)} вопросов")
    print(f"   DISC: {len(DISC_QUESTIONS)} вопросов")
    print(f"   HEXACO: {len(HEXACO_QUESTIONS)} вопросов")
    print(f"   Soft Skills: {len(SOFT_SKILLS_QUESTIONS)} вопросов")
    print()
    
    # === ПРОВЕРКА 2: Симуляция ответов PAEI ===
    print("🎯 Симуляция теста PAEI...")
    test_paei_answers = ["P", "A", "E", "I", "P", "P", "A", "A"]  # 8 ответов
    for i, answer in enumerate(test_paei_answers):
        session.paei_scores[answer] += 1
    print(f"   PAEI результаты: {session.paei_scores}")
    
    # === ПРОВЕРКА 3: Симуляция ответов DISC ===
    print("🎯 Симуляция теста DISC...")
    test_disc_answers = ["D", "I", "S", "C", "D", "D", "I", "S"]  # 8 ответов
    for answer in test_disc_answers:
        session.disc_scores[answer] += 1
    print(f"   DISC результаты: {session.disc_scores}")
    
    # === ПРОВЕРКА 4: Симуляция ответов HEXACO ===
    print("🎯 Симуляция теста HEXACO...")
    test_hexaco_answers = [4, 3, 5, 2, 4, 3]  # 6 ответов по шкале 1-5
    session.hexaco_scores = test_hexaco_answers.copy()
    print(f"   HEXACO ответы (1-5): {session.hexaco_scores}")
    
    # === ПРОВЕРКА 5: Симуляция ответов Soft Skills ===
    print("🎯 Симуляция теста Soft Skills...")
    test_soft_skills_answers = [7, 8, 6, 9, 7, 8, 6, 7, 8, 7]  # 10 ответов по шкале 1-10
    session.soft_skills_scores = test_soft_skills_answers.copy()
    print(f"   Soft Skills ответы (1-10): {session.soft_skills_scores}")
    print()
    
    # === ПРОВЕРКА 6: Преобразование данных для PDF ===
    print("🔄 Преобразование данных для PDF...")
    
    # Преобразуем PAEI
    total_paei = sum(session.paei_scores.values()) or 1
    paei_converted = {
        "P": round(1 + (session.paei_scores["P"] / total_paei) * 9, 1),
        "A": round(1 + (session.paei_scores["A"] / total_paei) * 9, 1), 
        "E": round(1 + (session.paei_scores["E"] / total_paei) * 9, 1),
        "I": round(1 + (session.paei_scores["I"] / total_paei) * 9, 1)
    }
    
    # Преобразуем DISC
    total_disc = sum(session.disc_scores.values()) or 1
    disc_converted = {
        "D": round(1 + (session.disc_scores["D"] / total_disc) * 9, 1),
        "I": round(1 + (session.disc_scores["I"] / total_disc) * 9, 1),
        "S": round(1 + (session.disc_scores["S"] / total_disc) * 9, 1),
        "C": round(1 + (session.disc_scores["C"] / total_disc) * 9, 1)
    }
    
    # Преобразуем HEXACO
    hexaco_dimensions = ["H", "E", "X", "A", "C", "O"]
    hexaco_converted = {}
    for i, dimension in enumerate(hexaco_dimensions):
        score = session.hexaco_scores[i]  # Оценка 1-5
        hexaco_converted[dimension] = round((score / 5.0) * 10.0, 1)
    
    # Преобразуем Soft Skills
    soft_skills_names = ["Коммуникация", "Лидерство", "Работа в команде", "Критическое мышление",
                        "Решение проблем", "Адаптивность", "Управление временем", "Эмоциональный интеллект",
                        "Креативность", "Стрессоустойчивость"]
    soft_skills_converted = {}
    for i, skill_name in enumerate(soft_skills_names):
        soft_skills_converted[skill_name] = session.soft_skills_scores[i]
    
    print(f"   PAEI (1-10): {paei_converted}")
    print(f"   DISC (1-10): {disc_converted}")
    print(f"   HEXACO (1-10): {hexaco_converted}")
    print(f"   Soft Skills (1-10): {soft_skills_converted}")
    print()
    
    # === ПРОВЕРКА 7: Генерация PDF ===
    print("📄 Генерация тестового PDF отчета...")
    
    # Обновляем данные сессии для PDF
    session.paei_scores = paei_converted
    session.disc_scores = disc_converted
    session.hexaco_scores = hexaco_converted
    session.soft_skills_scores = soft_skills_converted
    
    try:
        pdf_path = f"test_integration_report_{session.user_name.replace(' ', '_').lower()}.pdf"
        
        from datetime import datetime
        
        generator = EnhancedPDFReportV2()
        
        # Создаем простые интерпретации для теста
        ai_interpretations = {
            "paei": "Тестовая интерпретация PAEI",
            "disc": "Тестовая интерпретация DISC",
            "hexaco": "Тестовая интерпретация HEXACO",
            "soft_skills": "Тестовая интерпретация Soft Skills"
        }
        
        from pathlib import Path
        pdf_path = Path(f"test_integration_report_{session.user_name.replace(' ', '_').lower()}.pdf")
        
        generator.generate_enhanced_report(
            participant_name=session.user_name,
            test_date=datetime.now().strftime("%d.%m.%Y"),
            paei_scores=session.paei_scores,
            disc_scores=session.disc_scores,
            hexaco_scores=session.hexaco_scores,
            soft_skills_scores=session.soft_skills_scores,
            ai_interpretations=ai_interpretations,
            out_path=pdf_path
        )
        
        print(f"✅ PDF отчет успешно создан: {pdf_path}")
        
        # Проверяем размер файла
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path) / 1024  # KB
            print(f"   Размер файла: {file_size:.1f} KB")
        
    except Exception as e:
        print(f"❌ Ошибка при создании PDF: {e}")
        return False
    
    print()
    print("🎉 Тест интеграции завершен успешно!")
    return True

def test_data_consistency():
    """Проверяет консистентность данных между тестами"""
    
    print("🔍 Проверка консистентности данных...")
    print("=" * 40)
    
    # Проверяем структуру вопросов
    errors = []
    
    # PAEI должен иметь варианты ответов
    for i, q in enumerate(PAEI_QUESTIONS):
        if "answers" not in q or len(q["answers"]) != 4:
            errors.append(f"PAEI вопрос {i+1}: неверная структура answers")
    
    # DISC должен иметь варианты ответов
    for i, q in enumerate(DISC_QUESTIONS):
        if "answers" not in q or len(q["answers"]) != 4:
            errors.append(f"DISC вопрос {i+1}: неверная структура answers")
    
    # HEXACO должен иметь текст вопроса
    for i, q in enumerate(HEXACO_QUESTIONS):
        if "question" not in q:
            errors.append(f"HEXACO вопрос {i+1}: отсутствует текст вопроса")
    
    # Soft Skills должен иметь название навыка
    for i, q in enumerate(SOFT_SKILLS_QUESTIONS):
        if "skill" not in q:
            errors.append(f"Soft Skills вопрос {i+1}: отсутствует название навыка")
    
    if errors:
        print("❌ Найдены ошибки в структуре данных:")
        for error in errors:
            print(f"   • {error}")
        return False
    else:
        print("✅ Структура данных всех тестов корректна")
        return True

if __name__ == "__main__":
    print("🧪 ЗАПУСК КОМПЛЕКСНОГО ТЕСТИРОВАНИЯ ИНТЕГРАЦИИ")
    print("=" * 60)
    print()
    
    # Тестируем консистентность данных
    data_ok = test_data_consistency()
    print()
    
    # Тестируем полную интеграцию
    integration_ok = test_complete_integration()
    
    print()
    print("📋 ИТОГОВЫЙ РЕЗУЛЬТАТ:")
    print(f"   Консистентность данных: {'✅ ОК' if data_ok else '❌ ОШИБКА'}")
    print(f"   Интеграция тестов: {'✅ ОК' if integration_ok else '❌ ОШИБКА'}")
    
    if data_ok and integration_ok:
        print()
        print("🎯 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("   Бот готов к полноценному использованию со всеми четырьмя тестами.")
    else:
        print()
        print("⚠️  ОБНАРУЖЕНЫ ПРОБЛЕМЫ!")
        print("   Необходимо исправить ошибки перед использованием.")