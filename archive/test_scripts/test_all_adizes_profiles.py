#!/usr/bin/env python3
"""
Полный тест форматирования интерпретации Адизеса для разных профилей
"""

from interpretation_utils import generate_interpretations_from_prompt

def test_different_profiles():
    """Тестируем разные типы профилей PAEI"""
    print("🔍 Тестирование разных профилей Адизеса")
    print("=" * 70)
    
    test_cases = [
        {
            'name': 'Доминирующий Производитель (P)',
            'paei': {'P': 4, 'A': 1, 'E': 1, 'I': 0}
        },
        {
            'name': 'Доминирующий Администратор (A)',
            'paei': {'P': 1, 'A': 4, 'E': 0, 'I': 1}
        },
        {
            'name': 'Доминирующий Предприниматель (E)',
            'paei': {'P': 0, 'A': 1, 'E': 4, 'I': 1}
        },
        {
            'name': 'Доминирующий Интегратор (I)',
            'paei': {'P': 1, 'A': 0, 'E': 1, 'I': 4}
        },
        {
            'name': 'Сбалансированный профиль',
            'paei': {'P': 2, 'A': 2, 'E': 2, 'I': 2}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Тест {i}: {test_case['name']}")
        print("-" * 50)
        
        # Создаем полные тестовые данные
        test_results = {
            'paei': test_case['paei'],
            'disc': {'D': 15, 'I': 12, 'S': 10, 'C': 8},
            'soft': {'leadership': 4, 'communication': 5, 'teamwork': 3},
            'hexaco': {'H': 3.5, 'E': 4.0, 'X': 3.8, 'A': 4.2, 'C': 3.9, 'O': 4.1}
        }
        
        # Генерируем интерпретации
        interpretations = generate_interpretations_from_prompt(
            paei_scores=test_results['paei'],
            disc_scores=test_results['disc'],
            hexaco_scores=test_results['hexaco'],
            soft_skills_scores=test_results['soft']
        )
        
        if 'paei' in interpretations:
            paei_text = interpretations['paei']
            
            # Показываем первые несколько строк
            lines = paei_text.split('\n')
            preview_lines = lines[:8]  # Первые 8 строк
            
            print("📄 Превью интерпретации:")
            for line in preview_lines:
                print(f"   {line}")
            
            if len(lines) > 8:
                print(f"   ... (еще {len(lines) - 8} строк)")
            
            print(f"\n📊 Статистика:")
            print(f"   • Длина: {len(paei_text)} символов")
            print(f"   • Строк: {len(lines)}")
            
            # Проверяем маркдаун элементы
            markdown_elements = []
            if '**' in paei_text:
                markdown_elements.append("Жирный текст")
            if '###' in paei_text:
                markdown_elements.append("Заголовки")
            if '---' in paei_text:
                markdown_elements.append("Разделители")
            if '- ' in paei_text:
                markdown_elements.append("Списки")
                
            print(f"   • Маркдаун: {', '.join(markdown_elements) if markdown_elements else 'Нет'}")
            
            # Проверяем правильность адаптации роли
            role_names = {'P': 'Производитель', 'A': 'Администратор', 'E': 'Предприниматель', 'I': 'Интегратор'}
            max_role = max(test_case['paei'], key=test_case['paei'].get)
            expected_role = role_names[max_role]
            
            if expected_role in paei_text or max_role in paei_text:
                print(f"   ✅ Роль {expected_role} ({max_role}) найдена в тексте")
            else:
                print(f"   ⚠️ Роль {expected_role} ({max_role}) не найдена в тексте")
                
        else:
            print("❌ Интерпретация PAEI не найдена!")
    
    print("\n" + "=" * 70)
    print("🎯 Тестирование завершено!")

if __name__ == "__main__":
    test_different_profiles()