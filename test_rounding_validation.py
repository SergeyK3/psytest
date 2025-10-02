#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест проверки округления до 1 десятичного знака
"""

from scale_normalizer import ScaleNormalizer

def test_rounding_precision():
    """Тестируем точность округления"""
    print("🔍 Тест округления до 1 десятичного знака")
    print("=" * 50)
    
    # Тестовые данные с различными значениями
    test_cases = [
        # PAEI тесты
        ("PAEI", {"P": 1, "A": 2, "E": 1, "I": 1}),  # Все по 1-2
        ("PAEI", {"P": 0, "A": 5, "E": 0, "I": 0}),  # Экстремум A
        ("PAEI", {"P": 1, "A": 1, "E": 1, "I": 2}),  # Смешанные
        
        # DISC тесты
        ("DISC", {"D": 1, "I": 2, "S": 2, "C": 1}),  # Сбалансированные
        ("DISC", {"D": 6, "I": 0, "S": 0, "C": 0}),  # Экстремум D
        ("DISC", {"D": 2, "I": 1, "S": 2, "C": 1}),  # Смешанные
        
        # HEXACO тесты (шкала 1-5)
        ("HEXACO", {"H": 2.3, "E": 4.7, "X": 1.9, "A": 3.6, "C": 2.1, "O": 4.4}),
        ("HEXACO", {"H": 1.0, "E": 5.0, "X": 2.5, "A": 3.3, "C": 4.8, "O": 1.7}),
        
        # Soft Skills тесты (шкала 1-10)
        ("SOFT_SKILLS", {"Коммуникация": 7.8, "Лидерство": 6.3, "Тимворк": 8.9, "Адаптивность": 5.4}),
        ("SOFT_SKILLS", {"Коммуникация": 10.0, "Лидерство": 1.0, "Тимворк": 5.5, "Адаптивность": 7.2}),
    ]
    
    for test_type, scores in test_cases:
        print(f"\n📊 {test_type} тест:")
        print(f"   Исходные: {scores}")
        
        normalized, method = ScaleNormalizer.auto_normalize(test_type, scores)
        print(f"   Нормализованные: {normalized}")
        print(f"   Метод: {method}")
        
        # Проверяем округление
        for key, value in normalized.items():
            decimal_places = len(str(value).split('.')[-1]) if '.' in str(value) else 0
            if decimal_places > 1:
                print(f"   ❌ ОШИБКА: {key}={value} имеет {decimal_places} знаков после запятой!")
            else:
                print(f"   ✅ OK: {key}={value} корректно округлено")

def test_extreme_rounding_cases():
    """Тестируем экстремальные случаи округления"""
    print("\n🎯 Экстремальные случаи округления")
    print("=" * 50)
    
    # Случаи, которые могут давать много знаков после запятой
    extreme_cases = [
        # PAEI: 1/5 = 0.2, 2/5 = 0.4, 3/5 = 0.6, 4/5 = 0.8
        ("PAEI", {"P": 1, "A": 2, "E": 3, "I": 4}),  # Должно быть 2.0, 4.0, 6.0, 8.0
        
        # DISC: 1/6 = 0.166..., 2/6 = 0.333..., 5/6 = 0.833...
        ("DISC", {"D": 1, "I": 2, "S": 0, "C": 5}),  # Должно быть 1.7, 3.3, 0.0, 8.3
        
        # HEXACO: дробные значения
        ("HEXACO", {"H": 1.33, "E": 2.67, "X": 3.14, "A": 4.99, "C": 1.01, "O": 4.44}),
        
        # Soft Skills: значения с несколькими знаками
        ("SOFT_SKILLS", {"Skill1": 3.333, "Skill2": 6.666, "Skill3": 9.999, "Skill4": 1.111}),
    ]
    
    for test_type, scores in extreme_cases:
        print(f"\n🔬 {test_type} экстремальный тест:")
        print(f"   Исходные: {scores}")
        
        normalized, method = ScaleNormalizer.auto_normalize(test_type, scores)
        print(f"   Нормализованные: {normalized}")
        
        # Детальная проверка округления
        all_correct = True
        for key, value in normalized.items():
            str_value = str(value)
            if '.' in str_value:
                decimal_part = str_value.split('.')[1]
                if len(decimal_part) > 1:
                    print(f"   ❌ {key}={value} -> {len(decimal_part)} знаков после запятой")
                    all_correct = False
                else:
                    print(f"   ✅ {key}={value} -> {len(decimal_part)} знак после запятой")
            else:
                print(f"   ✅ {key}={value} -> целое число")
        
        if all_correct:
            print(f"   🎉 Все значения корректно округлены!")

if __name__ == "__main__":
    test_rounding_precision()
    test_extreme_rounding_cases()
    print("\n✅ Тестирование округления завершено!")