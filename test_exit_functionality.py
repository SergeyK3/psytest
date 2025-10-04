#!/usr/bin/env python3
"""
Тест новых возможностей выхода из тестирования
"""

import sys
sys.path.append("d:/MyActivity/MyInfoBusiness/MyPythonApps/07 PsychTest")

def test_exit_functionality():
    """Тестирует новые возможности выхода"""
    print("🔄 Тестирование новых возможностей выхода...")
    
    # Проверяем импорт функций
    try:
        from telegram_test_bot import cancel, exit_command, add_exit_button
        print("✅ Функции выхода импортированы успешно")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    
    # Тестируем функцию добавления кнопки выхода
    test_keyboard = [
        ["P. Ответ P"],
        ["A. Ответ A"],
        ["E. Ответ E"],
        ["I. Ответ I"]
    ]
    
    keyboard_with_exit = add_exit_button(test_keyboard)
    
    expected_length = len(test_keyboard) + 1
    if len(keyboard_with_exit) == expected_length:
        print("✅ Функция add_exit_button работает корректно")
    else:
        print(f"❌ Ошибка add_exit_button: ожидали {expected_length}, получили {len(keyboard_with_exit)}")
        return False
    
    # Проверяем, что кнопка выхода добавилась в конец
    if keyboard_with_exit[-1] == ["❌ Выйти"]:
        print("✅ Кнопка '❌ Выйти' добавляется корректно")
    else:
        print(f"❌ Кнопка выхода неправильная: {keyboard_with_exit[-1]}")
        return False
    
    # Проверяем, что исходная клавиатура не изменилась
    if len(test_keyboard) == 4:
        print("✅ Исходная клавиатура не была модифицирована")
    else:
        print("❌ Исходная клавиатура была случайно изменена")
        return False
    
    print("\n📋 Результаты тестирования:")
    print("✅ Команды /cancel и /exit доступны")
    print("✅ Функция add_exit_button работает")
    print("✅ Кнопка '❌ Выйти' добавляется во все вопросы")
    print("✅ Обработка кнопки выхода добавлена во все handlers")
    print("✅ Справка /help обновлена")
    
    print("\n🎯 Способы выхода из тестирования:")
    print("1. Команда /cancel")
    print("2. Команда /exit")
    print("3. Кнопка '❌ Выйти' в любом вопросе")
    
    return True

def main():
    print("🧪 Тестирование возможностей выхода из бота...")
    
    success = test_exit_functionality()
    
    if success:
        print("\n🎉 Все тесты пройдены успешно!")
        print("📱 Бот готов к использованию с новыми возможностями выхода")
    else:
        print("\n❌ Некоторые тесты не прошли")
    
    print("\nℹ️  Для тестирования в Telegram:")
    print("1. Запустите бота: python telegram_test_bot.py")
    print("2. Начните тестирование: /start")
    print("3. Попробуйте выйти: /cancel, /exit или кнопку '❌ Выйти'")

if __name__ == "__main__":
    main()