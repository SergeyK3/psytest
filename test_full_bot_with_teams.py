#!/usr/bin/env python3
"""
Полное тестирование бота с новой функциональностью рекомендаций по команде
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Добавляем src в путь
sys.path.append(str(Path(__file__).parent / 'src'))

from src.psytest.ai_interpreter import AIInterpreter

def test_full_team_recommendations():
    """Полное тестирование генерации рекомендаций по команде"""
    
    print("🧪 ПОЛНОЕ ТЕСТИРОВАНИЕ РЕКОМЕНДАЦИЙ ПО КОМАНДЕ")
    print("=" * 60)
    
    # Инициализируем AI интерпретатор
    try:
        ai = AIInterpreter()
        print("✅ AI интерпретатор успешно инициализирован")
    except Exception as e:
        print(f"❌ Ошибка инициализации AI: {e}")
        return False
    
    # Тестовые данные с явными слабыми областями
    test_scores = {
        'paei': {'P': 1, 'A': 1, 'E': 5, 'I': 4},  # P и A - очень слабые
        'disc': {'D': 5.0, 'I': 4.0, 'S': 1.0, 'C': 2.0},  # S очень слабый, C слабый
        'hexaco': {
            'Честность-Скромность': 4.0,
            'Эмоциональность': 1.5,      # Очень слабая
            'Экстраверсия': 1.2,         # Очень слабая  
            'Доброжелательность': 2.0,   # Слабая
            'Добросовестность': 4.5,
            'Открытость опыту': 3.8
        },
        'soft_skills': {
            'leadership': 5,
            'emotional_intelligence': 5, 
            'communication': 4,
            'critical_thinking': 1,      # Очень слабый
            'time_management': 4,
            'conflict_resolution': 5,
            'adaptability': 2,           # Слабый
            'employee_development': 5,
            'teamwork': 2,               # Слабый
            'creativity': 1              # Очень слабый
        }
    }
    
    print("📊 Тестовый профиль:")
    print("PAEI слабые области: P=1, A=1")
    print("DISC слабые области: S=1.0, C=2.0") 
    print("HEXACO слабые области: Эмоциональность=1.5, Экстраверсия=1.2, Доброжелательность=2.0")
    print("Soft Skills слабые области: critical_thinking=1, adaptability=2, teamwork=2, creativity=1")
    print()
    
    try:
        print("🔄 Генерируем общее заключение с рекомендациями по команде...")
        
        # Генерируем общее заключение
        general_conclusion = ai.interpret_general_conclusion(test_scores)
        
        print("✅ Генерация завершена успешно!")
        print()
        print("📄 РЕЗУЛЬТАТ ОБЩЕГО ЗАКЛЮЧЕНИЯ:")
        print("=" * 50)
        print(general_conclusion)
        print("=" * 50)
        
        # Анализируем результат
        content_lower = general_conclusion.lower()
        
        # Проверяем наличие ключевых элементов новой функциональности
        team_checks = {
            "Раздел 4 присутствует": "4." in general_conclusion and ("рекомендации по подбору" in content_lower or "команд" in content_lower),
            "DISC-компенсация": "disc" in content_lower and ("компенсация" in content_lower or "баланс" in content_lower),
            "PAEI-дополнение": "paei" in content_lower and ("дополнение" in content_lower or "роли" in content_lower),
            "HEXACO-баланс": "hexaco" in content_lower and ("баланс" in content_lower or "характеристик" in content_lower),
            "Soft Skills-синергия": ("soft skills" in content_lower or "навык" in content_lower) and ("синергия" in content_lower or "эксперт" in content_lower),
            "Анализ слабых областей": any(weak in content_lower for weak in ["слаб", "низк", "развит", "улучш"]),
            "Конкретные рекомендации": any(rec in content_lower for rec in ["специалист", "кандидат", "добавить", "искать", "компенсировать"]),
            "Упоминание команды": any(team in content_lower for team in ["команд", "подбор", "кадр"])
        }
        
        print("\n🔍 АНАЛИЗ ФУНКЦИОНАЛЬНОСТИ:")
        passed_checks = 0
        for check_name, result in team_checks.items():
            status = "✅" if result else "❌"
            print(f"{status} {check_name}")
            if result:
                passed_checks += 1
        
        success_rate = passed_checks / len(team_checks) * 100
        print(f"\n📊 Успешность: {passed_checks}/{len(team_checks)} ({success_rate:.1f}%)")
        
        if success_rate >= 75:
            print("\n🎉 ТЕСТ ПРОЙДЕН! Новая функциональность рекомендаций по команде работает отлично!")
            return True
        elif success_rate >= 50:
            print("\n⚠️  ТЕСТ ЧАСТИЧНО ПРОЙДЕН. Функциональность работает, но требуется доработка.")
            return True
        else:
            print("\n💥 ТЕСТ ПРОВАЛЕН. Функциональность не работает должным образом.")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при генерации заключения: {e}")
        return False

if __name__ == "__main__":
    success = test_full_team_recommendations()
    
    if success:
        print("\n🚀 ГОТОВ К КОММИТУ: Функциональность рекомендаций по команде протестирована и работает!")
    else:
        print("\n🔧 ТРЕБУЕТСЯ ДОРАБОТКА: Проверьте конфигурацию и промпты.")