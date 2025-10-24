#!/usr/bin/env python3
"""
Тест форматирования интерпретации Адизеса
"""

from interpretation_utils import generate_interpretations_from_prompt

def test_adizes_formatting():
    """Тестируем форматирование интерпретации Адизеса"""
    print("🔍 Тестирование форматирования интерпретации Адизеса")
    print("=" * 60)
    
    # Тестовые данные PAEI
    test_results = {
        'paei': {
            'P': 8,  # Производитель 
            'A': 5,  # Администратор
            'E': 7,  # Предприниматель
            'I': 6   # Интегратор
        },
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
    
    print("📋 Текущая интерпретация PAEI (Адизес):")
    print("-" * 40)
    if 'paei' in interpretations:
        paei_text = interpretations['paei']
        print(paei_text)
        print()
        print(f"📊 Длина текста: {len(paei_text)} символов")
        print(f"📄 Количество строк: {len(paei_text.split('\n'))}")
        
        # Проверяем наличие маркдаун разметки
        markdown_elements = []
        if '**' in paei_text:
            markdown_elements.append("Жирный текст (**text**)")
        if '###' in paei_text:
            markdown_elements.append("Заголовки (### text)")
        if '---' in paei_text:
            markdown_elements.append("Разделители (---)")
        if '*' in paei_text and '**' not in paei_text:
            markdown_elements.append("Курсив (*text*)")
        if '- ' in paei_text:
            markdown_elements.append("Списки (- item)")
            
        print(f"📝 Найденные элементы маркдаун: {', '.join(markdown_elements) if markdown_elements else 'Нет'}")
        
    else:
        print("❌ Интерпретация PAEI не найдена!")

if __name__ == "__main__":
    test_adizes_formatting()