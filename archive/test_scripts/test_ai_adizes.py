#!/usr/bin/env python3
"""
Тест генерации AI интерпретации Адизеса с маркдаун разметкой
"""

from pathlib import Path
import json
import os
import re

def test_real_ai_interpretation():
    """Тестируем реальную AI интерпретацию"""
    print("🔍 Тестирование генерации AI интерпретации Адизеса")
    print("=" * 60)
    
    # Имитируем настоящие данные PAEI
    paei_scores = {'P': 2, 'A': 2, 'E': 0, 'I': 1}  # Доминирующие P и A
    
    # Ищем доминирующую роль
    max_role = max(paei_scores, key=paei_scores.get)
    max_score = paei_scores[max_role]
    
    print(f"📊 PAEI результаты: {paei_scores}")
    print(f"🎯 Доминирующая роль: {max_role} ({max_score} баллов)")
    print()
    
    # Читаем промпт-файл
    adizes_file = Path("data/prompts/adizes_system_res.txt")
    if adizes_file.exists():
        with open(adizes_file, 'r', encoding='utf-8') as f:
            adizes_content = f.read()
        
        print("📋 Найден файл с промптами Адизеса")
        print(f"📏 Размер файла: {len(adizes_content)} символов")
        
        # Ищем примеры по ролям
        examples = []
        
        # Поиск всех примеров
        example_patterns = [
            r'Образец блока Классификация по Адизесу.*?(?=Образец блока|ИНСТРУКЦИЯ|$)',
        ]
        
        for pattern in example_patterns:
            matches = re.findall(pattern, adizes_content, re.DOTALL | re.IGNORECASE)
            examples.extend(matches)
        
        print(f"📚 Найдено примеров интерпретации: {len(examples)}")
        
        # Показываем примеры
        for i, example in enumerate(examples, 1):
            print(f"\n🔸 Пример {i}:")
            print(f"   Длина: {len(example)} символов")
            preview = example[:200].replace('\n', ' ')
            print(f"   Превью: {preview}...")
            
            # Проверяем маркдаун элементы
            markdown_elements = []
            if '**' in example:
                markdown_elements.append("Жирный текст (**text**)")
            if '###' in example:
                markdown_elements.append("Заголовки (### text)")
            if '---' in example:
                markdown_elements.append("Разделители (---)")
            if '- ' in example:
                markdown_elements.append("Списки (- item)")
            
            print(f"   Маркдаун: {', '.join(markdown_elements) if markdown_elements else 'Нет'}")
    
    else:
        print("❌ Файл с промптами не найден!")
        
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_real_ai_interpretation()