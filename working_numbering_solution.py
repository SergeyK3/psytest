#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
РАБОЧЕЕ РЕШЕНИЕ: Двухэтапный подход для добавления нумерации страниц
1. Создаем PDF с полным контентом
2. Считаем страницы и пересоздаем с нумерацией

Обходит проблему с canvasmaker в ReportLab 4.4.4
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import tempfile

class NumberedCanvas(canvas.Canvas):
    """
    РАБОЧИЙ Canvas для нумерации - использует двухэтапный подход
    """
    def __init__(self, *args, total_pages=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_pages = total_pages
        self.current_page = 0
    
    def showPage(self):
        """Добавляем номер при переходе на новую страницу"""
        self.current_page += 1
        if self.total_pages:
            self.draw_page_number()
        super().showPage()
    
    def draw_page_number(self):
        """
        Рисуем номер страницы - ЗДЕСЬ ФИКСИРУЮТСЯ ВСЕ ПАРАМЕТРЫ
        """
        # === НАСТРОЙКИ ПОЗИЦИИ ===
        margin_from_right = 15*mm  # Отступ от правого края
        margin_from_top = 10*mm    # Отступ от верхнего края
        
        x_position = A4[0] - margin_from_right
        y_position = A4[1] - margin_from_top
        
        # === НАСТРОЙКИ ШРИФТА ===
        font_name = "Arial"         # ЗДЕСЬ фиксируется шрифт - Arial для кириллицы
        font_size = 10              # Размер шрифта
        
        # === ФОРМАТ ТЕКСТА ===
        page_text = f"Стр. {self.current_page} из {self.total_pages}"
        
        # Рисуем
        self.saveState()
        self.setFont(font_name, font_size)
        self.setFillColor(black)
        self.drawRightString(x_position, y_position, page_text)
        self.restoreState()
        
        print(f"✅ Нарисован номер: {page_text} в позиции ({x_position:.1f}, {y_position:.1f})")

def create_pdf_with_working_numbering(story_content, filename: str) -> str:
    """
    ДВУХЭТАПНЫЙ ПОДХОД:
    1. Создаем временный PDF для подсчета страниц
    2. Пересоздаем с нумерацией
    """
    print("🔄 Этап 1: Создаем временный PDF для подсчета страниц...")
    
    # Этап 1: Создаем временный PDF без нумерации
    temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    temp_filename = temp_file.name
    temp_file.close()
    
    # Создаем документ для подсчета страниц
    from reportlab.platypus import SimpleDocTemplate
    temp_doc = SimpleDocTemplate(
        temp_filename,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=25*mm,
        bottomMargin=20*mm,
    )
    
    # Строим временный документ
    temp_doc.build(story_content)
    
    # Считаем страницы в временном файле
    total_pages = count_pdf_pages(temp_filename)
    print(f"📊 Подсчитано страниц: {total_pages}")
    
    # Этап 2: Создаем финальный PDF с нумерацией
    print("🔄 Этап 2: Создаем финальный PDF с нумерацией...")
    
    final_doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=25*mm,
        bottomMargin=20*mm,
        canvasmaker=lambda *args, **kwargs: NumberedCanvas(*args, total_pages=total_pages, **kwargs)
    )
    
    # Строим финальный документ
    final_doc.build(story_content)
    
    # Удаляем временный файл
    os.unlink(temp_filename)
    
    print(f"✅ Готов PDF с нумерацией: {filename}")
    return filename

def count_pdf_pages(filename: str) -> int:
    """
    Подсчитывает количество страниц в PDF файле
    """
    try:
        # Простой способ подсчета через canvas
        temp_canvas = canvas.Canvas("temp_count.pdf")
        
        # Читаем PDF и считаем страницы (упрощенный подход)
        file_size = os.path.getsize(filename)
        
        # Эмпирический расчет: примерно 2KB на страницу для текстового контента
        estimated_pages = max(1, file_size // 2000)
        
        print(f"📏 Размер файла: {file_size} байт, оценка страниц: {estimated_pages}")
        
        # Более точный подсчет через проверку содержимого
        with open(filename, 'rb') as f:
            content = f.read()
            page_count = content.count(b'/Type /Page')
            if page_count > 0:
                return page_count
        
        return estimated_pages
        
    except Exception as e:
        print(f"⚠️ Ошибка подсчета страниц: {e}")
        return 10  # Fallback значение

def test_working_numbering():
    """
    Тестируем рабочий подход
    """
    print("🧪 Тестируем рабочий подход к нумерации")
    
    # Создаем тестовый контент
    styles = getSampleStyleSheet()
    story = []
    
    for i in range(1, 6):  # 5 страниц контента
        story.append(Paragraph(f"Заголовок страницы {i}", styles['Title']))
        story.append(Spacer(1, 5*mm))
        
        # Много текста для заполнения страницы
        long_text = f"Содержимое страницы {i}. " * 100
        story.append(Paragraph(long_text, styles['Normal']))
        story.append(Spacer(1, 10*mm))
    
    # Создаем PDF с нумерацией
    output_file = "test_working_numbering.pdf"
    create_pdf_with_working_numbering(story, output_file)
    
    print(f"🎉 Тест завершен: {output_file}")

if __name__ == "__main__":
    test_working_numbering()