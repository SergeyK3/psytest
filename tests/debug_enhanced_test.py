#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ДИАГНОСТИЧЕСКИЙ ТЕСТ enhanced_pdf_report_v2.py
С подробным выводом ошибок
"""

from pathlib import Path
from datetime import datetime
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
import traceback

def debug_enhanced_report():
    """
    Диагностический тест с подробным выводом
    """
    print("🔍 ДИАГНОСТИЧЕСКИЙ ТЕСТ ENHANCED PDF")
    print("=" * 50)
    
    try:
        # Создание экземпляра генератора
        print("1️⃣ Создание генератора...")
        generator = EnhancedPDFReportV2()
        print("✅ Генератор создан")
        
        # Подготовка данных
        print("2️⃣ Подготовка данных...")
        participant_name = "Debug Test User"
        test_date = datetime.now().strftime("%Y-%m-%d")
        
        paei_scores = {"P": 8, "A": 6, "E": 9, "I": 7}
        disc_scores = {"D": 7, "I": 8, "S": 5, "C": 6}
        hexaco_scores = {"H": 4, "E": 3, "X": 5, "A": 4, "C": 5, "O": 4}
        
        soft_skills_scores = {
            "Лидерство": 8, "Коммуникация": 9, "Креативность": 7,
            "Аналитика": 6, "Адаптивность": 8, "Командная работа": 9,
            "Эмпатия": 8, "Критическое мышление": 7, 
            "Управление временем": 6, "Решение проблем": 8
        }
        
        ai_interpretations = {
            "PAEI": "Тестовое описание PAEI профиля...",
            "DISC": "Тестовое описание DISC стиля...", 
            "HEXACO": "Тестовое описание HEXACO личности...",
            "SOFT_SKILLS": "Тестовое описание мягких навыков..."
        }
        print("✅ Данные подготовлены")
        
        # Создание файла
        print("3️⃣ Создание PDF файла...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = Path(f"debug_enhanced_{timestamp}.pdf")
        
        print(f"   Файл: {out_path}")
        print(f"   Участник: {participant_name}")
        
        # Генерация только локально (без Google Drive для диагностики)
        print("4️⃣ Запуск генерации (без Google Drive)...")
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
        
        print("✅ Генерация завершена")
        
        # Проверка результата
        print("5️⃣ Проверка результата...")
        if pdf_path.exists():
            size = pdf_path.stat().st_size
            size_kb = size / 1024
            print(f"✅ Файл создан: {pdf_path}")
            print(f"📊 Размер: {size} байт ({size_kb:.1f} KB)")
            
            if size > 50000:
                print("✅ Размер соответствует полному отчету")
            else:
                print("⚠️ Размер меньше ожидаемого - возможны проблемы")
        else:
            print("❌ Файл не создан")
            
        return pdf_path
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        print("📋 Подробная информация:")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    debug_enhanced_report()