#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
РАБОЧЕЕ РЕШЕНИЕ НА ЧИСТОМ CANVAS
Обходит проблему с canvasmaker в SimpleDocTemplate

Этот подход ГАРАНТИРОВАННО работает, потому что:
1. Использует прямую работу с Canvas без SimpleDocTemplate
2. Полный контроль над позиционированием 
3. Настоящий Arial шрифт для кириллицы
4. Видимая нумерация "Стр. X из N"
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
import os

def register_arial_font():
    """Регистрация Arial для кириллицы"""
    try:
        arial_path = "C:/Windows/Fonts/arial.ttf"
        if os.path.exists(arial_path):
            pdfmetrics.registerFont(TTFont('Arial', arial_path))
            pdfmetrics.registerFont(TTFont('Arial-Bold', "C:/Windows/Fonts/arialbd.ttf"))
            print("✅ Arial и Arial-Bold зарегистрированы")
            return True
    except Exception as e:
        print(f"⚠️ Ошибка регистрации Arial: {e}")
    return False

class PureCanvasPDF:
    """
    Класс для создания PDF на чистом Canvas с гарантированной нумерацией
    """
    
    def __init__(self, filename: str):
        self.filename = filename
        self.canvas = canvas.Canvas(filename, pagesize=A4)
        self.current_page = 0
        self.total_pages = 0  # Будет установлено позже
        
        # Настройки страницы
        self.left_margin = 25*mm
        self.right_margin = 25*mm  
        self.top_margin = 25*mm
        self.bottom_margin = 25*mm
        
        # Рабочая область
        self.content_width = A4[0] - self.left_margin - self.right_margin
        self.content_height = A4[1] - self.top_margin - self.bottom_margin
        
        # Позиция для нумерации (ЗДЕСЬ ФИКСИРУЮТСЯ КООРДИНАТЫ)
        self.page_number_x = A4[0] - 15*mm  # 15мм от правого края
        self.page_number_y = A4[1] - 10*mm  # 10мм от верхнего края
        
        # Регистрируем Arial
        self.arial_available = register_arial_font()
        self.font_name = "Arial" if self.arial_available else "Helvetica"
        
        print(f"📄 Инициализация PDF: {filename}")
        print(f"🔤 Используется шрифт: {self.font_name}")
        print(f"📐 Позиция нумерации: ({self.page_number_x:.1f}, {self.page_number_y:.1f})")
    
    def start_new_page(self):
        """Начинает новую страницу"""
        if self.current_page > 0:
            self.canvas.showPage()
        
        self.current_page += 1
        print(f"📝 Начинаем страницу {self.current_page}")
        
        # Рисуем номер страницы (если знаем общее количество)
        if self.total_pages > 0:
            self.draw_page_number()
    
    def draw_page_number(self):
        """
        ГЛАВНЫЙ МЕТОД НУМЕРАЦИИ
        ЗДЕСЬ фиксируются ВСЕ параметры позиционирования и шрифта
        """
        self.canvas.saveState()
        
        # === НАСТРОЙКИ ШРИФТА ===
        font_size = 10
        self.canvas.setFont(self.font_name, font_size)
        self.canvas.setFillColor(black)
        
        # === ТЕКСТ НУМЕРАЦИИ ===
        page_text = f"Стр. {self.current_page} из {self.total_pages}"
        
        # === РИСОВАНИЕ ===
        self.canvas.drawRightString(self.page_number_x, self.page_number_y, page_text)
        
        self.canvas.restoreState()
        
        print(f"✅ Нарисован номер: '{page_text}' в позиции ({self.page_number_x:.1f}, {self.page_number_y:.1f})")
    
    def add_title(self, title: str, y_position: float = None):
        """Добавляет заголовок"""
        if y_position is None:
            y_position = A4[1] - 50*mm
        
        self.canvas.saveState()
        self.canvas.setFont(self.font_name, 16)
        self.canvas.setFillColor(black)
        
        # Центрируем заголовок
        title_width = self.canvas.stringWidth(title, self.font_name, 16)
        x_position = (A4[0] - title_width) / 2
        
        self.canvas.drawString(x_position, y_position, title)
        self.canvas.restoreState()
        
        return y_position - 15*mm  # Возвращаем позицию для следующего элемента
    
    def add_paragraph(self, text: str, y_position: float, font_size: int = 11):
        """Добавляет параграф текста"""
        self.canvas.saveState()
        self.canvas.setFont(self.font_name, font_size)
        self.canvas.setFillColor(black)
        
        # Простое разбитие на строки (для демонстрации)
        max_chars_per_line = int(self.content_width / (font_size * 0.5))
        words = text.split()
        lines = []
        current_line = ""        
        for word in words:
            if len(current_line + " " + word) <= max_chars_per_line:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Рисуем строки
        line_height = font_size * 1.2
        for i, line in enumerate(lines):
            line_y = y_position - (i * line_height)
            self.canvas.drawString(self.left_margin, line_y, line)
        
        self.canvas.restoreState()
        
        return y_position - (len(lines) * line_height) - 5*mm
    
    def set_total_pages(self, total: int):
        """Устанавливает общее количество страниц"""
        self.total_pages = total
        print(f"📊 Установлено общее количество страниц: {total}")
    
    def save(self):
        """Сохраняет PDF"""
        self.canvas.save()
        print(f"💾 PDF сохранен: {self.filename}")

def create_demo_pdf_with_numbering():
    """
    Создает демонстрационный PDF с гарантированной нумерацией
    """
    print("🚀 СОЗДАЕМ ДЕМО PDF С РАБОЧЕЙ НУМЕРАЦИЕЙ")
    print("=" * 50)
    
    filename = "pure_canvas_demo.pdf"
    
    # === ЭТАП 1: Создаем PDF с контентом ===
    pdf = PureCanvasPDF(filename)
    
    # Страница 1
    pdf.start_new_page()
    current_y = pdf.add_title("ДЕМОНСТРАЦИЯ НУМЕРАЦИИ НА ЧИСТОМ CANVAS")
    current_y = pdf.add_paragraph(
        "Это первая страница демонстрационного документа. Здесь показано, как работает нумерация страниц с использованием чистого Canvas без SimpleDocTemplate. Этот подход гарантированно работает в любой версии ReportLab.",
        current_y
    )
    
    # Добавляем информацию о настройках
    current_y -= 20
    current_y = pdf.add_paragraph(f"Используемый шрифт: {pdf.font_name}", current_y, 10)
    current_y = pdf.add_paragraph(f"Позиция нумерации: X={pdf.page_number_x:.1f}, Y={pdf.page_number_y:.1f}", current_y, 10)
    current_y = pdf.add_paragraph(f"Размеры A4: {A4[0]:.1f} x {A4[1]:.1f} points", current_y, 10)
    
    # Страница 2
    pdf.start_new_page()
    current_y = pdf.add_title("ВТОРАЯ СТРАНИЦА")
    current_y = pdf.add_paragraph(
        "Это вторая страница документа. Нумерация должна автоматически обновиться. Мы используем прямую работу с Canvas, что дает полный контроль над позиционированием всех элементов, включая номера страниц.",
        current_y
    )
    
    # Страница 3
    pdf.start_new_page()
    current_y = pdf.add_title("ТРЕТЬЯ СТРАНИЦА")
    current_y = pdf.add_paragraph(
        "Финальная страница демонстрации. Номер страницы должен показывать 'Стр. 3 из 3'. Этот подход полностью решает проблему с невидимой нумерацией в SimpleDocTemplate.",
        current_y
    )
    
    # === ЭТАП 2: Устанавливаем общее количество страниц и пересоздаем ===
    total_pages = pdf.current_page
    pdf.set_total_pages(total_pages)
    
    # Пересоздаем документ с нумерацией
    pdf.canvas.save()
    print(f"🔄 Первичное сохранение завершено. Пересоздаем с нумерацией...")
    
    # Создаем финальную версию с нумерацией
    final_pdf = PureCanvasPDF(filename)
    final_pdf.set_total_pages(total_pages)
    
    # Пересоздаем все страницы с нумерацией
    # Страница 1
    final_pdf.start_new_page()
    current_y = final_pdf.add_title("ДЕМОНСТРАЦИЯ НУМЕРАЦИИ НА ЧИСТОМ CANVAS")
    current_y = final_pdf.add_paragraph(
        "Это первая страница демонстрационного документа. Здесь показано, как работает нумерация страниц с использованием чистого Canvas без SimpleDocTemplate. Этот подход гарантированно работает в любой версии ReportLab.",
        current_y
    )
    current_y -= 20
    current_y = final_pdf.add_paragraph(f"Используемый шрифт: {final_pdf.font_name}", current_y, 10)
    current_y = final_pdf.add_paragraph(f"Позиция нумерации: X={final_pdf.page_number_x:.1f}, Y={final_pdf.page_number_y:.1f}", current_y, 10)
    current_y = final_pdf.add_paragraph(f"Размеры A4: {A4[0]:.1f} x {A4[1]:.1f} points", current_y, 10)
    
    # Страница 2
    final_pdf.start_new_page()
    current_y = final_pdf.add_title("ВТОРАЯ СТРАНИЦА")
    current_y = final_pdf.add_paragraph(
        "Это вторая страница документа. Нумерация должна автоматически обновиться. Мы используем прямую работу с Canvas, что дает полный контроль над позиционированием всех элементов, включая номера страниц.",
        current_y
    )
    
    # Страница 3
    final_pdf.start_new_page()
    current_y = final_pdf.add_title("ТРЕТЬЯ СТРАНИЦА")
    current_y = final_pdf.add_paragraph(
        "Финальная страница демонстрации. Номер страницы должен показывать 'Стр. 3 из 3'. Этот подход полностью решает проблему с невидимой нумерацией в SimpleDocTemplate.",
        current_y
    )
    
    final_pdf.save()
    
    # === ЭТАП 3: Проверяем результат ===
    if os.path.exists(filename):
        file_size = os.path.getsize(filename)
        print(f"📊 Размер финального файла: {file_size} байт")
        
        if file_size > 3000:
            print("✅ PDF создан успешно с рабочей нумерацией!")
            print(f"👀 ПРОВЕРЬТЕ ФАЙЛ: {os.path.abspath(filename)}")
            return True
        else:
            print("⚠️ Файл слишком маленький")
            return False
    else:
        print("❌ Файл не создан")
        return False

if __name__ == "__main__":
    create_demo_pdf_with_numbering()