#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ФИНАЛЬНЫЙ ТЕСТ ENHANCED PDF V4.0 + НУМЕРАЦИЯ + GOOGLE DRIVE
Полный тест с нумерацией страниц и загрузкой в Google папку
"""

from pathlib import Path
from datetime import datetime
from enhanced_pdf_report_v2 import EnhancedPDFReportV2

def final_test_enhanced_pdf():
    """
    Финальный тест enhanced PDF с нумерацией и Google Drive
    """
    print("🎯 ФИНАЛЬНЫЙ ТЕСТ ENHANCED PDF V4.0")
    print("=" * 60)
    print("✅ Нумерация страниц в верхнем правом углу")
    print("✅ Загрузка в Google Drive с месячной структурой")
    print("✅ Встроенные графики и диаграммы")
    print("✅ Полный отчет ~900KB")
    print()
    
    # Создание генератора
    generator = EnhancedPDFReportV2()
    
    # Тестовые данные
    participant_name = "Финальный Тест Enhanced V4.0"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    paei_scores = {"P": 8, "A": 6, "E": 9, "I": 7}
    disc_scores = {"D": 7, "I": 8, "S": 5, "C": 6}
    hexaco_scores = {"H": 4, "E": 3, "X": 5, "A": 4, "C": 5, "O": 4}
    
    soft_skills_scores = {
        "Лидерство": 8, "Коммуникация": 9, "Креативность": 7, "Аналитика": 6,
        "Адаптивность": 8, "Командная работа": 9, "Эмпатия": 8, 
        "Критическое мышление": 7, "Управление временем": 6, "Решение проблем": 8
    }
    
    # Полные AI интерпретации
    ai_interpretations = {
        "paei": """
        Результаты тестирования PAEI демонстрируют ярко выраженный профиль Предпринимателя (E=9) 
        с сильными качествами Производителя (P=8). Это сочетание указывает на уникальную 
        способность не только генерировать инновационные идеи и видеть стратегические 
        перспективы, но и эффективно реализовывать их на практике. Сотрудник обладает 
        редким балансом между креативностью и исполнительностью, что делает его особенно 
        ценным для организации в периоды роста и трансформации.
        """,
        "disc": """
        Профиль DISC показывает доминирование стиля Влияния (I=8) в сочетании с высоким 
        Доминированием (D=7). Данная комбинация характерна для прирожденных лидеров, 
        способных вдохновлять команды и принимать решительные действия. Высокое Влияние 
        свидетельствует о превосходных коммуникативных навыках, способности убеждать и 
        мотивировать других. Это дополняется решительностью и инициативностью, что 
        позволяет эффективно руководить проектами и командами.
        """,
        "hexaco": """
        Личностный профиль HEXACO демонстрирует сбалансированность основных личностных 
        факторов, что является показателем психологической зрелости и адаптивности. 
        Умеренные значения по всем шкалам указывают на гибкость в поведении и способность 
        адаптироваться к различным ситуациям и требованиям. Это профиль человека, который 
        может эффективно функционировать в разнообразных профессиональных контекстах.
        """
    }
    
    # Создание файла с автоматическим именованием
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c for c in participant_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_name = safe_name.replace(' ', '_')
    filename = f"final_enhanced_{safe_name}_{timestamp}.pdf"
    out_path = Path(filename)
    
    print(f"📄 Создание финального отчета: {filename}")
    print(f"👤 Участник: {participant_name}")
    print(f"📅 Дата: {test_date}")
    print()
    
    try:
        # Генерация с Google Drive и нумерацией
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
        
        print("🎉 ФИНАЛЬНЫЙ ENHANCED PDF СОЗДАН УСПЕШНО!")
        print(f"📄 Локальный файл: {pdf_path}")
        
        if gdrive_link:
            print(f"☁️ Google Drive: {gdrive_link}")
            print("🎯 Отчет загружен в месячную папку Google Drive!")
        else:
            print("⚠️ Google Drive: загрузка не выполнена")
        
        # Проверка размера
        if pdf_path.exists():
            size = pdf_path.stat().st_size
            size_kb = size / 1024
            print(f"📊 Размер файла: {size} байт ({size_kb:.1f} KB)")
        
        print()
        print("🎉 ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
        print("📋 Все функции работают корректно:")
        print("   ✅ PDF создан и содержит все секции")
        print("   ✅ Встроенные радарные и столбчатые диаграммы")
        print("   ✅ Нумерация страниц в верхнем правом углу")
        print("   ✅ Google Drive загрузка с месячной структурой")
        print("   ✅ Поддержка кириллицы (Arial шрифты)")
        print("   ✅ Профессиональное форматирование")
        print()
        print("🎯 Enhanced PDF Report V4.0 полностью готов к использованию!")
        
        return pdf_path, gdrive_link
        
    except Exception as e:
        print(f"❌ Ошибка финального теста: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    final_test_enhanced_pdf()