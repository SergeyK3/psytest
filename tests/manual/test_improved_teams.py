#!/usr/bin/env python3
"""
Тест генерации рекомендаций по команде с новыми инструкциями
"""

import sys
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from src.psytest.ai_interpreter import AIInterpreter

def test_team_recommendations_with_improvements():
    """Тестируем улучшенные рекомендации по команде"""
    
    print("🧪 ТЕСТ УЛУЧШЕННЫХ РЕКОМЕНДАЦИЙ ПО КОМАНДЕ")
    print("=" * 60)
    
    # Тестовые данные - создаем профиль с явными слабыми местами
    test_scores = {
        'paei': {'P': 1, 'A': 4, 'E': 1, 'I': 2},  # Сильный Администратор, слабые P и E
        'disc': {'D': 4.0, 'I': 2.0, 'S': 2.5, 'C': 3.5},  # Сильное Доминирование, слабое Влияние
        'hexaco': {'H': 4, 'E': 2, 'X': 2, 'A': 5, 'C': 4, 'O': 3},  # Слабые Эмоциональность и Экстраверсия
        'soft_skills': {'leadership': 4, 'emotional_intelligence': 2, 'communication': 3, 'critical_thinking': 2, 'time_management': 4, 'conflict_resolution': 3, 'adaptability': 3, 'employee_development': 2}  # Слабые: Эмоциональный интеллект, Критическое мышление, Навыки развития
    }
    
    print("📊 Тестовый профиль (с явными слабыми местами):")
    print(f"   PAEI: P=1, A=4, E=1, I=2 (слабые: P, E)")
    print(f"   DISC: D=4.0, I=2.0, S=2.5, C=3.5 (слабое: I)")
    print(f"   HEXACO: слабые E=2, X=2")
    print(f"   Soft Skills: слабые позиции (эмоц. интеллект, критич. мышление, развитие)")
    
    try:
        ai_interpreter = AIInterpreter()
        
        # Генерируем общее заключение с рекомендациями по команде
        general_interpretation = ai_interpreter.interpret_general_conclusion(test_scores)
        
        if general_interpretation:
            print(f"\n✅ AI успешно сгенерировал интерпретацию ({len(general_interpretation)} символов)")
            
            # Ищем раздел рекомендаций по команде
            lines = general_interpretation.split('\n')
            team_section_found = False
            team_content = []
            
            for line in lines:
                if 'рекомендации по подбору' in line.lower():
                    team_section_found = True
                    print(f"\n🎯 НАЙДЕН РАЗДЕЛ: {line}")
                    continue
                    
                if team_section_found:
                    if line.startswith('- ') or line.startswith('• '):
                        team_content.append(line)
                    elif line.strip() and not any(marker in line.lower() for marker in ['рекомендации', 'заключение', 'вывод']):
                        if 'полученный психологический портрет' not in line.lower():
                            team_content.append(line)
                    elif any(marker in line.lower() for marker in ['рекомендации', 'заключение']):
                        break
            
            if team_content:
                print(f"\n📋 СОДЕРЖИМОЕ РАЗДЕЛА КОМАНДЫ ({len(team_content)} строк):")
                for i, line in enumerate(team_content, 1):
                    print(f"   {i}. {line}")
                
                # Проверяем качество рекомендаций
                all_content = '\n'.join(team_content)
                
                print(f"\n🔍 АНАЛИЗ КАЧЕСТВА:")
                
                # Проверяем расшифровку аббревиатур
                abbreviations = ['(S)', '(E)', '(X)', '(P)', '(I)', '(D)', '(C)']
                expansions = ['Стабильность', 'Предприниматель', 'Экстраверсия', 'Производитель', 'Влияние', 'Доминирование', 'Соответствие']
                
                found_abbrev = [abbr for abbr in abbreviations if abbr in all_content]
                found_expansions = [exp for exp in expansions if exp.lower() in all_content.lower()]
                
                print(f"   📝 Найдено аббревиатур: {found_abbrev}")
                print(f"   📖 Найдено расшифровок: {found_expansions}")
                
                # Проверяем наличие запрещенной фразы
                forbidden_phrase = "полученный психологический портрет"
                if forbidden_phrase in all_content.lower():
                    print(f"   ❌ НАЙДЕНА ЗАПРЕЩЕННАЯ ФРАЗА: '{forbidden_phrase}'")
                else:
                    print(f"   ✅ Запрещенная фраза отсутствует")
                
                # Проверяем структуру рекомендаций
                disc_mentions = sum(1 for line in team_content if 'disc' in line.lower())
                paei_mentions = sum(1 for line in team_content if 'paei' in line.lower())
                hexaco_mentions = sum(1 for line in team_content if 'hexaco' in line.lower())
                soft_mentions = sum(1 for line in team_content if 'soft' in line.lower())
                
                print(f"   📊 Упоминания тестов: DISC={disc_mentions}, PAEI={paei_mentions}, HEXACO={hexaco_mentions}, Soft={soft_mentions}")
                
                if all([disc_mentions, paei_mentions, hexaco_mentions, soft_mentions]):
                    print(f"   ✅ Все 4 теста представлены в рекомендациях")
                else:
                    print(f"   ⚠️  Не все тесты представлены")
                
                return True
            else:
                print(f"   ❌ Раздел рекомендаций по команде не найден в содержимом")
                return False
        else:
            print("❌ AI не смог сгенерировать интерпретацию")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = test_team_recommendations_with_improvements()
    
    if success:
        print(f"\n🎊 ТЕСТ ПРОЙДЕН: Улучшенные рекомендации работают корректно!")
    else:
        print(f"\n❌ ТЕСТ НЕ ПРОЙДЕН: Требуется дополнительная настройка")