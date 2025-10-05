#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой запуск enhanced_pdf_report_v2.py
"""

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

def run_enhanced_report():
    """Запускает enhanced_pdf_report_v2 с правильными параметрами"""
    
    print("🚀 ЗАПУСК ENHANCED PDF REPORT V2")
    print("=" * 50)
    
    try:
        # Создаем генератор
        generator = EnhancedPDFReportV2()
        
        # Тестовые данные в правильном формате
        test_data = {
            'participant_name': 'Enhanced Report Test',
            'test_date': datetime.now().strftime("%Y-%m-%d"),
            
            # PAEI в правильном формате
            'paei_scores': {
                'P': 8,  # Производитель
                'A': 6,  # Администратор  
                'E': 9,  # Предприниматель
                'I': 7   # Интегратор
            },
            
            # DISC в правильном формате
            'disc_scores': {
                'D': 7,  # Доминирование
                'I': 8,  # Влияние
                'S': 5,  # Постоянство
                'C': 6   # Соответствие
            },
            
            # HEXACO
            'hexaco_scores': {
                'H': 4, 'E': 3, 'X': 5, 'A': 4, 'C': 5, 'O': 4
            },
            
            # Soft Skills
            'soft_skills_scores': {
                "Лидерство": 8,
                "Коммуникация": 9, 
                "Креативность": 7,
                "Аналитика": 6,
                "Адаптивность": 8,
                "Командная работа": 9,
                "Эмпатия": 7,
                "Критическое мышление": 6,
                "Управление временем": 8,
                "Решение проблем": 7
            },
            
            # AI интерпретации
            'ai_interpretations': {
                'overall': 'Комплексный анализ показывает сбалансированный профиль с выраженными лидерскими качествами.',
                'paei': 'По PAEI выявлена склонность к предпринимательской деятельности.',
                'disc': 'DISC профиль показывает сбалансированное сочетание влияния и доминирования.',
                'hexaco': 'HEXACO демонстрирует психологическую стабильность.',
                'soft_skills': 'Анализ soft skills выявляет сильные стороны в коммуникации.'
            }
        }
        
        print("📊 Создание отчета с enhanced_pdf_report_v2...")
        
        # Путь для выходного файла
        output_path = Path("temp_charts") / f"enhanced_report_{test_data['participant_name'].replace(' ', '_')}.pdf"
        
        # Генерируем отчет
        pdf_path, gdrive_link = generator.generate_enhanced_report_with_gdrive(
            out_path=output_path,
            **test_data
        )
        
        print(f"✅ Отчет создан: {pdf_path}")
        
        if gdrive_link:
            print(f"🔗 Google Drive: {gdrive_link}")
        else:
            print("⚠️ Google Drive: не загружен")
            
        return pdf_path, gdrive_link
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_enhanced_report()