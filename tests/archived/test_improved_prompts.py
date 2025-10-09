#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование улучшенных промптов для DISC и ADIZES
Проверяем качество интерпретаций с различными комбинациями баллов
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from psytest.ai_interpreter import AIInterpreter

def test_disc_interpretations():
    """Тестируем различные профили DISC"""
    print("🧪 ТЕСТИРОВАНИЕ ИНТЕРПРЕТАЦИЙ DISC")
    print("=" * 50)
    
    ai_interpreter = AIInterpreter()
    
    # Тестовые сценарии DISC
    test_cases = [
        {
            "name": "Сбалансированный профиль",
            "data": {
                "1.1": 3, "1.2": 3,  # D=6
                "2.1": 4, "2.2": 3,  # I=7 
                "3.1": 2, "3.2": 3,  # S=5
                "4.1": 3, "4.2": 3   # C=6
            }
        },
        {
            "name": "Доминирующий D (как на диаграмме)",
            "data": {
                "1.1": 4, "1.2": 4,  # D=8
                "2.1": 1, "2.2": 1,  # I=2
                "3.1": 2, "3.2": 2,  # S=4
                "4.1": 1, "4.2": 1   # C=2
            }
        },
        {
            "name": "Доминирующий I (влияние)",
            "data": {
                "1.1": 2, "1.2": 1,  # D=3
                "2.1": 5, "2.2": 4,  # I=9
                "3.1": 2, "3.2": 2,  # S=4
                "4.1": 3, "4.2": 2   # C=5
            }
        },
        {
            "name": "Доминирующий S (устойчивость)",
            "data": {
                "1.1": 2, "1.2": 2,  # D=4
                "2.1": 2, "2.2": 2,  # I=4
                "3.1": 4, "3.2": 5,  # S=9
                "4.1": 3, "4.2": 3   # C=6
            }
        },
        {
            "name": "Доминирующий C (соответствие)",
            "data": {
                "1.1": 2, "1.2": 1,  # D=3
                "2.1": 2, "2.2": 2,  # I=4
                "3.1": 3, "3.2": 2,  # S=5
                "4.1": 5, "4.2": 4   # C=9
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Тест {i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            interpretation = ai_interpreter.interpret_disc(test_case['data'])
            print(f"✅ Интерпретация получена (длина: {len(interpretation)} символов)")
            
            # Проверяем, что интерпретация содержит ключевые элементы
            required_elements = [
                "Сумма баллов по доминированию",
                "Сумма баллов по влиянию", 
                "Сумма баллов по устойчивости",
                "Сумма баллов по подчинению правилам",
                "Общий вывод"
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in interpretation:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"⚠️  Отсутствуют элементы: {missing_elements}")
            else:
                print("✅ Все обязательные элементы присутствуют")
                
            # Показываем краткий отрывок
            preview = interpretation[:200] + "..." if len(interpretation) > 200 else interpretation
            print(f"📝 Превью: {preview}")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")

def test_adizes_interpretations():
    """Тестируем различные профили ADIZES"""
    print("\n\n🧪 ТЕСТИРОВАНИЕ ИНТЕРПРЕТАЦИЙ ADIZES")
    print("=" * 50)
    
    ai_interpreter = AIInterpreter()
    
    # Тестовые сценарии ADIZES
    test_cases = [
        {
            "name": "Доминирующий I (интегратор)",
            "choices": ["I", "I", "I", "P"]
        },
        {
            "name": "Сбалансированный профиль",
            "choices": ["P", "A", "E", "I"]
        },
        {
            "name": "Доминирующий A (как на диаграмме)",
            "choices": ["A", "A", "A", "P"]
        },
        {
            "name": "Доминирующий E (предприниматель)",
            "choices": ["E", "E", "E", "A"]
        },
        {
            "name": "Доминирующий P (производитель)",
            "choices": ["P", "P", "P", "I"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Тест {i}: {test_case['name']}")
        print("-" * 30)
        print(f"Выборы: {test_case['choices']}")
        
        try:
            interpretation = ai_interpreter.interpret_adizes(test_case['choices'])
            print(f"✅ Интерпретация получена (длина: {len(interpretation)} символов)")
            
            # Проверяем, что интерпретация содержит ключевые элементы
            required_elements = [
                "Классификация по Адизесу",
                "Общий портрет",
                "Рекомендации психолога",
                "Идеальные профессиональные роли"
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in interpretation:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"⚠️  Отсутствуют элементы: {missing_elements}")
            else:
                print("✅ Все обязательные элементы присутствуют")
                
            # Показываем краткий отрывок
            preview = interpretation[:200] + "..." if len(interpretation) > 200 else interpretation
            print(f"📝 Превью: {preview}")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🚀 ЗАПУСК ТЕСТИРОВАНИЯ УЛУЧШЕННЫХ ПРОМПТОВ")
    print("=" * 60)
    
    try:
        test_disc_interpretations()
        test_adizes_interpretations()
        
        print("\n\n🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
        print("Проверьте качество интерпретаций выше.")
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()