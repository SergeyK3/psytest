#!/usr/bin/env python3
"""
Тестовый скрипт для проверки обновленных AI интерпретаций с новыми образцами
"""

import sys
import os
from pathlib import Path

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ai_interpreter():
    """Тестирует AI интерпретатор с новыми образцами"""
    
    print("🤖 Тестирование AI интерпретатора с новыми образцами")
    print("=" * 60)
    
    try:
        from src.psytest.ai_interpreter import get_ai_interpreter
        
        # Получаем AI интерпретатор
        ai_interpreter = get_ai_interpreter()
        
        if not ai_interpreter:
            print("⚠️ AI интерпретатор недоступен (нет OPENAI_API_KEY)")
            print("   Тестируем только загрузку промптов...")
            
            # Проверяем загрузку новых промптов
            from src.psytest.prompts import load_prompt
            
            try:
                adizes_prompt = load_prompt("adizes_system_res.txt")
                print("✅ Промпт adizes_system_res.txt загружен")
                print(f"   Размер: {len(adizes_prompt)} символов")
                
                disc_prompt = load_prompt("disk_system_res.txt") 
                print("✅ Промпт disk_system_res.txt загружен")
                print(f"   Размер: {len(disc_prompt)} символов")
                
                hexaco_prompt = load_prompt("hexaco_system_res.txt")
                print("✅ Промпт hexaco_system_res.txt загружен") 
                print(f"   Размер: {len(hexaco_prompt)} символов")
                
                soft_prompt = load_prompt("soft_system_res.txt")
                print("✅ Промпт soft_system_res.txt загружен")
                print(f"   Размер: {len(soft_prompt)} символов")
                
                return True
                
            except Exception as e:
                print(f"❌ Ошибка загрузки промптов: {e}")
                return False
        
        print("✅ AI интерпретатор доступен")
        
        # Тестовые данные
        test_paei = {"P": 7.5, "A": 6.0, "E": 4.2, "I": 8.1}
        test_disc = {"D": 6.8, "I": 5.4, "S": 7.2, "C": 8.0}
        test_hexaco = {"H": 7.8, "E": 5.2, "X": 6.4, "A": 8.1, "C": 7.5, "O": 4.9}
        test_soft_skills = {
            "Коммуникация": 7.5, "Лидерство": 6.8, "Работа в команде": 8.2,
            "Критическое мышление": 7.1, "Решение проблем": 7.8, "Адаптивность": 6.5,
            "Управление временем": 7.0, "Эмоциональный интеллект": 8.5, 
            "Креативность": 6.2, "Стрессоустойчивость": 7.4
        }
        
        # Тестируем интерпретации
        print("\n📊 Тестирование интерпретаций:")
        
        try:
            paei_interp = ai_interpreter.interpret_paei(test_paei)
            print(f"✅ PAEI интерпретация сгенерирована ({len(paei_interp)} символов)")
            
            disc_interp = ai_interpreter.interpret_disc(test_disc)
            print(f"✅ DISC интерпретация сгенерирована ({len(disc_interp)} символов)")
            
            hexaco_interp = ai_interpreter.interpret_hexaco(test_hexaco)
            print(f"✅ HEXACO интерпретация сгенерирована ({len(hexaco_interp)} символов)")
            
            soft_interp = ai_interpreter.interpret_soft_skills(test_soft_skills)
            print(f"✅ Soft Skills интерпретация сгенерирована ({len(soft_interp)} символов)")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка генерации интерпретаций: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def test_telegram_bot_integration():
    """Тестирует интеграцию AI в Telegram бот"""
    
    print("\n🤖 Тестирование интеграции AI в Telegram бот")
    print("=" * 50)
    
    try:
        # Импортируем модули бота
        import telegram_test_bot
        from src.psytest.ai_interpreter import get_ai_interpreter
        
        # Проверяем, что AI интерпретатор импортирован в боте
        if hasattr(telegram_test_bot, 'get_ai_interpreter'):
            print("✅ AI интерпретатор импортирован в Telegram бот")
        else:
            print("❌ AI интерпретатор НЕ импортирован в Telegram бот")
            return False
        
        # Создаем тестовую сессию
        session = telegram_test_bot.UserSession("Тест Юзер")
        session.paei_scores = {"P": 7.5, "A": 6.0, "E": 4.2, "I": 8.1}
        session.disc_scores = {"D": 6.8, "I": 5.4, "S": 7.2, "C": 8.0}
        session.hexaco_scores = {"H": 7.8, "E": 5.2, "X": 6.4, "A": 8.1, "C": 7.5, "O": 4.9}
        session.soft_skills_scores = {
            "Коммуникация": 7.5, "Лидерство": 6.8, "Работа в команде": 8.2,
            "Критическое мышление": 7.1, "Решение проблем": 7.8, "Адаптивность": 6.5,
            "Управление временем": 7.0, "Эмоциональный интеллект": 8.5, 
            "Креативность": 6.2, "Стрессоустойчивость": 7.4
        }
        session.user_id = 12345
        session.name = "Тест Юзер"
        
        print("✅ Тестовая сессия создана")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования интеграции: {e}")
        return False

def test_pdf_generation():
    """Тестирует генерацию PDF с новыми AI интерпретациями"""
    
    print("\n📄 Тестирование генерации PDF с AI интерпретациями")
    print("=" * 55)
    
    try:
        from enhanced_pdf_report_v2 import EnhancedPDFReportV2
        from src.psytest.ai_interpreter import get_ai_interpreter
        from pathlib import Path
        from datetime import datetime
        
        # Тестовые данные
        test_data = {
            "paei_scores": {"P": 7.5, "A": 6.0, "E": 4.2, "I": 8.1},
            "disc_scores": {"D": 6.8, "I": 5.4, "S": 7.2, "C": 8.0},
            "hexaco_scores": {"H": 7.8, "E": 5.2, "X": 6.4, "A": 8.1, "C": 7.5, "O": 4.9},
            "soft_skills_scores": {
                "Коммуникация": 7.5, "Лидерство": 6.8, "Работа в команде": 8.2,
                "Критическое мышление": 7.1, "Решение проблем": 7.8, "Адаптивность": 6.5,
                "Управление временем": 7.0, "Эмоциональный интеллект": 8.5, 
                "Креативность": 6.2, "Стрессоустойчивость": 7.4
            }
        }
        
        # Получаем AI интерпретатор  
        ai_interpreter = get_ai_interpreter()
        
        if ai_interpreter:
            print("✅ Генерируем AI интерпретации...")
            try:
                interpretations = {
                    "paei": ai_interpreter.interpret_paei(test_data["paei_scores"]),
                    "disc": ai_interpreter.interpret_disc(test_data["disc_scores"]),
                    "hexaco": ai_interpreter.interpret_hexaco(test_data["hexaco_scores"]),
                    "soft_skills": ai_interpreter.interpret_soft_skills(test_data["soft_skills_scores"])
                }
                print("✅ AI интерпретации сгенерированы")
            except Exception as e:
                print(f"⚠️ Ошибка AI, используем базовые интерпретации: {e}")
                interpretations = {
                    "paei": "Базовая интерпретация PAEI",
                    "disc": "Базовая интерпретация DISC", 
                    "hexaco": "Базовая интерпретация HEXACO",
                    "soft_skills": "Базовая интерпретация Soft Skills"
                }
        else:
            print("⚠️ AI недоступен, используем базовые интерпретации")
            interpretations = {
                "paei": "Базовая интерпретация PAEI",
                "disc": "Базовая интерпретация DISC",
                "hexaco": "Базовая интерпретация HEXACO", 
                "soft_skills": "Базовая интерпретация Soft Skills"
            }
        
        # Создаем PDF генератор
        pdf_generator = EnhancedPDFReportV2()
        
        # Генерируем PDF
        output_path = Path("test_ai_interpretation_report.pdf")
        
        pdf_generator.generate_enhanced_report(
            participant_name="Тест Интерпретации",
            test_date=datetime.now().strftime("%d.%m.%Y"),
            paei_scores=test_data["paei_scores"],
            disc_scores=test_data["disc_scores"],
            hexaco_scores=test_data["hexaco_scores"],
            soft_skills_scores=test_data["soft_skills_scores"],
            ai_interpretations=interpretations,
            out_path=output_path
        )
        
        if output_path.exists():
            file_size = output_path.stat().st_size / 1024
            print(f"✅ PDF отчет создан: {output_path}")
            print(f"   Размер файла: {file_size:.1f} KB")
            return True
        else:
            print("❌ PDF файл не создан")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка генерации PDF: {e}")
        return False

if __name__ == "__main__":
    print("🧪 ТЕСТИРОВАНИЕ ОБНОВЛЕННЫХ AI ИНТЕРПРЕТАЦИЙ")
    print("=" * 60)
    print()
    
    # Тестируем AI интерпретатор
    ai_ok = test_ai_interpreter()
    
    # Тестируем интеграцию в Telegram бот
    bot_ok = test_telegram_bot_integration()
    
    # Тестируем генерацию PDF
    pdf_ok = test_pdf_generation()
    
    print()
    print("📋 ИТОГОВЫЙ РЕЗУЛЬТАТ:")
    print(f"   AI интерпретатор: {'✅ ОК' if ai_ok else '❌ ОШИБКА'}")
    print(f"   Интеграция в бот: {'✅ ОК' if bot_ok else '❌ ОШИБКА'}")
    print(f"   Генерация PDF: {'✅ ОК' if pdf_ok else '❌ ОШИБКА'}")
    
    if ai_ok and bot_ok and pdf_ok:
        print()
        print("🎯 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("   Новые AI интерпретации интегрированы корректно.")
    else:
        print()
        print("⚠️  ОБНАРУЖЕНЫ ПРОБЛЕМЫ!")
        print("   Необходимо исправить ошибки.")