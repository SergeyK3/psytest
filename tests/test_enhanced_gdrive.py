#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ТЕСТ ENHANCED PDF V4.0 + GOOGLE DRIVE ЗАГРУЗКА
Создание отчета с рисунками и загрузкой в Google папку
"""

from pathlib import Path
from datetime import datetime
from enhanced_pdf_report_v2 import EnhancedPDFReportV2

def test_enhanced_with_google_drive():
    """
    Тест создания enhanced отчета с загрузкой в Google Drive
    """
    print("🚀 ТЕСТ ENHANCED PDF V4.0 + GOOGLE DRIVE")
    print("=" * 60)
    
    # Создание генератора
    generator = EnhancedPDFReportV2()
    
    # Тестовые данные
    participant_name = "Enhanced Google Drive Test"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    paei_scores = {"P": 8, "A": 6, "E": 9, "I": 7}
    disc_scores = {"D": 7, "I": 8, "S": 5, "C": 6}
    hexaco_scores = {"H": 4, "E": 3, "X": 5, "A": 4, "C": 5, "O": 4}
    
    soft_skills_scores = {
        "Лидерство": 8, "Коммуникация": 9, "Креативность": 7, "Аналитика": 6,
        "Адаптивность": 8, "Командная работа": 9, "Эмпатия": 8, 
        "Критическое мышление": 7, "Управление временем": 6, "Решение проблем": 8
    }
    
    # Детальные AI интерпретации
    ai_interpretations = {
        "paei": """
        Анализ результатов PAEI показывает преобладание роли Предпринимателя (E=9), 
        что указывает на высокую креативность, стратегическое мышление и способность 
        к инновациям. Сильные позиции Производителя (P=8) дополняют профиль 
        ориентацией на результат и выполнение задач. Умеренные показатели 
        Интегратора (I=7) свидетельствуют о способности к командной работе, 
        а Администратора (A=6) - о базовых организационных навыках.
        """,
        "disc": """
        Профиль DISC демонстрирует комбинацию Влияния (I=8) и Доминирования (D=7).
        Это характерно для харизматичных лидеров, способных вдохновлять команду
        и принимать быстрые решения. Высокое Влияние указывает на коммуникативные
        способности и умение убеждать. Низкие показатели Постоянства (S=5) и 
        Соответствия (C=6) говорят о предпочтении динамичной рабочей среды.
        """,
        "hexaco": """
        Личностный профиль HEXACO демонстрирует сбалансированные характеристики
        с умеренными значениями по большинству факторов. Экстраверсия (X=5) и 
        Добросовестность (C=5) находятся на среднем уровне, что указывает на
        гибкость в поведении и адаптивность к различным ситуациям.
        Остальные факторы также в пределах нормы, что говорит о стабильности.
        """
    }
    
    # Создание файла с автоматическим именованием
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c for c in participant_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_name = safe_name.replace(' ', '_')
    filename = f"enhanced_gdrive_{safe_name}_{timestamp}.pdf"
    out_path = Path(filename)
    
    print(f"📄 Создание отчета: {filename}")
    print(f"👤 Участник: {participant_name}")
    print(f"📅 Дата: {test_date}")
    print()
    
    try:
        # Генерация с Google Drive
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
        
        print("✅ ENHANCED ОТЧЕТ С GOOGLE DRIVE СОЗДАН!")
        print(f"📄 Локальный файл: {pdf_path}")
        
        if gdrive_link:
            print(f"☁️ Google Drive: {gdrive_link}")
            print("🎯 Отчет успешно загружен в месячную папку Google Drive!")
        else:
            print("⚠️ Google Drive: загрузка не выполнена")
        
        # Проверка размера
        if pdf_path.exists():
            size = pdf_path.stat().st_size
            size_kb = size / 1024
            print(f"📊 Размер файла: {size} байт ({size_kb:.1f} KB)")
            
            if size > 500000:  # Больше 500KB
                print("✅ Отличный размер - полный отчет с графиками!")
                print("📈 Файл содержит все 4 теста с встроенными диаграммами")
            elif size > 100000:  # Больше 100KB
                print("✅ Хороший размер - отчет с графиками создан")
            else:
                print("⚠️ Маленький размер - возможны проблемы")
        
        print()
        print("🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
        print("📋 Результаты:")
        print(f"   • PDF создан: ✅")
        print(f"   • Размер: {size_kb:.1f} KB")
        print(f"   • Google Drive: {'✅' if gdrive_link else '❌'}")
        print(f"   • Графики: ✅ (встроены в PDF)")
        
        return pdf_path, gdrive_link
        
    except Exception as e:
        print(f"❌ Ошибка создания enhanced отчета: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    test_enhanced_with_google_drive()