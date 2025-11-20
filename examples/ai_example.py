"""
Пример использования AI интерпретаций в psytest
"""
import os
import sys
from pathlib import Path

# Добавляем путь к src для импорта
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from psytest.ai_interpreter import get_ai_interpreter
from psytest.enhanced_report import render_enhanced_report

def example_ai_usage():
    """Пример использования AI интерпретатора"""
    
    # Загружаем переменные окружения из .env файла
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    
    # Проверяем наличие API ключа
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY не установлен")
        print("Установите переменную окружения или создайте файл .env")
        return
    
    # Создаём интерпретатор
    ai = get_ai_interpreter()
    if ai is None:
        print("❌ Не удалось создать AI интерпретатор")
        return
    
    print("✅ AI интерпретатор готов к работе")
    print(f"🤖 Используется модель: {ai.model}")
    
    # Пример интерпретации PAEI
    scores = {"P": 15, "A": 8, "E": 12, "I": 18}
    interpretation = ai.interpret_paei(scores)
    
    print("\n📊 Пример интерпретации PAEI:")
    print(f"Баллы: {scores}")
    print("Интерпретация:")
    print(interpretation)

if __name__ == "__main__":
    example_ai_usage()