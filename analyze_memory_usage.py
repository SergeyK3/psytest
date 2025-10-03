#!/usr/bin/env python3
"""
Анализ потребления оперативной памяти при многопользовательском режиме
"""

import sys
import psutil
import os
import tracemalloc
from pathlib import Path
import tempfile
from datetime import datetime

# Добавляем путь для импорта
sys.path.append('.')

def get_memory_usage():
    """Получает текущее потребление памяти процессом"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return {
        'rss': memory_info.rss / 1024 / 1024,  # MB
        'vms': memory_info.vms / 1024 / 1024,  # MB
        'percent': process.memory_percent()
    }

def analyze_user_session_memory():
    """Анализирует потребление памяти одной пользовательской сессии"""
    
    print("🔍 Анализ памяти для UserSession...")
    
    # Импортируем после начала трассировки
    from telegram_test_bot import UserSession
    
    tracemalloc.start()
    initial_memory = get_memory_usage()
    
    # Создаем одну сессию пользователя
    user_id = 1001
    session = UserSession(user_id)
    session.name = "Тестовый пользователь для анализа памяти"
    session.phone = "+7-999-123-45-67"
    
    # Заполняем данными как при реальном тестировании
    session.disc_scores = {"D": 5, "I": 3, "S": 2, "C": 4}
    session.hexaco_scores = [4, 3, 5, 2, 4, 3, 5, 4, 2, 3, 4, 5]  # 12 ответов
    session.soft_skills_scores = [7, 8, 6, 9, 5]  # 5 ответов
    session.current_test = "COMPLETED"
    session.current_question = 8
    
    after_session_memory = get_memory_usage()
    
    # Измеряем точное потребление с tracemalloc
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    session_memory = after_session_memory['rss'] - initial_memory['rss']
    
    print(f"📊 Одна пользовательская сессия:")
    print(f"   💾 Память RSS: ~{session_memory:.3f} MB")
    print(f"   📈 Точное потребление: {current / 1024 / 1024:.3f} MB")
    print(f"   🔝 Пиковое потребление: {peak / 1024 / 1024:.3f} MB")
    
    return session_memory

def analyze_pdf_generation_memory():
    """Анализирует потребление памяти при генерации PDF"""
    
    print("\n📄 Анализ памяти для генерации PDF...")
    
    tracemalloc.start()
    initial_memory = get_memory_usage()
    
    try:
        from enhanced_pdf_report_v2 import EnhancedPDFReportV2
        from datetime import datetime
        from pathlib import Path
        
        # Создаем генератор PDF
        pdf_generator = EnhancedPDFReportV2()
        
        # Тестовые данные для PDF
        test_data = {
            'participant_name': 'Тест Памяти',
            'test_date': datetime.now().strftime("%Y-%m-%d"),
            'paei_scores': {
                'Производитель': 7,
                'Администратор': 5,
                'Предприниматель': 8,
                'Интегратор': 6
            },
            'disc_scores': {
                'D (Доминирование)': 6,
                'I (Влияние)': 4,
                'S (Постоянство)': 3,
                'C (Соответствие)': 5
            },
            'hexaco_scores': {
                'Честность-Смирение': 7,
                'Эмоциональность': 6,
                'Экстраверсия': 8,
                'Приятность': 5,
                'Сознательность': 7,
                'Открытость опыту': 6
            },
            'soft_skills_scores': {
                'Коммуникация': 8,
                'Лидерство': 7,
                'Командная работа': 6,
                'Адаптивность': 9,
                'Критическое мышление': 5
            },
            'ai_interpretations': {
                'overall': 'Тестовая интерпретация для анализа памяти ' * 10,
                'disc': 'DISC интерпретация ' * 20,
                'paei': 'PAEI интерпретация ' * 15,
                'hexaco': 'HEXACO интерпретация ' * 25,
                'soft_skills': 'Soft skills интерпретация ' * 18
            },
            'out_path': Path("memory_test_report.pdf")
        }
        
        # Генерируем PDF
        pdf_path = pdf_generator.generate_enhanced_report(**test_data)
        
        after_pdf_memory = get_memory_usage()
        current, peak = tracemalloc.get_traced_memory()
        
        # Проверяем размер созданного файла
        file_size = 0
        if pdf_path and os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path) / 1024 / 1024  # MB
            os.unlink(pdf_path)  # Удаляем тестовый файл
        
        tracemalloc.stop()
        
        pdf_memory = after_pdf_memory['rss'] - initial_memory['rss']
        
        print(f"📊 Генерация одного PDF:")
        print(f"   💾 Память RSS: ~{pdf_memory:.3f} MB")
        print(f"   📈 Точное потребление: {current / 1024 / 1024:.3f} MB")
        print(f"   🔝 Пиковое потребление: {peak / 1024 / 1024:.3f} MB")
        print(f"   📄 Размер PDF файла: {file_size:.3f} MB")
        
        return pdf_memory
        
    except Exception as e:
        tracemalloc.stop()
        print(f"❌ Ошибка при анализе PDF: {e}")
        return 0

def analyze_concurrent_memory():
    """Анализирует потребление памяти при одновременной работе пользователей"""
    
    print("\n👥 Анализ памяти для множественных сессий...")
    
    from telegram_test_bot import UserSession
    
    tracemalloc.start()
    initial_memory = get_memory_usage()
    
    # Создаем несколько пользовательских сессий
    sessions = {}
    user_count = 5
    
    for i in range(1, user_count + 1):
        user_id = 2000 + i
        sessions[user_id] = UserSession(user_id)
        sessions[user_id].name = f"Пользователь_{i}"
        sessions[user_id].phone = f"+7-999-{i:03d}-45-67"
        
        # Заполняем данными
        sessions[user_id].disc_scores = {"D": i, "I": i+1, "S": i+2, "C": i+3}
        sessions[user_id].hexaco_scores = [i % 5 + 1] * 12
        sessions[user_id].soft_skills_scores = [(i % 10) + 1] * 5
    
    after_sessions_memory = get_memory_usage()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    total_memory = after_sessions_memory['rss'] - initial_memory['rss']
    memory_per_user = total_memory / user_count
    
    print(f"📊 {user_count} одновременных сессий:")
    print(f"   💾 Общая память: {total_memory:.3f} MB")
    print(f"   👤 На одного пользователя: {memory_per_user:.3f} MB")
    print(f"   📈 Точное потребление: {current / 1024 / 1024:.3f} MB")
    print(f"   🔝 Пиковое потребление: {peak / 1024 / 1024:.3f} MB")
    
    return memory_per_user

def calculate_load_scenarios():
    """Рассчитывает нагрузку для различных сценариев"""
    
    print("\n🎯 Расчет нагрузки для различных сценариев...")
    
    # Базовые измерения
    session_memory = analyze_user_session_memory()
    pdf_memory = analyze_pdf_generation_memory()
    concurrent_memory_per_user = analyze_concurrent_memory()
    
    # Системная информация
    total_ram = psutil.virtual_memory().total / 1024 / 1024 / 1024  # GB
    available_ram = psutil.virtual_memory().available / 1024 / 1024  # MB
    
    print(f"\n💻 Системная информация:")
    print(f"   🖥️ Общая RAM: {total_ram:.1f} GB")
    print(f"   💾 Доступная RAM: {available_ram:.0f} MB")
    
    # Оценки для разных сценариев
    scenarios = [3, 5, 10, 20, 50, 100]
    
    print(f"\n📈 Оценка потребления памяти:")
    print(f"{'Пользователей':<12} {'Сессии (MB)':<15} {'PDF Gen (MB)':<15} {'Общая (MB)':<15} {'% от RAM':<10}")
    print("-" * 75)
    
    for users in scenarios:
        session_total = concurrent_memory_per_user * users
        pdf_total = pdf_memory * (users * 0.2)  # Предполагаем 20% одновременно генерируют PDF
        total_estimated = session_total + pdf_total
        ram_percent = (total_estimated / available_ram) * 100
        
        print(f"{users:<12} {session_total:<15.1f} {pdf_total:<15.1f} {total_estimated:<15.1f} {ram_percent:<10.1f}%")
    
    # Рекомендации
    print(f"\n💡 Рекомендации:")
    
    safe_users = int(available_ram * 0.3 / (concurrent_memory_per_user + pdf_memory * 0.2))
    optimal_users = int(available_ram * 0.5 / (concurrent_memory_per_user + pdf_memory * 0.2))
    max_users = int(available_ram * 0.8 / (concurrent_memory_per_user + pdf_memory * 0.2))
    
    print(f"   🟢 Безопасная нагрузка (30% RAM): {safe_users} пользователей")
    print(f"   🟡 Оптимальная нагрузка (50% RAM): {optimal_users} пользователей") 
    print(f"   🔴 Максимальная нагрузка (80% RAM): {max_users} пользователей")

def main():
    """Основная функция анализа"""
    
    print("🔬 Анализ потребления оперативной памяти")
    print("=" * 60)
    
    # Начальное состояние
    initial_memory = get_memory_usage()
    print(f"📊 Начальное потребление памяти: {initial_memory['rss']:.1f} MB ({initial_memory['percent']:.1f}%)")
    
    # Проводим анализ
    calculate_load_scenarios()
    
    # Финальное состояние
    final_memory = get_memory_usage()
    print(f"\n📊 Финальное потребление памяти: {final_memory['rss']:.1f} MB ({final_memory['percent']:.1f}%)")
    print(f"📈 Использовано для анализа: {final_memory['rss'] - initial_memory['rss']:.1f} MB")

if __name__ == "__main__":
    main()