#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание тестового отчета с нормализованными значениями для демонстрации округления
"""

import sys
sys.path.append('.')

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from scale_normalizer import ScaleNormalizer
from datetime import datetime
from pathlib import Path

def create_demo_normalized_report():
    """Создаем демонстрационный отчет с нормализованными значениями"""
    print("📊 Создание демонстрационного отчета с нормализацией...")
    
    # Тестовые данные ДО нормализации
    original_data = {
        "paei": {"P": 1, "A": 5, "E": 2, "I": 0},  # Максимум A=5
        "disc": {"D": 6, "I": 1, "S": 2, "C": 0},  # Максимум D=6
        "hexaco": {"H": 2.3, "E": 4.7, "X": 1.9, "A": 3.6, "C": 2.1, "O": 4.4},  # Шкала 1-5
        "soft_skills": {"Коммуникация": 7.8, "Лидерство": 6.3, "Креативность": 8.9, "Адаптивность": 5.4}  # Шкала 1-10
    }
    
    print("📈 Исходные данные:")
    for test_type, scores in original_data.items():
        print(f"   {test_type.upper()}: {scores}")
    
    # Нормализация
    print("\n🔄 Применяем нормализацию...")
    normalized_data = {}
    normalization_info = {}
    
    for test_type, scores in original_data.items():
        norm_scores, method = ScaleNormalizer.auto_normalize(test_type.upper(), scores)
        normalized_data[test_type] = norm_scores
        normalization_info[test_type] = method
        print(f"   {test_type.upper()}: {norm_scores} ({method})")
    
    # Создание отчета
    print("\n📄 Создание PDF отчета...")
    
    try:
        generator = EnhancedPDFReportV2()
        
        # Подготавливаем данные для отчета
        participant_info = {
            "name": "Демо Тестирование",
            "age": 30,
            "position": "Специалист по тестированию",
            "department": "IT отдел",
            "test_date": datetime.now().strftime("%d.%m.%Y"),
            "interpretation_type": "Демонстрация нормализации"
        }
        
        # Создаем отчет с нормализованными данными
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"demo_normalized_report_{timestamp}.pdf"
        out_path = Path(filename)
        
        # Подготавливаем AI интерпретации (заглушки)
        ai_interpretations = {
            "paei": "Демонстрационная интерпретация PAEI с нормализованными значениями",
            "disc": "Демонстрационная интерпретация DISC с нормализованными значениями", 
            "hexaco": "Демонстрационная интерпретация HEXACO с нормализованными значениями",
            "soft_skills": "Демонстрационная интерпретация Soft Skills с нормализованными значениями"
        }
        
        pdf_path = generator.generate_enhanced_report(
            participant_name=participant_info["name"],
            test_date=participant_info["test_date"],
            paei_scores=normalized_data["paei"],
            disc_scores=normalized_data["disc"],
            hexaco_scores=normalized_data["hexaco"],
            soft_skills_scores=normalized_data["soft_skills"],
            ai_interpretations=ai_interpretations,
            out_path=out_path
        )
        
        print(f"✅ Отчет создан: {pdf_path}")
        
        # Добавляем информацию о нормализации в отчет
        print("\n📋 Примененная нормализация:")
        for test_type, method in normalization_info.items():
            print(f"   {test_type.upper()}: {method}")
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Ошибка создания отчета: {e}")
        return None

def demo_rounding_comparison():
    """Демонстрируем сравнение до и после округления"""
    print("\n🔍 Демонстрация округления:")
    print("=" * 60)
    
    # Примеры с высокой точностью
    test_cases = [
        ("PAEI", {"P": 1, "A": 2, "E": 1, "I": 1}),  # 1/5=0.2 -> 2.0, 2/5=0.4 -> 4.0
        ("DISC", {"D": 1, "I": 2, "S": 0, "C": 5}),  # 1/6=0.1666... -> 1.7, 2/6=0.3333... -> 3.3
        ("HEXACO", {"H": 1.33, "E": 2.67, "X": 3.14, "A": 4.99, "C": 1.01, "O": 4.44}),
    ]
    
    for test_type, scores in test_cases:
        print(f"\n{test_type} пример:")
        print(f"  Исходные значения: {scores}")
        
        # Имитируем расчет без округления
        if test_type == "PAEI":
            max_questions = 5
            raw_normalized = {k: (v / max_questions) * 10 for k, v in scores.items()}
        elif test_type == "DISC":
            max_questions = 6
            raw_normalized = {k: (v / max_questions) * 10 for k, v in scores.items()}
        elif test_type == "HEXACO":
            raw_normalized = {k: ((v - 1) / 4) * 10 for k, v in scores.items()}
        
        print(f"  Без округления:   {raw_normalized}")
        
        # С округлением
        normalized, method = ScaleNormalizer.auto_normalize(test_type, scores)
        print(f"  С округлением:    {normalized}")
        print(f"  Улучшение:        Все значения до 1 знака после запятой ✅")

if __name__ == "__main__":
    demo_rounding_comparison()
    
    print("\n" + "="*60)
    pdf_path = create_demo_normalized_report()
    
    if pdf_path:
        print(f"\n🎉 Демонстрационный отчет готов!")
        print(f"📁 Файл: {pdf_path}")
        print(f"📊 Все значения в диаграммах округлены до 1 десятичного знака")
        print(f"🔄 Применена корректная нормализация шкал")