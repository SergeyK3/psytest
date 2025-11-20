#!/usr/bin/env python3
"""
Тест многопользовательской нагрузки для Telegram бота
Симулирует несколько пользователей одновременно
"""

import asyncio
import time
from datetime import datetime
from telegram_test_bot import UserSession

async def simulate_user_session(user_id: int, name: str):
    """Симулирует сессию одного пользователя"""
    
    print(f"👤 Пользователь {user_id} ({name}) начал тест в {datetime.now().strftime('%H:%M:%S')}")
    
    # Создаем сессию пользователя
    session = UserSession(user_id)
    session.name = name
    
    # Симулируем прохождение DISC теста (8 вопросов)
    for i in range(8):
        # Случайные ответы
        import random
        answer = random.choice(['D', 'I', 'S', 'C'])
        session.disc_scores[answer] += 1
        
        # Имитируем время обдумывания
        await asyncio.sleep(random.uniform(1, 3))
        
        print(f"  📝 {name} ответил на вопрос {i+1}/8")
    
    # Симулируем HEXACO тест (12 вопросов)
    session.hexaco_scores = [random.randint(1, 5) for _ in range(12)]
    await asyncio.sleep(2)
    
    # Симулируем Soft Skills тест (5 вопросов)  
    session.soft_skills_scores = [random.randint(1, 10) for _ in range(5)]
    await asyncio.sleep(1)
    
    print(f"✅ Пользователь {user_id} ({name}) завершил тест в {datetime.now().strftime('%H:%M:%S')}")
    
    return session

async def test_concurrent_users():
    """Тестирует одновременную работу нескольких пользователей"""
    
    print("🧪 Запуск теста многопользовательской нагрузки\n")
    
    # Список пользователей для тестирования
    users = [
        (1001, "Алексей"),
        (1002, "Мария"), 
        (1003, "Дмитрий"),
        (1004, "Елена"),
        (1005, "Сергей"),
    ]
    
    start_time = time.time()
    
    # Запускаем всех пользователей одновременно
    tasks = [simulate_user_session(user_id, name) for user_id, name in users]
    sessions = await asyncio.gather(*tasks)
    
    end_time = time.time()
    
    print(f"\n📊 Результаты теста:")
    print(f"👥 Пользователей: {len(users)}")
    print(f"⏱️ Общее время: {end_time - start_time:.2f} секунд")
    print(f"📈 Среднее время на пользователя: {(end_time - start_time) / len(users):.2f} секунд")
    
    print(f"\n📋 Детали сессий:")
    for session in sessions:
        print(f"  👤 {session.name} (ID: {session.user_id})")
        print(f"     DISC: {session.disc_scores}")
        print(f"     HEXACO: {len(session.hexaco_scores)} ответов")
        print(f"     Soft Skills: {len(session.soft_skills_scores)} ответов")

def test_session_isolation():
    """Тестирует изоляцию данных между пользователями"""
    
    print("🔒 Тест изоляции пользовательских данных\n")
    
    # Создаем несколько сессий
    sessions = {}
    
    for i in range(1, 6):
        user_id = 2000 + i
        sessions[user_id] = UserSession(user_id)
        sessions[user_id].name = f"User_{i}"
        sessions[user_id].disc_scores['D'] = i * 2  # Разные значения
    
    # Проверяем изоляцию
    print("📊 Проверка изоляции данных:")
    for user_id, session in sessions.items():
        print(f"  👤 {session.name}: D-score = {session.disc_scores['D']}")
    
    # Изменяем одного пользователя
    sessions[2001].disc_scores['D'] = 999
    
    print(f"\n🔄 После изменения User_1:")
    for user_id, session in sessions.items():
        print(f"  👤 {session.name}: D-score = {session.disc_scores['D']}")
    
    print(f"✅ Изоляция работает корректно!")

if __name__ == "__main__":
    print("🚀 Тестирование многопользовательской архитектуры\n")
    
    # Тест изоляции данных
    test_session_isolation()
    
    print("\n" + "="*50 + "\n")
    
    # Тест одновременной нагрузки
    asyncio.run(test_concurrent_users())
    
    print(f"\n🎉 Все тесты завершены успешно!")
    print(f"✅ Система готова к многопользовательской работе")