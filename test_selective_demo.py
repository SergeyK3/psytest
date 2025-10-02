#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрационный отчет с селективной нормализацией
"""

import sys
sys.path.append('.')

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from scale_normalizer import ScaleNormalizer
from datetime import datetime
from pathlib import Path

def create_selective_normalization_demo():
    """Создаем демонстрационный отчет с селективной нормализацией"""
    print("📊 Создание демонстрационного отчета с селективной нормализацией...")
    
    # Тестовые данные ДО нормализации
    original_data = {
        "paei": {"P": 1, "A": 5, "E": 2, "I": 0},  # Максимум A=5, нормализуется
        "disc": {"D": 6, "I": 1, "S": 2, "C": 0},  # Максимум D=6, нормализуется
        "hexaco": {"H": 2.3, "E": 4.7, "X": 1.9, "A": 3.6, "C": 2.1, "O": 4.4},  # Остается 1-5
        "soft_skills": {"Коммуникация": 7.8, "Лидерство": 6.3, "Креативность": 8.9, "Адаптивность": 5.4}  # Остается 1-10
    }
    
    print("📈 Исходные данные:")
    for test_type, scores in original_data.items():
        print(f"   {test_type.upper()}: {scores}")
    
    # Применяем селективную нормализацию
    print("\n🔄 Применяем селективную нормализацию...")
    processed_data = {}
    normalization_info = {}
    
    for test_type, scores in original_data.items():
        processed_scores, method = ScaleNormalizer.auto_normalize(test_type.upper(), scores)
        processed_data[test_type] = processed_scores
        normalization_info[test_type] = method
        print(f"   {test_type.upper()}: {processed_scores}")
        print(f"      └─ {method}")
    
    # Создание отчета
    print("\n📄 Создание PDF отчета...")
    
    try:
        generator = EnhancedPDFReportV2()
        
        # Подготавливаем AI интерпретации
        ai_interpretations = {
            "paei": "PAEI с селективной нормализацией: значения приведены к шкале 0-10 для корректного отображения пропорций",
            "disc": "DISC с селективной нормализацией: значения приведены к шкале 0-10 для корректного отображения пропорций", 
            "hexaco": "HEXACO без нормализации: сохранена оригинальная шкала 1-5 для правильной психологической интерпретации",
            "soft_skills": "Soft Skills без нормализации: сохранена оригинальная шкала 1-10 для правильной оценки навыков"
        }
        
        # Создаем отчет
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"selective_normalization_demo_{timestamp}.pdf"
        out_path = Path(filename)
        
        pdf_path = generator.generate_enhanced_report(
            participant_name="Демо Селективная Нормализация",
            test_date=datetime.now().strftime("%d.%m.%Y"),
            paei_scores=processed_data["paei"],
            disc_scores=processed_data["disc"],
            hexaco_scores=processed_data["hexaco"],
            soft_skills_scores=processed_data["soft_skills"],
            ai_interpretations=ai_interpretations,
            out_path=out_path
        )
        
        print(f"✅ Отчет создан: {pdf_path}")
        
        # Показываем сводку изменений
        print(f"\n📋 Сводка селективной нормализации:")
        print(f"   📈 PAEI: {original_data['paei']} → {processed_data['paei']}")
        print(f"      └─ Нормализовано к 0-10 (A: 5→10.0)")
        print(f"   📈 DISC: {original_data['disc']} → {processed_data['disc']}")
        print(f"      └─ Нормализовано к 0-10 (D: 6→10.0)")
        print(f"   📊 HEXACO: остался без изменений (шкала 1-5)")
        print(f"   📊 SOFT_SKILLS: остался без изменений (шкала 1-10)")
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Ошибка создания отчета: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    pdf_path = create_selective_normalization_demo()
    
    if pdf_path:
        print(f"\n🎉 Демонстрационный отчет с селективной нормализацией готов!")
        print(f"📁 Файл: {pdf_path}")
        print(f"\n🔍 Особенности:")
        print(f"   ✅ PAEI/DISC: нормализованы к 0-10 для правильных пропорций диаграмм")
        print(f"   ✅ HEXACO: оригинальная шкала 1-5 для корректной интерпретации")
        print(f"   ✅ SOFT_SKILLS: оригинальная шкала 1-10 для корректной оценки")
        print(f"   ✅ Все значения округлены до 1 десятичного знака")
    else:
        print("❌ Не удалось создать отчет")