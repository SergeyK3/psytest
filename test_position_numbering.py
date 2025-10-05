#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест позиций нумерации - создает PDF с нумерацией в разных местах
"""

from final_full_numbered_generator import FinalFullVolumeGenerator
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, blue, green, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

class MultiPositionCanvas(canvas.Canvas):
    """Canvas с нумерацией в РАЗНЫХ позициях для поиска видимой области"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for (page_num, page_state) in enumerate(self._saved_page_states):
            self.__dict__.update(page_state)
            self.draw_multiple_positions(page_num + 1, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_multiple_positions(self, page_num, total_pages):
        """Рисует нумерацию в РАЗНЫХ позициях с разными цветами"""
        self.saveState()
        
        # Регистрируем шрифт
        try:
            arial_path = "C:/Windows/Fonts/arial.ttf"
            if os.path.exists(arial_path):
                pdfmetrics.registerFont(TTFont('Arial-Multi', arial_path))
                font_name = "Arial-Multi"
            else:
                font_name = "Times-Roman"
        except:
            font_name = "Times-Roman"
        
        self.setFont(font_name, 12)
        text = f"Стр. {page_num} из {total_pages}"
        
        # ПОЗИЦИЯ 1: Правый верх (КРАСНЫЙ) - основная
        self.setFillColor(red)
        self.drawRightString(A4[0] - 25*mm, A4[1] - 15*mm, f"ПРАВО-ВЕРХ: {text}")
        
        # ПОЗИЦИЯ 2: Правый верх ближе к краю (СИНИЙ)
        self.setFillColor(blue)
        self.drawRightString(A4[0] - 10*mm, A4[1] - 10*mm, f"КРАЙ: {text}")
        
        # ПОЗИЦИЯ 3: Правый верх дальше от края (ЗЕЛЕНЫЙ)
        self.setFillColor(green)
        self.drawRightString(A4[0] - 40*mm, A4[1] - 20*mm, f"ДАЛЬШЕ: {text}")
        
        # ПОЗИЦИЯ 4: Центр верха (ЧЕРНЫЙ)
        self.setFillColor(black)
        self.drawCentredText(A4[0] / 2, A4[1] - 15*mm, f"ЦЕНТР-ВЕРХ: {text}")
        
        # ПОЗИЦИЯ 5: Правый низ (для сравнения)
        self.setFillColor(red)
        self.drawRightString(A4[0] - 25*mm, 20*mm, f"ПРАВО-НИЗ: {text}")
        
        self.restoreState()

def create_position_test():
    """Создает тест позиций нумерации"""
    
    filename = 'position_test.pdf'
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=25*mm,
        rightMargin=25*mm,
        topMargin=30*mm,  # Больше места для тестов
        bottomMargin=25*mm,
        canvasmaker=MultiPositionCanvas
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Заголовок как на изображении
    title_style = styles['Title']
    title_style.fontSize = 14
    title_style.alignment = 1
    
    story.append(Paragraph("КОМПЛЕКСНАЯ ОЦЕНКА КОМАНДНЫХ НАВЫКОВ", title_style))
    story.append(Spacer(1, 30))
    
    # Информационная таблица как на изображении  
    info_text = """
    Имя сотрудника: Тестовый Пользователь<br/>
    Дата тестирования: 2025-10-05<br/>
    Количество методик: 4 (PAEI, DISC, HEXACO, Soft Skills)
    """
    story.append(Paragraph(info_text, styles['Normal']))
    story.append(Spacer(1, 30))
    
    # Заголовок секции
    story.append(Paragraph("ОБЩЕЕ ЗАКЛЮЧЕНИЕ И РЕКОМЕНДАЦИИ", styles['Heading1']))
    story.append(Spacer(1, 20))
    
    # Основной текст как на изображении
    main_text = """
    На основе комплексного психологического тестирования сотрудника Тестовый
    Пользователь проведен анализ управленческого потенциала, личностных особенностей,
    поведенческих стилей и профессиональных компетенций. Результаты позволяют
    составить целостное представление о профессиональном профиле и потенциале
    развития.
    """
    story.append(Paragraph(main_text, styles['Normal']))
    
    # Строим документ
    doc.build(story)
    return filename

if __name__ == "__main__":
    try:
        result = create_position_test()
        print(f"✅ Тест позиций создан: {result}")
        print("🔍 Ищите ЦВЕТНУЮ нумерацию в разных местах:")
        print("   🔴 КРАСНЫЙ - правый верх (основная позиция)")
        print("   🔵 СИНИЙ - ближе к краю")
        print("   🟢 ЗЕЛЕНЫЙ - дальше от края")
        print("   ⚫ ЧЕРНЫЙ - центр верха")
        print("   🔴 КРАСНЫЙ внизу - для сравнения")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()