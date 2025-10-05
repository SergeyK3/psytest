#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ТЕСТИРОВАНИЕ ПРОБЛЕМЫ С CANVASMAKER
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class TestCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        print("🔧 TestCanvas.__init__ ВЫЗВАН!")
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        print("🔧 TestCanvas.showPage ВЫЗВАН!")
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        print(f"🔧 TestCanvas.save ВЫЗВАН! Страниц: {len(self._saved_page_states)}")
        for i, page_state in enumerate(self._saved_page_states):
            print(f"🔧 Обрабатываем страницу {i+1}")
            self.__dict__.update(page_state)
            
            # Рисуем номер страницы
            self.setFont("Helvetica-Bold", 16)
            self.setFillColor('red')
            self.drawString(200, 400, f"TEST PAGE {i+1} of {len(self._saved_page_states)}")
            
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

def test_canvas_usage():
    print("🚀 Начинаем тест Canvas")
    
    # Создаем документ с кастомным Canvas
    doc = SimpleDocTemplate(
        "test_canvas_output.pdf",
        pagesize=A4,
        canvasmaker=TestCanvas
    )
    
    print("📄 SimpleDocTemplate создан с canvasmaker=TestCanvas")
    
    # Создаем контент
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Тест страницы 1", styles['Title']),
        Paragraph("Контент первой страницы" * 50, styles['Normal']),
        Paragraph("Тест страницы 2", styles['Title']),
        Paragraph("Контент второй страницы" * 50, styles['Normal']),
    ]
    
    print("📝 Контент создан")
    
    # Строим документ
    print("🔨 Начинаем doc.build()...")
    doc.build(story)
    print("✅ doc.build() завершен")

if __name__ == "__main__":
    test_canvas_usage()