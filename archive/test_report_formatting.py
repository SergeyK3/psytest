#!/usr/bin/env python3
"""
Тестовый скрипт для быстрого тестирования форматирования PDF отчета
Использует фиксированные ответы для генерации отчета без прохождения теста
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent / "src"))

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from oauth_google_drive import upload_to_google_drive_oauth

def get_test_answers():
    """Возвращает фиксированные тестовые ответы для быстрого тестирования"""
    
    # Тестовые ответы PAEI (Адизес)
    paei_answers = {
        '0': 'P',  # Вопрос 1: Producer
        '1': 'A',  # Вопрос 2: Administrator  
        '2': 'E',  # Вопрос 3: Entrepreneur
        '3': 'I',  # Вопрос 4: Integrator
        '4': 'P'   # Вопрос 5: Producer
    }
    
    # Тестовые ответы DISC (8 вопросов по 2 на категорию)
    disc_answers = {
        '0': 5,  # D1: Решительный
        '1': 4,  # D2: Властный
        '2': 3,  # I1: Общительный
        '3': 4,  # I2: Влиятельный
        '4': 2,  # S1: Стабильный
        '5': 3,  # S2: Поддерживающий
        '6': 4,  # C1: Точный
        '7': 5   # C2: Соблюдающий правила
    }
    
    # Тестовые ответы Soft Skills (10 вопросов)
    soft_skills_answers = {
        '0': 4,  # Коммуникация
        '1': 5,  # Лидерство
        '2': 3,  # Работа в команде
        '3': 4,  # Адаптивность
        '4': 5,  # Критическое мышление
        '5': 3,  # Управление временем
        '6': 4,  # Эмоциональный интеллект
        '7': 5,  # Решение проблем
        '8': 4,  # Креативность
        '9': 3   # Стрессоустойчивость
    }
    
    # Тестовые ответы HEXACO (6 вопросов)
    hexaco_answers = {
        '0': 4,  # Честность-Скромность
        '1': 3,  # Эмоциональность
        '2': 5,  # Экстраверсия
        '3': 4,  # Доброжелательность
        '4': 3,  # Добросовестность
        '5': 4   # Открытость опыту
    }
    
    return {
        'PAEI': paei_answers,
        'DISC': disc_answers,
        'SOFT_SKILLS': soft_skills_answers,
        'HEXACO': hexaco_answers
    }

def create_test_user_data():
    """Создает тестовые данные пользователя"""
    return {
        'first_name': 'Тестовый',
        'last_name': 'Пользователь',
        'telegram_id': 'test_user',
        'username': 'test_format'
    }

def test_user_report():
    """Генерирует пользовательский отчет (краткий)"""
    print("🔬 Генерация пользовательского отчета (краткий формат)...")
    
    user_data = create_test_user_data()
    answers = get_test_answers()
    
    # Генерируем timestamp для имени файла
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    user_filename = f"{timestamp}_TEST_USER_report.pdf"
    
    try:
        from pathlib import Path
        
        generator = EnhancedPDFReportV2(include_questions_section=False)
        
        # Преобразуем ответы в нужный формат
        paei_scores = {'P': 2, 'A': 1, 'E': 1, 'I': 1}  # Подсчет на основе ответов
        disc_scores = {'D': 4.5, 'I': 3.5, 'S': 2.5, 'C': 4.5}  # Средние значения
        hexaco_scores = {'H': 4, 'E': 3, 'eX': 5, 'A': 4, 'C': 3, 'O': 4}
        soft_skills_scores = {
            'Communication': 4, 'Leadership': 5, 'Teamwork': 3,
            'Adaptability': 4, 'Critical Thinking': 5, 'Time Management': 3,
            'Emotional Intelligence': 4, 'Problem Solving': 5,
            'Creativity': 4, 'Stress Management': 3
        }
        
        generator.generate_enhanced_report(
            participant_name=f"{user_data['first_name']} {user_data['last_name']}",
            test_date=timestamp,
            paei_scores=paei_scores,
            disc_scores=disc_scores,
            hexaco_scores=hexaco_scores,
            soft_skills_scores=soft_skills_scores,
            ai_interpretations={},
            out_path=Path(user_filename),
            user_answers=None  # Краткий отчет без ответов
        )
        
        print(f"✅ Пользовательский отчет создан: {user_filename}")
        
        # Загружаем в Google Drive
        print("📤 Загружаем отчет в Google Drive...")
        gdrive_link = upload_to_google_drive_oauth(user_filename)
        
        if gdrive_link:
            print(f"🎉 Отчет загружен в Google Drive: {gdrive_link}")
        else:
            print("⚠️ Не удалось загрузить в Google Drive")
        
        return user_filename
        
    except Exception as e:
        print(f"❌ Ошибка создания пользовательского отчета: {e}")
        return None

def test_full_report():
    """Генерирует полный отчет (с деталями вопросов)"""
    print("🔬 Генерация полного отчета (с деталями вопросов)...")
    
    user_data = create_test_user_data()
    answers = get_test_answers()
    
    # Генерируем timestamp для имени файла
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    full_filename = f"{timestamp}_TEST_FULL_report.pdf"
    
    try:
        from pathlib import Path
        
        generator = EnhancedPDFReportV2(include_questions_section=True)
        
        # Преобразуем ответы в нужный формат
        paei_scores = {'P': 2, 'A': 1, 'E': 1, 'I': 1}  # Подсчет на основе ответов
        disc_scores = {'D': 4.5, 'I': 3.5, 'S': 2.5, 'C': 4.5}  # Средние значения
        hexaco_scores = {'H': 4, 'E': 3, 'eX': 5, 'A': 4, 'C': 3, 'O': 4}
        soft_skills_scores = {
            'Communication': 4, 'Leadership': 5, 'Teamwork': 3,
            'Adaptability': 4, 'Critical Thinking': 5, 'Time Management': 3,
            'Emotional Intelligence': 4, 'Problem Solving': 5,
            'Creativity': 4, 'Stress Management': 3
        }
        
        generator.generate_enhanced_report(
            participant_name=f"{user_data['first_name']} {user_data['last_name']}",
            test_date=timestamp,
            paei_scores=paei_scores,
            disc_scores=disc_scores,
            hexaco_scores=hexaco_scores,
            soft_skills_scores=soft_skills_scores,
            ai_interpretations={},
            out_path=Path(full_filename),
            user_answers=answers  # Полный отчет с деталями ответов
        )
        
        print(f"✅ Полный отчет создан: {full_filename}")
        
        # Загружаем в Google Drive
        print("📤 Загружаем отчет в Google Drive...")
        gdrive_link = upload_to_google_drive_oauth(full_filename)
        
        if gdrive_link:
            print(f"🎉 Отчет загружен в Google Drive: {gdrive_link}")
        else:
            print("⚠️ Не удалось загрузить в Google Drive")
        
        return full_filename
        
    except Exception as e:
        print(f"❌ Ошибка создания полного отчета: {e}")
        return None

def test_both_reports():
    """Генерирует оба типа отчета для сравнения"""
    print("🎯 Тестирование форматирования отчетов")
    print("=" * 50)
    
    # Генерируем пользовательский отчет
    user_file = test_user_report()
    print()
    
    # Генерируем полный отчет  
    full_file = test_full_report()
    print()
    
    print("📋 Результаты тестирования:")
    print("-" * 30)
    
    if user_file and os.path.exists(user_file):
        print(f"📄 Пользовательский отчет: {user_file}")
        print(f"📏 Размер: {os.path.getsize(user_file)} байт")
    else:
        print("❌ Пользовательский отчет не создан")
    
    if full_file and os.path.exists(full_file):
        print(f"📄 Полный отчет: {full_file}")
        print(f"📏 Размер: {os.path.getsize(full_file)} байт")
    else:
        print("❌ Полный отчет не создан")
    
    print()
    print("🔍 Что проверить в отчетах:")
    print("• Расположение элементов на первой странице")
    print("• Размеры и пропорции диаграмм") 
    print("• Читаемость текста и отступы")
    print("• Переносы на вторую страницу")
    print("• Общий внешний вид и компоновку")

def quick_user_report():
    """Быстрая генерация только пользовательского отчета"""
    return test_user_report()

def quick_full_report():
    """Быстрая генерация только полного отчета"""
    return test_full_report()

if __name__ == "__main__":
    print("🧪 Тестовый генератор отчетов для проверки форматирования")
    print("Использует фиксированные ответы для быстрого тестирования")
    print()
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == 'user':
            quick_user_report()
        elif mode == 'full':
            quick_full_report()
        elif mode == 'both':
            test_both_reports()
        else:
            print("❓ Использование:")
            print("  python test_report_formatting.py user   # Только пользовательский отчет")
            print("  python test_report_formatting.py full   # Только полный отчет") 
            print("  python test_report_formatting.py both   # Оба отчета")
    else:
        # По умолчанию генерируем оба отчета
        test_both_reports()