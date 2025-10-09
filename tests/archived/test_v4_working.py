#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ТЕСТ РАБОЧЕЙ ВЕРСИИ enhanced_pdf_report_v2.py из коммита v4.0.0
"""

from pathlib import Path
from datetime import datetime
from enhanced_pdf_report_v2 import EnhancedPDFReportV2

def test_v4_working_version():
    """
    Тест рабочей версии enhanced_pdf_report_v2.py из v4.0.0
    """
    print("🚀 ТЕСТ РАБОЧЕЙ ВЕРСИИ V4.0.0")
    print("=" * 50)
    
    # Создание генератора
    generator = EnhancedPDFReportV2()
    
    # Тестовые данные
    participant_name = "Рабочий Тест V4.0"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    paei_scores = {"P": 8, "A": 6, "E": 9, "I": 7}
    disc_scores = {"D": 7, "I": 8, "S": 5, "C": 6}
    hexaco_scores = {"H": 4, "E": 3, "X": 5, "A": 4, "C": 5, "O": 4}
    
    soft_skills_scores = {
        "Лидерство": 8, "Коммуникация": 9, "Креативность": 7, "Аналитика": 6,
        "Адаптивность": 8, "Командная работа": 9, "Эмпатия": 8, 
        "Критическое мышление": 7, "Управление временем": 6, "Решение проблем": 8
    }
    
    # AI интерпретации (простые для v4.0)
    ai_interpretations = {
        "paei": "Преобладающий стиль Предпринимателя с высокими показателями Производителя",
        "disc": "Доминирующий тип с высокой инициативностью и ориентацией на результат",
        "hexaco": "Сбалансированный профиль с умеренными показателями по всем факторам"
    }
    
    # Создание файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = Path(f"test_v4_working_{timestamp}.pdf")
    
    print(f"📄 Создание отчета: {out_path}")
    print(f"👤 Участник: {participant_name}")
    print()
    
    try:
        # Генерация отчета (v4.0 версия)
        pdf_path = generator.generate_enhanced_report(
            participant_name=participant_name,
            test_date=test_date,
            paei_scores=paei_scores,
            disc_scores=disc_scores,
            hexaco_scores=hexaco_scores,
            soft_skills_scores=soft_skills_scores,
            ai_interpretations=ai_interpretations,
            out_path=out_path
        )
        
        print("✅ ОТЧЕТ V4.0 СОЗДАН!")
        print(f"📄 Файл: {pdf_path}")
        
        # Проверка размера
        if pdf_path.exists():
            size = pdf_path.stat().st_size
            size_kb = size / 1024
            print(f"📊 Размер файла: {size} байт ({size_kb:.1f} KB)")
            
            if size > 100000:  # Больше 100KB
                print("✅ Отличный размер - полный отчет с графиками!")
            elif size > 10000:  # Больше 10KB
                print("✅ Хороший размер - отчет создан")
            else:
                print("⚠️ Маленький размер - возможны проблемы")
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_v4_working_version()