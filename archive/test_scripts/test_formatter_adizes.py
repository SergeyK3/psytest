#!/usr/bin/env python3
"""
Тест форматирования интерпретации Адизеса через interpretation_formatter
"""

from interpretation_formatter import format_ai_interpretations
from interpretation_utils import generate_interpretations_from_prompt

def test_adizes_through_formatter():
    """Тестируем прохождение Адизеса через форматтер"""
    print("🔍 Тестирование форматирования Адизеса через formatter")
    print("=" * 60)
    
    # Тестовые данные 
    test_results = {
        'paei': {'P': 1, 'A': 2, 'E': 4, 'I': 1},  # Доминирует Предприниматель
        'disc': {'D': 4.0, 'I': 3.0, 'S': 2.5, 'C': 3.0},
        'hexaco': {'H': 3.8, 'E': 4.2, 'X': 3.5, 'A': 4.0, 'C': 3.9, 'O': 4.3},
        'soft': {'leadership': 4, 'communication': 5, 'teamwork': 3}
    }
    
    # Генерируем интерпретации
    print("📝 Генерируем исходные интерпретации...")
    raw_interpretations = generate_interpretations_from_prompt(
        paei_scores=test_results['paei'],
        disc_scores=test_results['disc'],
        hexaco_scores=test_results['hexaco'],
        soft_skills_scores=test_results['soft']
    )
    
    if 'paei' in raw_interpretations:
        print("✅ PAEI интерпретация сгенерирована")
        raw_adizes = raw_interpretations['paei']
        
        print(f"📊 Исходная интерпретация:")
        print(f"   • Длина: {len(raw_adizes)} символов")
        print(f"   • Строк: {len(raw_adizes.split('\n'))}")
        
        # Считаем маркдаун элементы
        markdown_before = {
            'bold': raw_adizes.count('**'),
            'headers': raw_adizes.count('###'),
            'separators': raw_adizes.count('---'),
            'lists': raw_adizes.count('- ')
        }
        print(f"   • Маркдаун элементы ДО: {markdown_before}")
        
        # Форматируем через formatter
        print("\n🔄 Форматируем через interpretation_formatter...")
        formatted_interpretations = format_ai_interpretations(raw_interpretations)
        
        if 'paei' in formatted_interpretations:
            formatted_adizes = formatted_interpretations['paei']
            
            print(f"📊 Отформатированная интерпретация:")
            print(f"   • Длина: {len(formatted_adizes)} символов")
            print(f"   • Строк: {len(formatted_adizes.split('\n'))}")
            
            # Считаем маркдаун элементы после
            markdown_after = {
                'bold': formatted_adizes.count('**'),
                'headers': formatted_adizes.count('###'),
                'separators': formatted_adizes.count('---'),
                'lists': formatted_adizes.count('- ')
            }
            print(f"   • Маркдаун элементы ПОСЛЕ: {markdown_after}")
            
            # Проверяем изменения
            changed = any(markdown_before[k] != markdown_after[k] for k in markdown_before)
            if changed:
                print("⚠️ Форматтер изменил маркдаун разметку!")
                for key in markdown_before:
                    if markdown_before[key] != markdown_after[key]:
                        print(f"   • {key}: {markdown_before[key]} → {markdown_after[key]}")
            else:
                print("✅ Маркдаун разметка сохранена")
                
            # Показываем превью
            lines = formatted_adizes.split('\n')[:10]
            print(f"\n📄 Превью отформатированной интерпретации:")
            for line in lines:
                print(f"   {line}")
            if len(formatted_adizes.split('\n')) > 10:
                print("   ...")
        else:
            print("❌ PAEI интерпретация потеряна после форматирования!")
    else:
        print("❌ PAEI интерпретация не сгенерирована!")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_adizes_through_formatter()