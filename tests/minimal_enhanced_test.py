#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
МИНИМАЛЬНЫЙ ТЕСТ enhanced_pdf_report_v2.py
Проверяем по шагам
"""

from pathlib import Path
from datetime import datetime
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
import traceback
import sys

def minimal_test():
    """
    Минимальный тест с перехватом всех ошибок
    """
    print("🔍 МИНИМАЛЬНЫЙ ТЕСТ ENHANCED PDF")
    print("=" * 50)
    
    try:
        print("1️⃣ Создание генератора...")
        generator = EnhancedPDFReportV2()
        print("✅ Генератор создан")
        
        print("2️⃣ Подготовка минимальных данных...")
        participant_name = "Test User"
        test_date = "2025-10-05"
        
        # Минимальные данные
        paei_scores = {"P": 5, "A": 5, "E": 5, "I": 5}
        disc_scores = {"D": 5, "I": 5, "S": 5, "C": 5}
        hexaco_scores = {"H": 3, "E": 3, "X": 3, "A": 3, "C": 3, "O": 3}
        soft_skills_scores = {"Лидерство": 5, "Коммуникация": 5}
        
        ai_interpretations = {
            "PAEI": "Test PAEI interpretation",
            "DISC": "Test DISC interpretation",
            "HEXACO": "Test HEXACO interpretation", 
            "SOFT_SKILLS": "Test soft skills interpretation"
        }
        print("✅ Данные подготовлены")
        
        print("3️⃣ Создание PDF...")
        out_path = Path("minimal_test.pdf")
        
        # Перенаправляем все ошибки в файл для анализа
        with open("debug_log.txt", "w", encoding="utf-8") as log_file:
            original_stderr = sys.stderr
            sys.stderr = log_file
            
            try:
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
            finally:
                sys.stderr = original_stderr
        
        print("✅ Генерация завершена")
        
        print("4️⃣ Проверка результата...")
        if out_path.exists():
            size = out_path.stat().st_size
            print(f"✅ Файл создан: {out_path}")
            print(f"📊 Размер: {size} байт")
            
            # Читаем лог ошибок
            if Path("debug_log.txt").exists():
                with open("debug_log.txt", "r", encoding="utf-8") as f:
                    log_content = f.read()
                    if log_content.strip():
                        print("⚠️ Найдены предупреждения/ошибки:")
                        print(log_content)
                    else:
                        print("✅ Ошибок не найдено")
        else:
            print("❌ Файл не создан")
            
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    minimal_test()