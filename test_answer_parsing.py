#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест парсинга ответов в различных форматах
"""

def test_answer_parsing():
    """Тестирует логику парсинга ответов в стиле telegram бота"""
    
    test_answers = [
        "1. Полностью не согласен",
        "2. Скорее не согласен", 
        "3. Обычно воспринимаю критику спокойно",
        "4. Скорее согласен",
        "5. Полностью согласен"
    ]
    
    print("🧪 Тестируем парсинг ответов...")
    print("=" * 50)
    
    for answer_text in test_answers:
        print(f"📝 Тестируем ответ: '{answer_text}'")
        
        # Проверяем на выход
        if answer_text == "❌ Выйти":
            print("🚪 Обнаружена команда выхода")
            continue
        
        # Извлекаем числовой ответ (1-5)
        try:
            score = None
            for i in range(1, 6):  # Проверяем цифры 1-5
                if answer_text.startswith(str(i)):
                    score = i
                    break
                    
            if score is not None:
                print(f"✅ Извлечен балл: {score}")
            else:
                print(f"❌ Не удалось извлечь балл из: '{answer_text}'")
                
        except (ValueError, IndexError) as e:
            print(f"❌ Ошибка парсинга: {e}")
        
        print("-" * 30)
    
    print("\n🎯 Тест завершен!")

if __name__ == "__main__":
    test_answer_parsing()