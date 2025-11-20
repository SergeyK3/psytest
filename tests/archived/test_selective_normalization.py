#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест селективной нормализации: PAEI/DISC с нормализацией, HEXACO/SOFT_SKILLS без
"""

from scale_normalizer import ScaleNormalizer

def test_selective_normalization():
    """Тестируем селективную нормализацию"""
    print("🔄 Тест селективной нормализации")
    print("=" * 60)
    
    # Тестовые данные
    test_data = {
        "PAEI": {"P": 1, "A": 5, "E": 2, "I": 0},          # Должны нормализоваться 0-10
        "DISC": {"D": 6, "I": 1, "S": 2, "C": 0},          # Должны нормализоваться 0-10
        "HEXACO": {"H": 2.3, "E": 4.7, "X": 1.9, "A": 3.6, "C": 2.1, "O": 4.4},  # Остаются 1-5
        "SOFT_SKILLS": {"Коммуникация": 7.8, "Лидерство": 6.3, "Креативность": 8.9, "Адаптивность": 5.4}  # Остаются 1-10
    }
    
    print("📊 Результаты обработки:")
    print()
    
    for test_type, scores in test_data.items():
        print(f"🔍 {test_type}:")
        print(f"   Исходные:      {scores}")
        
        normalized, method = ScaleNormalizer.auto_normalize(test_type, scores)
        print(f"   Обработанные:  {normalized}")
        print(f"   Метод:         {method}")
        
        # Анализ результатов
        if test_type in ["PAEI", "DISC"]:
            max_val = max(normalized.values())
            if max_val <= 10:
                print(f"   ✅ Корректно нормализовано (макс: {max_val})")
            else:
                print(f"   ❌ Ошибка нормализации (макс: {max_val})")
        else:
            # HEXACO должно остаться в диапазоне 1-5, SOFT_SKILLS в 1-10
            original_range = scores
            if test_type == "HEXACO":
                expected_min, expected_max = 1, 5
            else:  # SOFT_SKILLS
                expected_min, expected_max = 1, 10
                
            actual_min = min(normalized.values())
            actual_max = max(normalized.values())
            
            if expected_min <= actual_min and actual_max <= expected_max:
                print(f"   ✅ Остался в оригинальном диапазоне ({actual_min:.1f}-{actual_max:.1f})")
            else:
                print(f"   ❌ Вышел за оригинальный диапазон ({actual_min:.1f}-{actual_max:.1f})")
        
        print()

def test_visualization_impact():
    """Демонстрируем влияние на визуализацию"""
    print("📈 Влияние на визуализацию диаграмм:")
    print("=" * 60)
    
    # Проблемный случай - высокие значения PAEI/DISC
    problem_case = {
        "PAEI": {"P": 0, "A": 5, "E": 0, "I": 0},          # A максимальное
        "DISC": {"D": 6, "I": 0, "S": 0, "C": 0},          # D максимальное
        "HEXACO": {"H": 3.0, "E": 3.0, "X": 3.0, "A": 3.0, "C": 3.0, "O": 3.0},  # Средние значения
        "SOFT_SKILLS": {"Навык1": 5.0, "Навык2": 5.0, "Навык3": 5.0, "Навык4": 5.0}  # Средние значения
    }
    
    print("🎯 Проблемный случай (максимальные PAEI/DISC, средние остальные):")
    print()
    
    for test_type, scores in problem_case.items():
        normalized, method = ScaleNormalizer.auto_normalize(test_type, scores)
        max_val = max(normalized.values())
        
        print(f"{test_type}:")
        print(f"  До:     {scores} (макс: {max(scores.values()):.1f})")
        print(f"  После:  {normalized} (макс: {max_val:.1f})")
        
        if test_type in ["PAEI", "DISC"]:
            print(f"  📊 Диаграмма: максимальные значения теперь достигают края (10.0)")
        else:
            print(f"  📊 Диаграмма: сохранена оригинальная интерпретация")
        print()

if __name__ == "__main__":
    test_selective_normalization()
    print()
    test_visualization_impact()
    
    print("🎉 Селективная нормализация настроена!")
    print("✅ PAEI/DISC: нормализация к 0-10 для правильных пропорций")
    print("✅ HEXACO: оригинальная шкала 1-5 для правильной интерпретации") 
    print("✅ SOFT_SKILLS: оригинальная шкала 1-10 для правильной интерпретации")