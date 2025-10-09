#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование улучшенных промптов для DISC и ADIZES с загрузкой .env
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Загружаем переменные окружения из .env файла
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Переменные из .env файла загружены")
except ImportError:
    print("⚠️ python-dotenv не установлен, пробуем загрузить .env вручную")
    # Простая загрузка .env файла
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        print("✅ .env файл загружен вручную")

from psytest.ai_interpreter import AIInterpreter

def test_disc_with_api():
    """Тестируем DISC с реальным API"""
    print("\n🧪 ТЕСТИРОВАНИЕ DISC С OPENAI API")
    print("=" * 50)
    
    try:
        ai_interpreter = AIInterpreter()
        print("✅ AI интерпретатор успешно инициализирован")
        
        # Тест 1: Доминирующий D (как на диаграмме пользователя)
        test_data = {
            "1.1": 4, "1.2": 4,  # D=8
            "2.1": 1, "2.2": 1,  # I=2  
            "3.1": 2, "3.2": 2,  # S=4
            "4.1": 1, "4.2": 1   # C=2
        }
        
        print(f"\n🔍 Тестируем доминирующий D профиль:")
        print(f"Данные: {test_data}")
        
        interpretation = ai_interpreter.interpret_disc(test_data)
        print(f"\n📝 Интерпретация получена (длина: {len(interpretation)} символов)")
        print(f"\n💡 Результат:")
        print("-" * 60)
        print(interpretation)
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_adizes_with_api():
    """Тестируем ADIZES с реальным API"""
    print("\n\n🧪 ТЕСТИРОВАНИЕ ADIZES С OPENAI API")
    print("=" * 50)
    
    try:
        ai_interpreter = AIInterpreter()
        
        # Тест: Доминирующий A (как на диаграмме пользователя)
        test_choices = ["A", "A", "A", "P"]
        
        print(f"\n🔍 Тестируем доминирующий A профиль:")
        print(f"Выборы: {test_choices}")
        
        interpretation = ai_interpreter.interpret_adizes(test_choices)
        print(f"\n📝 Интерпретация получена (длина: {len(interpretation)} символов)")
        print(f"\n💡 Результат:")
        print("-" * 60)
        print(interpretation)
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def check_api_key():
    """Проверяем наличие API ключа"""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OpenAI API ключ найден (длина: {len(api_key)} символов)")
        print(f"🔑 Начинается с: {api_key[:10]}...")
        return True
    else:
        print("❌ OpenAI API ключ не найден в переменных окружения")
        return False

if __name__ == "__main__":
    print("🚀 ТЕСТИРОВАНИЕ УЛУЧШЕННЫХ ПРОМПТОВ С OPENAI API")
    print("=" * 70)
    
    # Проверяем API ключ
    if not check_api_key():
        print("\n❌ Не удается найти OpenAI API ключ. Завершение.")
        exit(1)
    
    try:
        # Тестируем DISC
        disc_success = test_disc_with_api()
        
        # Тестируем ADIZES
        adizes_success = test_adizes_with_api()
        
        print(f"\n\n🎉 ИТОГИ ТЕСТИРОВАНИЯ:")
        print(f"DISC: {'✅ Успешно' if disc_success else '❌ Ошибка'}")
        print(f"ADIZES: {'✅ Успешно' if adizes_success else '❌ Ошибка'}")
        
        if disc_success and adizes_success:
            print("\n🎊 Все тесты прошли успешно! Улучшенные промпты работают отлично!")
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()