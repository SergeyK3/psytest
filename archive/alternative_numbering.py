#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
РАБОЧИЙ ПОДХОД ДЛЯ ДОБАВЛЕНИЯ НУМЕРАЦИИ СТРАНИЦ
Обходит проблему с canvasmaker в ReportLab 4.4.4
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
import io
from PyPDF2 import PdfReader, PdfWriter

def add_page_numbers_to_pdf(input_pdf_path: str, output_pdf_path: str) -> str:
    """
    ПОСТ-ОБРАБОТКА: добавляет номера страниц к готовому PDF
    
    Args:
        input_pdf_path: путь к исходному PDF без нумерации
        output_pdf_path: путь для сохранения PDF с нумерацией
    
    Returns:
        путь к готовому файлу
    """
    print(f"📄 Добавляем нумерацию к PDF: {input_pdf_path}")
    
    # Читаем исходный PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    total_pages = len(reader.pages)
    
    print(f"📊 Всего страниц для нумерации: {total_pages}")
    
    for page_num in range(total_pages):
        # Берем страницу из исходного PDF
        page = reader.pages[page_num]
        
        # Создаем overlay с номером страницы
        overlay = create_page_number_overlay(page_num + 1, total_pages)
        
        # Накладываем номер на страницу
        page.merge_page(overlay)
        writer.add_page(page)
        
        print(f"✅ Добавлен номер на страницу {page_num + 1}")
    
    # Сохраняем результат
    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"🎉 PDF с нумерацией сохранен: {output_pdf_path}")
    return output_pdf_path

def create_page_number_overlay(page_num: int, total_pages: int):
    """
    Создает overlay с номером страницы
    """
    # Создаем временный PDF с номером страницы
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    # НАСТРОЙКИ ПОЗИЦИИ И ШРИФТА
    # Правый верхний угол с отступом от края
    x_position = A4[0] - 15*mm  # 15мм от правого края
    y_position = A4[1] - 10*mm  # 10мм от верхнего края
    
    # Шрифт и размер
    can.setFont("Helvetica", 10)
    can.setFillColor(black)
    
    # Текст нумерации на русском
    page_text = f"Стр. {page_num} из {total_pages}"
    
    # Рисуем номер страницы
    can.drawRightString(x_position, y_position, page_text)
    
    can.save()
    
    # Возвращаем созданную страницу как overlay
    packet.seek(0)
    overlay_pdf = PdfReader(packet)
    return overlay_pdf.pages[0]

# АЛЬТЕРНАТИВНЫЙ ПОДХОД 2: ИСПОЛЬЗОВАНИЕ PLATYPUS PAGETEMPLATE

from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_RIGHT

class NumberedPageTemplate(PageTemplate):
    """
    Шаблон страницы с автоматической нумерацией
    """
    def __init__(self, id='numbered', **kwargs):
        # Основная область для контента
        frame = Frame(
            20*mm, 20*mm,  # x, y (левый нижний угол)
            A4[0] - 40*mm, A4[1] - 40*mm,  # width, height
            id='main'
        )
        super().__init__(id, frames=[frame], **kwargs)
    
    def beforeDrawPage(self, canvas, doc):
        """
        Вызывается ПЕРЕД рисованием каждой страницы
        """
        # Получаем номер текущей страницы
        page_num = canvas.getPageNumber()
        
        # Рисуем номер страницы в правом верхнем углу
        canvas.saveState()
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(black)
        
        # Позиция для номера страницы
        x_position = A4[0] - 15*mm
        y_position = A4[1] - 10*mm
        
        # ПРОБЛЕМА: мы не знаем общее количество страниц на этом этапе!
        # Поэтому используем временный формат
        page_text = f"Стр. {page_num}"
        canvas.drawRightString(x_position, y_position, page_text)
        
        canvas.restoreState()

def create_pdf_with_template_numbering(filename: str, story_content):
    """
    ПОДХОД 3: Использование PageTemplate для нумерации
    """
    # Создаем BaseDocTemplate вместо SimpleDocTemplate
    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=25*mm,  # Больше места для номера страницы
        bottomMargin=20*mm,
    )
    
    # Добавляем шаблон с нумерацией
    template = NumberedPageTemplate()
    doc.addPageTemplates([template])
    
    # Строим документ
    doc.build(story_content)
    
    return filename

if __name__ == "__main__":
    print("🔧 Тестируем альтернативные подходы для нумерации страниц")
    
    # Можно протестировать post-processing подход
    # add_page_numbers_to_pdf("input.pdf", "output_with_numbers.pdf")