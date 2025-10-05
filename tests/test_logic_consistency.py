#!/usr/bin/env python3
"""
Тест обновленной логики AI интерпретации с общим заключением
"""

import sys
from pathlib import Path

# Добавляем путь для импорта
sys.path.append('.')
sys.path.append('./src')

def test_ai_interpreter_logic():
    """Тестируем обновленную логику AI интерпретатора"""
    
    print("🔄 Тестирование обновленной логики AI интерпретатора...")
    
    try:
        from src.psytest.ai_interpreter import AIInterpreter
        
        # Проверяем, что новый метод доступен
        ai = AIInterpreter.__new__(AIInterpreter)  # Создаем без инициализации API
        
        # Проверяем наличие метода interpret_general_conclusion
        if hasattr(ai, 'interpret_general_conclusion'):
            print("✅ Метод interpret_general_conclusion найден")
        else:
            print("❌ Метод interpret_general_conclusion отсутствует")
            return False
            
        # Проверяем другие методы
        methods_to_check = [
            'interpret_paei',
            'interpret_disc', 
            'interpret_hexaco',
            'interpret_soft_skills'
        ]
        
        for method in methods_to_check:
            if hasattr(ai, method):
                print(f"✅ Метод {method} найден")
            else:
                print(f"❌ Метод {method} отсутствует")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при проверке AI интерпретатора: {e}")
        return False

def test_prompt_files():
    """Тестируем файлы промптов"""
    
    print("\n🔄 Тестирование файлов промптов...")
    
    prompt_files = [
        "adizes_system_res.txt",
        "disk_system_res.txt", 
        "soft_system_res.txt",
        "hexaco_system_res.txt",
        "general_system_res.txt"
    ]
    
    prompts_dir = Path("data/prompts")
    
    for prompt_file in prompt_files:
        prompt_path = prompts_dir / prompt_file
        
        if prompt_path.exists():
            try:
                content = prompt_path.read_text(encoding="utf-8")
                
                # Проверяем, что нет лишнего Python кода
                if "system_res_" in content or "'''" in content:
                    print(f"⚠️  {prompt_file}: содержит лишний Python код")
                else:
                    print(f"✅ {prompt_file}: корректный формат")
                    
                # Проверяем минимальную длину
                if len(content.strip()) < 200:
                    print(f"⚠️  {prompt_file}: слишком короткий контент ({len(content.strip())} символов)")
                    
            except Exception as e:
                print(f"❌ {prompt_file}: ошибка чтения - {e}")
        else:
            print(f"❌ {prompt_file}: файл не найден")

def test_telegram_bot_integration():
    """Тестируем интеграцию с telegram bot"""
    
    print("\n🔄 Тестирование интеграции с Telegram ботом...")
    
    try:
        from telegram_test_bot import generate_user_report, UserSession
        
        # Создаем тестовую сессию
        session = UserSession(12345)
        session.name = "Test User"
        session.paei_scores = {"Производитель": 8, "Администратор": 5, "Предприниматель": 7, "Интегратор": 6}
        session.disc_scores = {"D": 7, "I": 5, "S": 3, "C": 4}
        session.hexaco_scores = {"Честность-Скромность": 4, "Эмоциональность": 3, "Экстраверсия": 5, "Дружелюбие": 4, "Сознательность": 5, "Открытость опыту": 3}
        session.soft_skills_scores = {"Лидерство": 8, "Коммуникация": 7, "Критическое мышление": 6, "Управление временем": 7, "Разрешение конфликтов": 8, "Адаптивность": 6, "Эмоциональный интеллект": 7, "Навыки развития": 6}
        
        print("✅ Тестовая сессия создана")
        print(f"   PAEI: {session.paei_scores}")
        print(f"   DISC: {session.disc_scores}")
        print(f"   HEXACO: {len(session.hexaco_scores)} параметров")
        print(f"   Soft Skills: {len(session.soft_skills_scores)} навыков")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании интеграции: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Главная функция тестирования"""
    
    print("🧪 Проверка соответствия скриптов обновленной логике промптов")
    print("=" * 70)
    
    tests = [
        ("AI Interpreter Logic", test_ai_interpreter_logic),
        ("Prompt Files", test_prompt_files), 
        ("Telegram Bot Integration", test_telegram_bot_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        if test_func():
            passed += 1
            print(f"✅ {test_name}: ПРОЙДЕН")
        else:
            print(f"❌ {test_name}: ПРОВАЛЕН")
    
    print(f"\n📊 Результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Логика скриптов соответствует обновленным промптам.")
    else:
        print("⚠️  Есть проблемы, требующие исправления.")
    
    return passed == total

if __name__ == "__main__":
    main()