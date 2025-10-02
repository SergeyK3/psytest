#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полное тестирование улучшенных промптов с различными профилями
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Загружаем переменные окружения из .env файла
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

from psytest.ai_interpreter import AIInterpreter

def test_comprehensive_disc():
    """Тестируем все типы DISC профилей"""
    print("🧪 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ DISC")
    print("=" * 50)
    
    ai_interpreter = AIInterpreter()
    
    test_cases = [
        {
            "name": "🎯 Доминирующий D (решительный лидер)",
            "data": {"1.1": 5, "1.2": 4, "2.1": 1, "2.2": 2, "3.1": 2, "3.2": 1, "4.1": 2, "4.2": 2},
            "expected_dominant": "D"
        },
        {
            "name": "🗣️ Доминирующий I (коммуникатор)",
            "data": {"1.1": 2, "1.2": 1, "2.1": 5, "2.2": 4, "3.1": 2, "3.2": 2, "4.1": 3, "4.2": 2},
            "expected_dominant": "I"
        },
        {
            "name": "🤝 Доминирующий S (стабильный)",
            "data": {"1.1": 2, "1.2": 2, "2.1": 2, "2.2": 2, "3.1": 5, "3.2": 4, "4.1": 3, "4.2": 3},
            "expected_dominant": "S"
        },
        {
            "name": "📋 Доминирующий C (аналитик)",
            "data": {"1.1": 1, "1.2": 2, "2.1": 2, "2.2": 2, "3.1": 3, "3.2": 2, "4.1": 5, "4.2": 4},
            "expected_dominant": "C"
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Тест {i}: {test_case['name']}")
        print("-" * 40)
        
        # Вычисляем баллы
        d_score = test_case['data']['1.1'] + test_case['data']['1.2']
        i_score = test_case['data']['2.1'] + test_case['data']['2.2']
        s_score = test_case['data']['3.1'] + test_case['data']['3.2']
        c_score = test_case['data']['4.1'] + test_case['data']['4.2']
        
        print(f"D: {d_score}, I: {i_score}, S: {s_score}, C: {c_score}")
        
        try:
            interpretation = ai_interpreter.interpret_disc(test_case['data'])
            
            # Проверяем качество интерпретации
            quality_checks = {
                "Содержит точные суммы": f"Сумма баллов по доминированию {d_score}" in interpretation,
                "Анализирует все аспекты": all(aspect in interpretation for aspect in ["доминированию", "влиянию", "устойчивости", "подчинению правилам"]),
                "Есть общий вывод": "Общий вывод" in interpretation,
                "Есть рекомендации": "Рекомендации" in interpretation or "рекомендации" in interpretation.lower(),
                "Достаточная длина": len(interpretation) > 500
            }
            
            passed_checks = sum(quality_checks.values())
            total_checks = len(quality_checks)
            
            print(f"✅ Интерпретация получена ({len(interpretation)} символов)")
            print(f"📊 Качество: {passed_checks}/{total_checks} проверок пройдено")
            
            for check, passed in quality_checks.items():
                print(f"  {'✅' if passed else '❌'} {check}")
            
            results.append({
                "name": test_case['name'],
                "length": len(interpretation),
                "quality": f"{passed_checks}/{total_checks}",
                "success": passed_checks >= 4
            })
            
            # Показываем краткий отрывок
            preview = interpretation[:200] + "..." if len(interpretation) > 200 else interpretation
            print(f"📝 Превью: {preview}")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            results.append({"name": test_case['name'], "success": False, "error": str(e)})
    
    return results

def test_comprehensive_adizes():
    """Тестируем все типы ADIZES профилей"""
    print("\n\n🧪 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ ADIZES")
    print("=" * 50)
    
    ai_interpreter = AIInterpreter()
    
    test_cases = [
        {
            "name": "🚀 Доминирующий P (производитель)",
            "choices": ["P", "P", "P", "A"]
        },
        {
            "name": "📊 Доминирующий A (администратор)",
            "choices": ["A", "A", "A", "P"]
        },
        {
            "name": "💡 Доминирующий E (предприниматель)",
            "choices": ["E", "E", "E", "I"]
        },
        {
            "name": "🤝 Доминирующий I (интегратор)",
            "choices": ["I", "I", "I", "P"]
        },
        {
            "name": "⚖️ Сбалансированный профиль",
            "choices": ["P", "A", "E", "I"]
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Тест {i}: {test_case['name']}")
        print("-" * 40)
        print(f"Выборы: {test_case['choices']}")
        
        try:
            interpretation = ai_interpreter.interpret_adizes(test_case['choices'])
            
            # Проверяем качество интерпретации
            quality_checks = {
                "Есть заголовок": "Классификация по Адизесу" in interpretation,
                "Анализирует выборы": any(choice in interpretation for choice in ["P", "A", "E", "I"]),
                "Есть общий портрет": "Общий портрет" in interpretation,
                "Есть рекомендации": "Рекомендации психолога" in interpretation,
                "Есть профроли": "Идеальные профессиональные роли" in interpretation,
                "Достаточная длина": len(interpretation) > 800
            }
            
            passed_checks = sum(quality_checks.values())
            total_checks = len(quality_checks)
            
            print(f"✅ Интерпретация получена ({len(interpretation)} символов)")
            print(f"📊 Качество: {passed_checks}/{total_checks} проверок пройдено")
            
            for check, passed in quality_checks.items():
                print(f"  {'✅' if passed else '❌'} {check}")
            
            results.append({
                "name": test_case['name'],
                "length": len(interpretation),
                "quality": f"{passed_checks}/{total_checks}",
                "success": passed_checks >= 5
            })
            
            # Показываем краткий отрывок
            preview = interpretation[:200] + "..." if len(interpretation) > 200 else interpretation
            print(f"📝 Превью: {preview}")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            results.append({"name": test_case['name'], "success": False, "error": str(e)})
    
    return results

def generate_summary(disc_results, adizes_results):
    """Генерируем итоговый отчет"""
    print("\n\n🎉 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
    print("=" * 60)
    
    print(f"\n📊 РЕЗУЛЬТАТЫ DISC ({len(disc_results)} тестов):")
    disc_success = 0
    for result in disc_results:
        status = "✅" if result.get('success', False) else "❌"
        length = result.get('length', 'N/A')
        quality = result.get('quality', 'N/A')
        print(f"  {status} {result['name']} - {length} символов, качество: {quality}")
        if result.get('success', False):
            disc_success += 1
    
    print(f"\n📊 РЕЗУЛЬТАТЫ ADIZES ({len(adizes_results)} тестов):")
    adizes_success = 0
    for result in adizes_results:
        status = "✅" if result.get('success', False) else "❌"
        length = result.get('length', 'N/A')
        quality = result.get('quality', 'N/A')
        print(f"  {status} {result['name']} - {length} символов, качество: {quality}")
        if result.get('success', False):
            adizes_success += 1
    
    print(f"\n🎯 ОБЩАЯ СТАТИСТИКА:")
    print(f"  DISC: {disc_success}/{len(disc_results)} успешно ({disc_success/len(disc_results)*100:.1f}%)")
    print(f"  ADIZES: {adizes_success}/{len(adizes_results)} успешно ({adizes_success/len(adizes_results)*100:.1f}%)")
    
    total_success = disc_success + adizes_success
    total_tests = len(disc_results) + len(adizes_results)
    print(f"  ОБЩИЙ РЕЗУЛЬТАТ: {total_success}/{total_tests} успешно ({total_success/total_tests*100:.1f}%)")
    
    if total_success/total_tests >= 0.8:
        print("\n🎊 ОТЛИЧНЫЙ РЕЗУЛЬТАТ! Улучшенные промпты работают превосходно!")
    elif total_success/total_tests >= 0.6:
        print("\n✅ ХОРОШИЙ РЕЗУЛЬТАТ! Улучшения работают, но есть место для доработки.")
    else:
        print("\n⚠️ ТРЕБУЕТСЯ ДОРАБОТКА. Некоторые промпты нуждаются в улучшении.")

if __name__ == "__main__":
    print("🚀 ПОЛНОЕ ТЕСТИРОВАНИЕ УЛУЧШЕННЫХ ПРОМПТОВ")
    print("=" * 70)
    
    try:
        # Проверяем API ключ
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ OpenAI API ключ не найден")
            exit(1)
        
        # Запускаем тесты
        disc_results = test_comprehensive_disc()
        adizes_results = test_comprehensive_adizes()
        
        # Генерируем отчет
        generate_summary(disc_results, adizes_results)
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()