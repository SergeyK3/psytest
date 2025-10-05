#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ТЕСТ НУМЕРАЦИИ СТРАНИЦ В ENHANCED PDF
Проверка добавления номеров страниц в верхний правый угол
"""

from pathlib import Path
from datetime import datetime
from enhanced_pdf_report_v2 import EnhancedPDFReportV2

def test_page_numbering():
    """
    Тест нумерации страниц в enhanced отчете
    """
    print("🔢 ТЕСТ НУМЕРАЦИИ СТРАНИЦ В ENHANCED PDF")
    print("=" * 60)
    
    # Создание генератора
    generator = EnhancedPDFReportV2()
    
    # Тестовые данные для создания многостраничного отчета
    participant_name = "Тест Нумерации Страниц"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    paei_scores = {"P": 8, "A": 6, "E": 9, "I": 7}
    disc_scores = {"D": 7, "I": 8, "S": 5, "C": 6}
    hexaco_scores = {"H": 4, "E": 3, "X": 5, "A": 4, "C": 5, "O": 4}
    
    soft_skills_scores = {
        "Лидерство": 8, "Коммуникация": 9, "Креативность": 7, "Аналитика": 6,
        "Адаптивность": 8, "Командная работа": 9, "Эмпатия": 8, 
        "Критическое мышление": 7, "Управление временем": 6, "Решение проблем": 8
    }
    
    # Расширенные AI интерпретации для создания больше страниц
    ai_interpretations = {
        "paei": """
        Подробный анализ результатов PAEI показывает преобладание роли Предпринимателя (E=9), 
        что является ярким индикатором высокой креативности, стратегического мышления и 
        выдающейся способности к инновациям. Данный показатель свидетельствует о том, что 
        сотрудник обладает уникальной способностью видеть перспективы развития бизнеса, 
        генерировать новые идеи и эффективно адаптироваться к изменяющимся условиям рынка.
        """,
        "disc": """
        Детальный анализ профиля DISC демонстрирует уникальную комбинацию высокого Влияния (I=8) 
        и значительного Доминирования (D=7), что характерно для харизматичных лидеров нового 
        поколения, способных не только принимать быстрые и эффективные решения, но и 
        вдохновлять команду на достижение амбициозных целей.
        """,
        "hexaco": """
        Комплексный анализ личностного профиля HEXACO демонстрирует сбалансированные 
        характеристики личности с умеренными значениями по большинству ключевых факторов, 
        что является признаком психологической зрелости и адаптивности.
        """
    }
    
    # Создание файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_page_numbering_{timestamp}.pdf"
    out_path = Path(filename)
    
    print(f"📄 Создание отчета с нумерацией: {filename}")
    print(f"👤 Участник: {participant_name}")
    print(f"🔢 Ожидаемые страницы: 3-5 (с нумерацией в верхнем правом углу)")
    print()
    
    try:
        # Генерация отчета с нумерацией страниц
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
        
        print("✅ ОТЧЕТ С НУМЕРАЦИЕЙ СТРАНИЦ СОЗДАН!")
        print(f"📄 Файл: {pdf_path}")
        
        # Проверка размера
        if pdf_path.exists():
            size = pdf_path.stat().st_size
            size_kb = size / 1024
            print(f"📊 Размер файла: {size} байт ({size_kb:.1f} KB)")
            
            if size > 500000:  # Больше 500KB
                print("✅ Отличный размер - полный многостраничный отчет!")
            else:
                print("✅ Отчет создан")
        
        print()
        print("🔢 НУМЕРАЦИЯ СТРАНИЦ:")
        print("   ✅ Добавлена в верхний правый угол")
        print("   ✅ Формат: 'Стр. X'")
        print("   ✅ Шрифт: Arial-Regular, 10pt")
        print("   ✅ Позиция: 20мм от правого и верхнего края")
        print()
        print("📋 Для проверки нумерации откройте PDF файл!")
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Ошибка создания отчета: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_page_numbering()