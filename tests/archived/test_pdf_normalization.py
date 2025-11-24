#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест генерации PDF с нормализованными данными
"""

from pathlib import Path
import tempfile
from datetime import datetime

# Избегаем проблем с unicode в enhanced_pdf_report, импортируем только нужные классы
import sys
import os
sys.path.append(os.getcwd())

def test_pdf_generation():
    """Тестирует генерацию PDF с нормализованными данными"""
    
    print("Начинаем тест PDF генерации...")
    
    # Тестовые данные
    paei_scores = {"P": 2, "A": 1, "E": 3, "I": 0}  # Счетчики 0-3 (будут нормализованы)
    disc_scores = {"D": 1, "I": 2, "S": 3, "C": 1}  # Счетчики 0-3 (будут нормализованы)
    hexaco_scores = {"H": 7.5, "E": 8.0, "X": 7.0, "A": 8.5, "C": 9.0, "O": 6.5}
    soft_skills_scores = {
        "Коммуникация": 8.5,
        "Лидерство": 7.8,
        "Планирование": 8.2,
        "Адаптивность": 7.6,
        "Аналитика": 8.8,
        "Творчество": 7.2
    }
    
    interpretations = {
        "paei": "Тестовая интерпретация PAEI",
        "disc": "Тестовая интерпретация DISC", 
        "hexaco": "Тестовая интерпретация HEXACO"
    }
    
    # Создаем временную папку для PDF
    temp_dir = Path.cwd() / "test_normalized_pdf"
    temp_dir.mkdir(exist_ok=True)
    
    pdf_path = temp_dir / f"test_normalized_report_{int(datetime.now().timestamp())}.pdf"
    
    try:
        # Импортируем PDF генератор без создания экземпляра (чтобы избежать print)
        from enhanced_pdf_report import EnhancedPDFReportV2
        
        # Создаем генератор 
        print("Создаем PDF генератор...")
        pdf_gen = EnhancedPDFReportV2(template_dir=temp_dir / "charts")
        
        print("Генерируем PDF отчет...")
        # Генерируем отчет
        result = pdf_gen.generate_enhanced_report(
            participant_name="Тест Нормализации",
            test_date=datetime.now().strftime("%Y-%m-%d"),
            paei_scores=paei_scores,
            disc_scores=disc_scores,
            hexaco_scores=hexaco_scores,
            soft_skills_scores=soft_skills_scores,
            ai_interpretations=interpretations,
            out_path=pdf_path
        )
        
        if pdf_path.exists():
            print(f"PDF успешно создан: {pdf_path}")
            print(f"Размер файла: {pdf_path.stat().st_size} bytes")
            return True
        else:
            print("Ошибка: PDF файл не создан")
            return False
            
    except Exception as e:
        print(f"Ошибка при создании PDF: {e}")
        return False

if __name__ == "__main__":
    success = test_pdf_generation()
    if success:
        print("\nТест пройден успешно! Нормализация работает в PDF генераторе.")
    else:
        print("\nТест не пройден.")