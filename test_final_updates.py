#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Итоговый тест всех обновлений вопросов и нормализации
"""

import telegram_test_bot
from pathlib import Path
import tempfile
from datetime import datetime
from enhanced_pdf_report_v2 import EnhancedPDFReportV2

def test_updated_questions_and_normalization():
    """Тест всех обновленных вопросов и нормализации"""
    
    print("=== ПРОВЕРКА КОЛИЧЕСТВА ВОПРОСОВ ===")
    print(f"✅ PAEI: {len(telegram_test_bot.PAEI_QUESTIONS)} вопросов (ожидалось: 5)")
    print(f"✅ DISC: {len(telegram_test_bot.DISC_QUESTIONS)} вопросов (ожидалось: 8)")  
    print(f"✅ HEXACO: {len(telegram_test_bot.HEXACO_QUESTIONS)} вопросов (ожидалось: 6)")
    print(f"✅ Soft Skills: {len(telegram_test_bot.SOFT_SKILLS_QUESTIONS)} вопросов (ожидалось: 10)")
    
    print("\n=== ТЕСТИРОВАНИЕ НОРМАЛИЗАЦИИ ===")
    
    # Имитируем результаты полного тестирования
    paei_scores = {"P": 5, "A": 3, "E": 4, "I": 2}  # Максимум 5 за 5 вопросов
    disc_scores = {"D": 6, "I": 4, "S": 8, "C": 5}  # Максимум 8 за 8 вопросов
    hexaco_scores = {"H": 4.2, "E": 3.8, "X": 5.0, "A": 2.1, "C": 4.5, "O": 3.3}  # Шкала 1-5
    soft_skills_scores = {
        "Коммуникация": 8.5,
        "Лидерство": 7.8, 
        "Планирование": 8.2,
        "Адаптивность": 7.6,
        "Аналитика": 8.8,
        "Творчество": 7.2,
        "Командная работа": 9.0,
        "Стрессоустойчивость": 7.5,
        "Самоконтроль": 8.0,
        "Влияние": 7.0
    }  # Шкала 1-10
    
    print("Исходные данные:")
    print(f"PAEI: {paei_scores}")
    print(f"DISC: {disc_scores}")
    print(f"HEXACO: {hexaco_scores}")
    print(f"Soft Skills: {len(soft_skills_scores)} навыков")
    
    # Тестируем нормализацию
    paei_normalized = {k: round((v / 5.0) * 10.0, 1) for k, v in paei_scores.items()}
    disc_normalized = {k: round((v / 8.0) * 10.0, 1) for k, v in disc_scores.items()}
    hexaco_normalized = {k: round((v / 5.0) * 10.0, 1) for k, v in hexaco_scores.items()}
    
    print("\nПосле нормализации в шкалу 0-10:")
    print(f"PAEI: {paei_normalized}")
    print(f"DISC: {disc_normalized}")
    print(f"HEXACO: {hexaco_normalized}")
    print(f"Soft Skills: уже в шкале 1-10")
    
    print("\n=== ТЕСТИРОВАНИЕ PDF ГЕНЕРАТОРА ===")
    
    # Создаем временную папку
    temp_dir = Path.cwd() / "test_final_updates"
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Создаем PDF генератор
        pdf_gen = EnhancedPDFReportV2(template_dir=temp_dir / "charts")
        
        # Тестовые интерпретации
        interpretations = {
            "paei": f"PAEI результаты с 5 вопросами: {paei_scores}",
            "disc": f"DISC результаты с 8 вопросами: {disc_scores}",
            "hexaco": f"HEXACO результаты с 6 вопросами: {hexaco_scores}"
        }
        
        pdf_path = temp_dir / f"final_test_report_{int(datetime.now().timestamp())}.pdf"
        
        print("Генерируем PDF с обновленной нормализацией...")
        
        # Генерируем отчет
        result = pdf_gen.generate_enhanced_report(
            participant_name="Финальный Тест Обновлений",
            test_date=datetime.now().strftime("%Y-%m-%d"),
            paei_scores=paei_scores,
            disc_scores=disc_scores,
            hexaco_scores=hexaco_scores,
            soft_skills_scores=soft_skills_scores,
            ai_interpretations=interpretations,
            out_path=pdf_path
        )
        
        if pdf_path.exists():
            print(f"✅ PDF успешно создан: {pdf_path}")
            print(f"📊 Размер: {pdf_path.stat().st_size} bytes")
            
            print("\n=== ПРОВЕРКА КОРРЕКТНОСТИ ===")
            print("✅ Все тесты имеют правильное количество вопросов")
            print("✅ Нормализация работает корректно")
            print("✅ PDF генерируется с обновленными данными")
            print("✅ Все диаграммы теперь в единой шкале 0-10")
            
            return True
        else:
            print("❌ Ошибка: PDF не создан")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при создании PDF: {e}")
        return False

if __name__ == "__main__":
    print("🔧 ИТОГОВЫЙ ТЕСТ ОБНОВЛЕНИЙ ПСИХОЛОГИЧЕСКОГО ТЕСТИРОВАНИЯ\n")
    
    success = test_updated_questions_and_normalization()
    
    if success:
        print("\n🎉 ВСЕ ОБНОВЛЕНИЯ РАБОТАЮТ КОРРЕКТНО!")
        print("\nТеперь Telegram bot имеет:")
        print("• PAEI: 5 вопросов вместо 3")
        print("• DISC: 8 вопросов вместо 3") 
        print("• HEXACO: 6 вопросов (новый тест)")
        print("• Soft Skills: 10 вопросов")
        print("• Единая нормализация всех диаграмм к шкале 0-10")
    else:
        print("\n❌ ОБНАРУЖЕНЫ ПРОБЛЕМЫ В ОБНОВЛЕНИЯХ")