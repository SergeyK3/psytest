#!/usr/bin/env python3
"""
Краткий тест нового функционала в боте
"""

import asyncio
from datetime import datetime
from pathlib import Path
from telegram_test_bot import UserSession, generate_user_report
from bot_integration_example import UserAnswersCollector

def test_dual_report_generation():
    """Тест генерации двух типов отчетов в боте"""
    
    print("🧪 Тест нового функционала бота: два типа отчетов")
    print("=" * 55)
    
    # Создаем тестовую сессию
    user_id = 123456789
    session = UserSession(user_id)
    session.name = "Тестовый Пользователь"
    
    # Заполняем тестовые результаты (правильные форматы)
    session.paei_scores = {"P": 4, "A": 3, "E": 4, "I": 2}
    session.disc_scores = {"D": 8, "I": 6, "S": 5, "C": 7}
    session.hexaco_scores = {"H": 4.2, "E": 3.8, "X": 4.5, "A": 4.1, "C": 3.9, "O": 4.3}
    # Soft Skills должен быть словарем навыков
    soft_skills_names = ["Коммуникация", "Лидерство", "Работа в команде", "Решение проблем", 
                        "Адаптивность", "Креативность", "Эмоциональный интеллект", 
                        "Управление временем", "Критическое мышление", "Стрессоустойчивость"]
    session.soft_skills_scores = {skill: 5 + i % 5 for i, skill in enumerate(soft_skills_names)}
    
    # Добавляем тестовые ответы в коллектор
    session.answers_collector.add_paei_answer(0, "4 - Полностью согласен")
    session.answers_collector.add_paei_answer(1, "3 - Скорее согласен")
    session.answers_collector.add_disc_answer(0, 4)
    session.answers_collector.add_disc_answer(1, 3)
    session.answers_collector.add_soft_skills_answer(0, 4)
    session.answers_collector.add_hexaco_answer(0, 4)
    
    print("📋 Тестовая сессия создана:")
    print(f"   ├─ Пользователь: {session.name}")
    print(f"   ├─ User ID: {user_id}")
    print(f"   ├─ PAEI результаты: {session.paei_scores}")
    print(f"   ├─ DISC результаты: {session.disc_scores}")
    print(f"   └─ Собранные ответы: {len(session.answers_collector.get_answers_dict())} записей")
    
    try:
        # Запускаем генерацию отчетов
        print(f"\n⚙️  Запуск generate_user_report...")
        pdf_path_user, pdf_path_gdrive = generate_user_report(session)
        
        print(f"\n✅ Функция вернула два пути:")
        print(f"   📱 Для пользователя: {pdf_path_user}")
        print(f"   ☁️  Для Google Drive: {pdf_path_gdrive}")
        
        # Проверяем, что файлы существуют
        user_exists = Path(pdf_path_user).exists()
        gdrive_exists = Path(pdf_path_gdrive).exists()
        
        print(f"\n📁 Проверка файлов:")
        print(f"   📱 Пользовательский отчет: {'✅ Существует' if user_exists else '❌ Не найден'}")
        print(f"   ☁️  Полный отчет: {'✅ Существует' if gdrive_exists else '❌ Не найден'}")
        
        if user_exists and gdrive_exists:
            print(f"\n🎯 УСПЕХ! Новый функционал работает корректно!")
            print(f"   📏 Размер пользовательского отчета: {Path(pdf_path_user).stat().st_size} байт")
            print(f"   📏 Размер полного отчета: {Path(pdf_path_gdrive).stat().st_size} байт")
            
            # Полный отчет должен быть больше пользовательского из-за раздела вопросов
            if Path(pdf_path_gdrive).stat().st_size > Path(pdf_path_user).stat().st_size:
                print(f"   ✅ Полный отчет больше пользовательского (как и ожидалось)")
            else:
                print(f"   ⚠️  Размеры отчетов одинаковые - нужно проверить")
        else:
            print(f"\n❌ ОШИБКА! Не все файлы созданы")
            
    except Exception as e:
        print(f"\n❌ ОШИБКА при генерации: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dual_report_generation()