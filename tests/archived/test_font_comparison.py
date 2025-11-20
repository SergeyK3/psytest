#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Продвинутый тест различных методов отображения кириллицы в PDF
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm
from reportlab.lib.colors import black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def test_font_methods():
    """Тестирует различные методы отображения кириллицы"""
    
    output_path = Path("font_test_comparison.pdf")
    
    # Создание PDF документа
    doc = SimpleDocTemplate(str(output_path), pagesize=A4,
                          topMargin=20*mm, bottomMargin=20*mm)
    
    # Получение базовых стилей
    styles = getSampleStyleSheet()
    story = []
    
    # Заголовок
    title_style = ParagraphStyle(
        name='Title',
        parent=styles['Title'],
        fontSize=16,
        fontName='Times-Bold',
        textColor=black,
        alignment=1
    )
    
    story.append(Paragraph("ТЕСТ ОТОБРАЖЕНИЯ КИРИЛЛИЦЫ В PDF", title_style))
    story.append(Spacer(1, 10*mm))
    
    # Тестовый текст
    test_text = "Психологический портрет сотрудника: Петров Василий Александрович"
    
    # 1. Times-Roman (встроенный)
    times_style = ParagraphStyle(
        name='TimesRoman',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Times-Roman',
    )
    
    story.append(Paragraph("<b>1. Times-Roman (встроенный):</b>", times_style))
    story.append(Paragraph(test_text, times_style))
    story.append(Spacer(1, 5*mm))
    
    # 2. Helvetica (встроенный)
    helvetica_style = ParagraphStyle(
        name='Helvetica',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Helvetica',
    )
    
    story.append(Paragraph("<b>2. Helvetica (встроенный):</b>", helvetica_style))
    story.append(Paragraph(test_text, helvetica_style))
    story.append(Spacer(1, 5*mm))
    
    # 3. Попытка использовать Arial Unicode (если доступен)
    arial_available = False
    try:
        windows_fonts = "C:/Windows/Fonts/"
        arial_path = os.path.join(windows_fonts, "arial.ttf")
        
        if os.path.exists(arial_path):
            pdfmetrics.registerFont(TTFont('ArialCustom', arial_path))
            arial_available = True
            
            arial_style = ParagraphStyle(
                name='ArialCustom',
                parent=styles['Normal'],
                fontSize=12,
                fontName='ArialCustom',
            )
            
            story.append(Paragraph("<b>3. Arial TTF (Windows шрифт):</b>", arial_style))
            story.append(Paragraph(test_text, arial_style))
        else:
            story.append(Paragraph("<b>3. Arial TTF:</b> Не найден", times_style))
            
    except Exception as e:
        story.append(Paragraph(f"<b>3. Arial TTF:</b> Ошибка - {e}", times_style))
    
    story.append(Spacer(1, 5*mm))
    
    # 4. Специальные символы и знаки препинания
    special_text = "ПАЭИ (PAEI): Производитель, Администратор, Предприниматель, Интегратор — роли Адизеса."
    
    story.append(Paragraph("<b>4. Специальные символы (Times-Roman):</b>", times_style))
    story.append(Paragraph(special_text, times_style))
    story.append(Spacer(1, 5*mm))
    
    # 5. Числа и формулировки
    numbers_text = "Результаты: D: 9, I: 7, S: 3, C: 6 — стиль поведения по DISC."
    
    story.append(Paragraph("<b>5. Числа и латинские буквы (Times-Roman):</b>", times_style))
    story.append(Paragraph(numbers_text, times_style))
    story.append(Spacer(1, 10*mm))
    
    # Заключение
    conclusion_style = ParagraphStyle(
        name='Conclusion',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Times-Roman',
        textColor=black,
    )
    
    story.append(Paragraph("<b>ЗАКЛЮЧЕНИЕ:</b>", conclusion_style))
    story.append(Paragraph("Если вы видите черные квадратики вместо русского текста,", conclusion_style))
    story.append(Paragraph("проблема в шрифте. Times-Roman должен поддерживать кириллицу.", conclusion_style))
    story.append(Paragraph("Если проблема остается, нужно использовать TTF шрифты.", conclusion_style))
    
    # Сборка PDF
    try:
        doc.build(story)
        print(f"✅ Тест шрифтов создан: {output_path}")
        print("📋 Проверьте следующее:")
        print("   1. Отображается ли кириллица в Times-Roman?")
        print("   2. Есть ли разница между шрифтами?")
        print("   3. Какой шрифт лучше всего подходит?")
        
        if arial_available:
            print("   ✅ Arial шрифт загружен успешно")
        else:
            print("   ⚠️  Arial шрифт не найден")
            
        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"📊 Размер файла: {size_kb:.1f} KB")
            
    except Exception as e:
        print(f"❌ Ошибка при создании PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_font_methods()