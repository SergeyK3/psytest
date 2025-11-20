#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест создания PDF с кириллицей для диагностики проблемы с черными квадратиками
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm
from reportlab.lib.colors import black

def test_cyrillic_pdf():
    """Создает простой PDF с кириллицей для диагностики"""
    
    output_path = Path("test_cyrillic.pdf")
    
    # Создание PDF документа
    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    
    # Получение стилей
    styles = getSampleStyleSheet()
    
    # Создание пользовательского стиля
    custom_style = ParagraphStyle(
        name='CustomRussian',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Times-Roman',  # Встроенный шрифт
        textColor=black,
    )
    
    # Создание содержимого
    story = []
    
    # Тестовые строки с кириллицей
    test_texts = [
        "ПСИХОЛОГИЧЕСКИЙ ПОРТРЕТ СОТРУДНИКА",
        "Имя сотрудника: Петров Василий",
        "Дата тестирования: 25-01-25",
        "Результаты тестирования:",
        "• Диаграмма PAEI (Адизес): P: 18, A: 15, E: 16, I: 12",
        "• Диаграмма DISC: D: 9, I: 7, S: 3, C: 6",
        "КРАТКИЕ ВЫВОДЫ",
        "По Адизесу: Ярко выраженный Producer (Производитель) с сильными административными навыками...",
    ]
    
    for text in test_texts:
        story.append(Paragraph(text, custom_style))
        story.append(Spacer(1, 5*mm))
    
    # Сборка PDF
    try:
        doc.build(story)
        print(f"✅ Тестовый PDF создан: {output_path}")
        print("💡 Откройте файл для проверки отображения кириллицы")
        
        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"📊 Размер файла: {size_kb:.1f} KB")
            
    except Exception as e:
        print(f"❌ Ошибка при создании PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cyrillic_pdf()