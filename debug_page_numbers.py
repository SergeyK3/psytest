#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Отладочная версия генератора с ОЧЕНЬ ЗАМЕТНОЙ нумерацией
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, red, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

class DebugNumberedCanvas(canvas.Canvas):
    """ОТЛАДОЧНЫЙ Canvas с ОЧЕНЬ ЗАМЕТНОЙ нумерацией"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Добавляем ОЧЕНЬ ЗАМЕТНЫЕ номера страниц"""
        num_pages = len(self._saved_page_states)
        for (page_num, page_state) in enumerate(self._saved_page_states):
            self.__dict__.update(page_state)
            self.draw_debug_page_number(page_num + 1, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_debug_page_number(self, page_num, total_pages):
        """ОТЛАДОЧНАЯ нумерация - делаем ее максимально заметной"""
        
        # Сохраняем текущее состояние
        self.saveState()
        
        # Устанавливаем КРАСНЫЙ цвет для заметности
        self.setFillColor(red)
        self.setStrokeColor(red)
        
        # Большой шрифт
        try:
            arial_path = "C:/Windows/Fonts/arialbd.ttf"  # Жирный Arial
            if os.path.exists(arial_path):
                pdfmetrics.registerFont(TTFont('Arial-Debug', arial_path))
                self.setFont("Arial-Debug", 14)  # Большой размер
            else:
                self.setFont("Times-Bold", 14)
        except:
            self.setFont("Times-Bold", 14)
        
        text = f"Стр. {page_num} из {total_pages}"
        
        # Рисуем нумерацию в НЕСКОЛЬКИХ местах для отладки
        
        # 1. Правый верхний угол (основная позиция)
        self.drawRightString(A4[0] - 15*mm, A4[1] - 12*mm, text)
        
        # 2. Центр верха страницы (для сравнения)
        self.drawCentredText(A4[0] / 2, A4[1] - 12*mm, f"ЦЕНТР: {text}")
        
        # 3. Левый верхний угол (для сравнения)
        self.drawString(15*mm, A4[1] - 12*mm, f"ЛЕВО: {text}")
        
        # 4. Правый низ страницы (альтернативная позиция)
        self.drawRightString(A4[0] - 15*mm, 15*mm, f"НИЗ: {text}")
        
        # Восстанавливаем состояние
        self.restoreState()

def create_debug_pdf():
    """Создает отладочный PDF с заметной нумерацией"""
    
    filename = 'debug_page_numbers.pdf'
    
    # Создаем документ с отладочным canvas
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=25*mm,
        rightMargin=25*mm,
        topMargin=30*mm,  # Больше места для отладочной нумерации
        bottomMargin=25*mm,
        canvasmaker=DebugNumberedCanvas
    )
    
    # Создаем стили
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DebugTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,
        fontName='Times-Bold'
    )
    
    normal_style = ParagraphStyle(
        'DebugNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=8,
        fontName='Times-Roman'
    )
    
    # Создаем контент
    story = []
    
    # Заголовок
    story.append(Paragraph("ОТЛАДКА НУМЕРАЦИИ СТРАНИЦ", title_style))
    story.append(Spacer(1, 30))
    
    # Инструкции
    story.append(Paragraph("ИНСТРУКЦИИ ПО ПРОВЕРКЕ:", normal_style))
    story.append(Paragraph("1. Посмотрите в ПРАВЫЙ ВЕРХНИЙ угол - основная нумерация", normal_style))
    story.append(Paragraph("2. Сверху по центру - вспомогательная нумерация", normal_style))  
    story.append(Paragraph("3. Слева сверху - контрольная нумерация", normal_style))
    story.append(Paragraph("4. Справа снизу - альтернативная позиция", normal_style))
    story.append(Paragraph("5. ВСЕ НОМЕРА ДОЛЖНЫ БЫТЬ КРАСНОГО ЦВЕТА!", normal_style))
    story.append(Spacer(1, 30))
    
    # Несколько страниц для проверки
    for page in range(1, 4):
        story.append(Paragraph(f"СТРАНИЦА {page}", title_style))
        story.append(Spacer(1, 20))
        
        for i in range(10):
            story.append(Paragraph(
                f"Тестовый параграф {i+1} на странице {page}. "
                f"Этот текст нужен для заполнения страницы и проверки нумерации. "
                f"Посмотрите вверх и вниз страницы - должна быть видна КРАСНАЯ нумерация.",
                normal_style
            ))
            story.append(Spacer(1, 8))
        
        if page < 3:  # Не добавляем разрыв после последней страницы
            story.append(PageBreak())
    
    # Строим документ
    print("🔄 Создание отладочного PDF...")
    doc.build(story)
    
    return filename

if __name__ == "__main__":
    try:
        result = create_debug_pdf()
        print(f"✅ Отладочный PDF создан: {result}")
        print("🔍 ПРОВЕРЬТЕ КРАСНУЮ НУМЕРАЦИЮ в разных углах страниц!")
        
        # Открываем файл правильной командой для PDF
        import subprocess
        try:
            # Для Windows - используем команду открытия PDF
            subprocess.run(['cmd', '/c', 'start', '', result], shell=False)
            print(f"📖 Открываем PDF: {result}")
        except Exception as e:
            print(f"⚠️ Не удалось открыть PDF автоматически: {e}")
            print(f"📁 Откройте файл вручную: {result}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()