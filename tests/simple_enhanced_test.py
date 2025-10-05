#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ПРОСТОЙ ТЕСТ ENHANCED PDF С GOOGLE DRIVE
Используем working architecture из final_full_numbered_generator.py
"""

from pathlib import Path
from datetime import datetime
from enhanced_pdf_report_v2 import EnhancedPDFReportV2

def simple_enhanced_with_gdrive():
    """
    Простой тест с Google Drive загрузкой
    """
    print("🚀 ПРОСТОЙ ТЕСТ ENHANCED PDF + GOOGLE DRIVE")
    print("=" * 60)
    
    # Создание генератора
    generator = EnhancedPDFReportV2()
    
    # Подготовка данных 
    participant_name = "Enhanced Test User"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    # Тестовые данные (аналогично final_full_numbered_generator.py)
    paei_scores = {"P": 8, "A": 6, "E": 9, "I": 7}
    disc_scores = {"D": 7, "I": 8, "S": 5, "C": 6}
    hexaco_scores = {"H": 4, "E": 3, "X": 5, "A": 4, "C": 5, "O": 4}
    
    soft_skills_scores = {
        "Лидерство": 8, "Коммуникация": 9, "Креативность": 7, "Аналитика": 6,
        "Адаптивность": 8, "Командная работа": 9, "Эмпатия": 8, 
        "Критическое мышление": 7, "Управление временем": 6, "Решение проблем": 8
    }
    
    # AI интерпретации (обязательные для enhanced)
    ai_interpretations = {
        "PAEI": """
        Анализ результатов PAEI показывает преобладание роли Предпринимателя (E=9), 
        что указывает на высокую креативность и стратегическое мышление. 
        Сильные позиции Производителя (P=8) дополняют профиль ориентацией на результат.
        Умеренные показатели Интегратора (I=7) и Администратора (A=6) указывают на 
        сбалансированный управленческий стиль с акцентом на инновации и достижения.
        """,
        "DISC": """
        Профиль DISC демонстрирует комбинацию Влияния (I=8) и Доминирования (D=7).
        Это характерно для харизматичных лидеров, способных вдохновлять команду
        и принимать быстрые решения. Низкие показатели Постоянства (S=5) и 
        Соответствия (C=6) указывают на предпочтение динамичной рабочей среды
        и готовность к изменениям.
        """,
        "HEXACO": """
        Личностный профиль HEXACO показывает сбалансированные характеристики
        с умеренными значениями по всем факторам. Экстраверсия (X=5) и 
        Добросовестность (C=5) находятся на среднем уровне, что указывает на
        гибкость в поведении и адаптивность к различным ситуациям.
        Честность (H=4) и другие факторы в норме.
        """,
        "SOFT_SKILLS": """
        Анализ мягких навыков выявляет выдающиеся способности в области
        Коммуникации (9) и Командной работы (9). Высокие показатели 
        Лидерства (8), Эмпатии (8) и Решения проблем (8) подтверждают
        потенциал для управленческих ролей. Области для развития включают
        Управление временем (6) и Аналитику (6).
        """
    }
    
    # Создание файла с автоматическим именованием
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c for c in participant_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_name = safe_name.replace(' ', '_')
    filename = f"enhanced_report_{safe_name}_{timestamp}.pdf"
    out_path = Path(filename)
    
    print(f"📄 Создание отчета: {filename}")
    print(f"👤 Участник: {participant_name}")
    print(f"📅 Дата: {test_date}")
    print()
    
    try:
        # Генерация с Google Drive (используем метод enhanced)
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
        
        print("✅ ENHANCED ОТЧЕТ СОЗДАН!")
        print(f"📄 Локальный файл: {pdf_path}")
        
        if gdrive_link:
            print(f"☁️ Google Drive: {gdrive_link}")
        else:
            print("⚠️ Google Drive: загрузка не выполнена")
        
        # Проверка размера
        if pdf_path.exists():
            size = pdf_path.stat().st_size
            size_kb = size / 1024
            print(f"📊 Размер файла: {size} байт ({size_kb:.1f} KB)")
            
            if size > 100000:  # Больше 100KB
                print("✅ Размер соответствует расширенному отчету")
            elif size > 10000:  # Больше 10KB
                print("⚠️ Размер меньше ожидаемого, но файл создан")
            else:
                print("❌ Размер критически мал")
        
        return pdf_path, gdrive_link
        
    except Exception as e:
        print(f"❌ Ошибка создания enhanced отчета: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    simple_enhanced_with_gdrive()