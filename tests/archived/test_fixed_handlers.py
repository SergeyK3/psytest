#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест исправленных функций обработки ответов бота
"""

# Имитируем основные структуры бота
class MockSession:
    def __init__(self):
        self.soft_skills_scores = []
        self.hexaco_scores = []
        self.current_question = 0

class MockUpdate:
    def __init__(self, text):
        self.message = MockMessage(text)
        self.effective_user = MockUser()

class MockMessage:
    def __init__(self, text):
        self.text = text
    
    async def reply_text(self, text):
        print(f"🤖 Bot reply: {text}")

class MockUser:
    def __init__(self):
        self.id = 12345

# Имитируем состояния
SOFT_SKILLS_TESTING = 5
HEXACO_TESTING = 6

# Имитируем функции
async def ask_soft_skills_question(update, context):
    print("🔄 Переход к следующему вопросу Soft Skills")
    return SOFT_SKILLS_TESTING

async def ask_hexaco_question(update, context):
    print("🔄 Переход к следующему вопросу HEXACO")
    return HEXACO_TESTING

async def cancel(update, context):
    print("🚪 Обработка команды выхода")
    return -1

# Имитируем сессии пользователей
user_sessions = {12345: MockSession()}

# Импортируем исправленные функции из реального кода (упрощенная версия)
async def handle_soft_skills_answer_fixed(update, context):
    """Исправленная версия обработки ответов Soft Skills"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    answer_text = update.message.text
    
    # Проверяем на выход
    if answer_text == "❌ Выйти":
        return await cancel(update, context)
    
    # Извлекаем числовой ответ (1-5)
    try:
        score = None
        for i in range(1, 6):  # Проверяем цифры 1-5
            if answer_text.startswith(str(i)):
                score = i
                break
                
        if score is not None:
            # Сохраняем ответ в список
            session.soft_skills_scores.append(score)
            session.current_question += 1
            return await ask_soft_skills_question(update, context)
        else:
            raise ValueError("Неверный формат ответа")
            
    except (ValueError, IndexError):
        await update.message.reply_text("❗ Пожалуйста, выберите один из предложенных вариантов (1-5)")
        return SOFT_SKILLS_TESTING

async def handle_hexaco_answer_fixed(update, context):
    """Исправленная версия обработки ответов HEXACO"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    answer_text = update.message.text
    
    # Проверяем на выход
    if answer_text == "❌ Выйти":
        return await cancel(update, context)
    
    # Извлекаем числовой ответ (1-5)
    try:
        score = None
        for i in range(1, 6):  # Проверяем цифры 1-5
            if answer_text.startswith(str(i)):
                score = i
                break
                
        if score is not None:
            # Сохраняем ответ в список
            session.hexaco_scores.append(score)
            session.current_question += 1
            return await ask_hexaco_question(update, context)
        else:
            raise ValueError("Неверный формат ответа")
            
    except (ValueError, IndexError):
        await update.message.reply_text("❗ Пожалуйста, выберите один из предложенных вариантов (1-5)")
        return HEXACO_TESTING

async def test_fixed_handlers():
    """Тестирует исправленные обработчики"""
    print("🧪 Тестирование исправленных обработчиков ответов...")
    print("=" * 60)
    
    # Тестовые ответы
    test_answers = [
        "1. Полностью не согласен",
        "3. Обычно воспринимаю критику спокойно", 
        "5. Полностью согласен",
        "❌ Выйти"
    ]
    
    print("📊 Тестируем Soft Skills обработчик:")
    for answer in test_answers:
        print(f"\n📝 Ответ: '{answer}'")
        session = user_sessions[12345]
        session.soft_skills_scores = []  # Сброс
        
        update = MockUpdate(answer)
        result = await handle_soft_skills_answer_fixed(update, None)
        
        if answer != "❌ Выйти":
            print(f"💾 Сохраненные баллы: {session.soft_skills_scores}")
        print(f"🔄 Результат функции: {result}")
    
    print("\n" + "=" * 60)
    print("📊 Тестируем HEXACO обработчик:")
    for answer in test_answers[:3]:  # Без команды выхода для краткости
        print(f"\n📝 Ответ: '{answer}'")
        session = user_sessions[12345]
        session.hexaco_scores = []  # Сброс
        
        update = MockUpdate(answer)
        result = await handle_hexaco_answer_fixed(update, None)
        
        print(f"💾 Сохраненные баллы: {session.hexaco_scores}")
        print(f"🔄 Результат функции: {result}")
    
    print("\n🎯 Тестирование завершено!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_fixed_handlers())