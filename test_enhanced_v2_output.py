#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ТЕСТ ГЕНЕРАТОРА enhanced_pdf_report_v2.py
Создание отчета с загрузкой в Google Drive
"""

from pathlib import Path
from datetime import datetime
from enhanced_pdf_report_v2 import EnhancedPDFReportV2

def test_enhanced_report():
    """
    Тест создания расширенного отчета с загрузкой в Google Drive
    """
    print("🚀 ТЕСТ ENHANCED PDF REPORT V2")
    print("=" * 50)
    
    # Создание экземпляра генератора
    generator = EnhancedPDFReportV2()
    
    # Подготовка данных
    participant_name = "Тестовый Пользователь Enhanced"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    # Тестовые данные для всех методик
    paei_scores = {"P": 8, "A": 6, "E": 9, "I": 7}
    disc_scores = {"D": 7, "I": 8, "S": 5, "C": 6}
    hexaco_scores = {"H": 4, "E": 3, "X": 5, "A": 4, "C": 5, "O": 4}
    
    soft_skills_scores = {
        "Лидерство": 8, "Коммуникация": 9, "Креативность": 7,
        "Аналитика": 6, "Адаптивность": 8, "Командная работа": 9,
        "Эмпатия": 8, "Критическое мышление": 7, 
        "Управление временем": 6, "Решение проблем": 8
    }
    
    # AI интерпретации (обязательные для расширенного отчета)
    ai_interpretations = {
        "PAEI": """
        На основе результатов тестирования PAEI выявлен преобладающий стиль Предпринимателя (E=9). 
        Это указывает на высокую креативность, стратегическое мышление и способность к инновациям. 
        Сильные позиции Производителя (P=8) дополняют профиль ориентацией на результат.
        """,
        "DISC": """
        Профиль DISC показывает комбинацию Влияния (I=8) и Доминирования (D=7). 
        Такая комбинация характерна для харизматичных лидеров, способных вдохновлять команду 
        и принимать быстрые решения. Низкие показатели S и C указывают на предпочтение динамичной среды.
        """,
        "HEXACO": """
        Личностный профиль HEXACO демонстрирует сбалансированные показатели с акцентом на 
        Экстраверсию (X=5) и Добросовестность (C=5). Умеренные значения других факторов 
        указывают на гибкость в поведении и адаптивность к различным ситуациям.
        """,
        "SOFT_SKILLS": """
        Анализ мягких навыков выявляет особые сильные стороны в области Коммуникации (9) 
        и Командной работы (9). Высокие показатели Лидерства (8) и Эмпатии (8) подтверждают 
        потенциал для управленческих ролей. Области для развития: Управление временем (6).
        """
    }
    
    # Создание имени файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = Path(f"enhanced_report_{timestamp}.pdf")
    
    try:
        print(f"📄 Создание отчета: {out_path}")
        print(f"👤 Участник: {participant_name}")
        print(f"📅 Дата: {test_date}")
        print()
        
        # Генерация отчета с Google Drive
        pdf_path, gdrive_link = generator.generate_enhanced_report_with_gdrive(
            participant_name=participant_name,
            test_date=test_date,
            paei_scores=paei_scores,
            disc_scores=disc_scores,
            hexaco_scores=hexaco_scores,
            soft_skills_scores=soft_skills_scores,
            ai_interpretations=ai_interpretations,
            out_path=out_path,
            upload_to_gdrive=True
        )
        
        print("✅ ОТЧЕТ СОЗДАН УСПЕШНО!")
        print(f"📄 Локальный файл: {pdf_path}")
        
        if gdrive_link:
            print(f"☁️ Google Drive: {gdrive_link}")
        else:
            print("⚠️ Google Drive: загрузка не выполнена")
        
        # Проверка размера файла
        if pdf_path.exists():
            size = pdf_path.stat().st_size
            size_kb = size / 1024
            print(f"📊 Размер файла: {size} байт ({size_kb:.1f} KB)")
            
            if size > 100000:  # Больше 100KB
                print("✅ Размер соответствует расширенному отчету")
            else:
                print("⚠️ Размер меньше ожидаемого")
        
        return pdf_path, gdrive_link
        
    except Exception as e:
        print(f"❌ Ошибка создания отчета: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    test_enhanced_report()