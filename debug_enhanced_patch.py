#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ПАТЧ ДЛЯ ДИАГНОСТИКИ enhanced_pdf_report_v2.py
Добавляет отладочный вывод
"""

from pathlib import Path
from datetime import datetime
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
import traceback

class DebugEnhancedPDFReportV2(EnhancedPDFReportV2):
    """
    Отладочная версия с выводом информации о процессе
    """
    
    def generate_enhanced_report(self, *args, **kwargs):
        """
        Переопределенный метод с отладкой
        """
        print("🔍 DEBUG: Начало генерации enhanced report")
        
        # Вызываем оригинальный метод с перехватом
        try:
            result = super().generate_enhanced_report(*args, **kwargs)
            print(f"🔍 DEBUG: Генерация завершена, результат: {result}")
            
            # Проверяем размер созданного файла
            if result and result.exists():
                size = result.stat().st_size
                print(f"🔍 DEBUG: Размер файла: {size} байт")
                
                if size < 5000:
                    print("⚠️ DEBUG: Файл слишком маленький, возможна ошибка!")
                    # Попробуем прочитать первые строки
                    try:
                        with open(result, 'rb') as f:
                            first_bytes = f.read(100)
                            print(f"🔍 DEBUG: Первые байты: {first_bytes}")
                    except Exception as e:
                        print(f"🔍 DEBUG: Ошибка чтения файла: {e}")
            
            return result
            
        except Exception as e:
            print(f"❌ DEBUG: Ошибка в генерации: {e}")
            traceback.print_exc()
            raise

def debug_test():
    """
    Тест с отладочной версией
    """
    print("🚀 ОТЛАДОЧНЫЙ ТЕСТ ENHANCED PDF")
    print("=" * 50)
    
    generator = DebugEnhancedPDFReportV2()
    
    # Минимальные данные
    participant_name = "Debug User"
    test_date = "2025-10-05"
    
    paei_scores = {"P": 5, "A": 5, "E": 5, "I": 5}
    disc_scores = {"D": 5, "I": 5, "S": 5, "C": 5}
    hexaco_scores = {"H": 3, "E": 3, "X": 3, "A": 3, "C": 3, "O": 3}
    soft_skills_scores = {"Лидерство": 5, "Коммуникация": 5}
    
    ai_interpretations = {
        "PAEI": "Test PAEI interpretation with more text to see if content affects size",
        "DISC": "Test DISC interpretation with more text to see if content affects size",
        "HEXACO": "Test HEXACO interpretation with more text to see if content affects size", 
        "SOFT_SKILLS": "Test soft skills interpretation with more text to see if content affects size"
    }
    
    out_path = Path("debug_enhanced_v2.pdf")
    
    try:
        result = generator.generate_enhanced_report(
            participant_name=participant_name,
            test_date=test_date,
            paei_scores=paei_scores,
            disc_scores=disc_scores,
            hexaco_scores=hexaco_scores,
            soft_skills_scores=soft_skills_scores,
            ai_interpretations=ai_interpretations,
            out_path=out_path
        )
        
        print(f"✅ Результат: {result}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    debug_test()