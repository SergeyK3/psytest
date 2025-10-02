"""
Улучшенный модуль для создания PDF отчётов с минималистичным дизайном
Оптимизирован для печати, без титульной страницы
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus import PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import numpy as np

from .charts import make_radar, make_bar_chart

# Константы для минималистичного дизайна
class DesignConfig:
    """Конфигурация дизайна для печати"""
    
    # Цветовая палитра (оптимизирована для ч/б печати)
    PRIMARY_COLOR = Color(0.18, 0.25, 0.34)      # #2E4057 тёмно-синий
    ACCENT_COLOR = Color(0.29, 0.56, 0.72)       # #4A90B8 светло-синий  
    TEXT_COLOR = Color(0.17, 0.17, 0.17)         # #2C2C2C тёмно-серый
    LIGHT_GRAY = Color(0.9, 0.9, 0.9)            # #E6E6E6 светло-серый
    WHITE = Color(1, 1, 1)                        # #FFFFFF белый
    
    # Размеры (в мм)
    PAGE_WIDTH = 210
    PAGE_HEIGHT = 297
    MARGIN = 20
    
    # Размеры графиков (в мм) 
    RADAR_SIZE = 80
    BAR_CHART_WIDTH = 160
    BAR_CHART_HEIGHT = 60
    
    # Шрифты (используем встроенные Unicode шрифты)
    TITLE_FONT = "Times-Bold"
    BODY_FONT = "Times-Roman"
    SMALL_FONT = "Times-Roman"
    
    TITLE_SIZE = 14
    BODY_SIZE = 10
    SMALL_SIZE = 8


class EnhancedCharts:
    """Класс для создания улучшенных диаграмм"""
    
    @staticmethod
    def create_minimalist_radar(labels: List[str], values: List[float], 
                               title: str, out_path: Path) -> Path:
        """Создаёт минималистичную радарную диаграмму"""
        return make_radar(labels, values, out_path, title=title, max_value=10)
    
    @staticmethod
    def create_minimalist_bar_chart(labels: List[str], values: List[float],
                                   title: str, out_path: Path) -> Path:
        """Создаёт минималистичную столбчатую диаграмму"""
        return make_bar_chart(labels, values, out_path, title=title, max_value=10)


class EnhancedPDFReport:
    """Класс для создания улучшенных PDF отчётов"""
    
    def __init__(self, template_dir: Optional[Path] = None):
        self.template_dir = template_dir or Path.cwd() / "temp_charts"
        self.template_dir.mkdir(exist_ok=True)
        self._setup_fonts()
        
    def _setup_fonts(self):
        """Настраивает шрифты с поддержкой кириллицы"""
        try:
            # Пытаемся использовать системные шрифты Windows с кириллицей
            import os
            windows_fonts = "C:/Windows/Fonts/"
            
            # Список шрифтов в порядке предпочтения
            font_candidates = [
                ("arial.ttf", "Arial-Regular"),
                ("arialbd.ttf", "Arial-Bold"), 
                ("times.ttf", "Times-Regular"),
                ("timesbd.ttf", "Times-Bold"),
            ]
            
            fonts_registered = {}
            
            for font_file, font_name in font_candidates:
                font_path = os.path.join(windows_fonts, font_file)
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont(font_name, font_path))
                        fonts_registered[font_name] = True
                        print(f"✅ Зарегистрирован шрифт: {font_name}")
                    except Exception as e:
                        print(f"⚠️  Ошибка регистрации {font_name}: {e}")
            
            # Устанавливаем шрифты в зависимости от того, что удалось зарегистрировать
            if "Arial-Regular" in fonts_registered:
                DesignConfig.BODY_FONT = "Arial-Regular"
                DesignConfig.SMALL_FONT = "Arial-Regular"
                print("📝 Используется Arial для основного текста")
            else:
                DesignConfig.BODY_FONT = "Times-Roman"
                DesignConfig.SMALL_FONT = "Times-Roman"
                print("📝 Используется Times-Roman для основного текста")
            
            if "Arial-Bold" in fonts_registered:
                DesignConfig.TITLE_FONT = "Arial-Bold"
                print("📝 Используется Arial-Bold для заголовков")
            elif "Times-Bold" in fonts_registered:
                DesignConfig.TITLE_FONT = "Times-Bold"
                print("📝 Используется Times-Bold для заголовков")
            else:
                DesignConfig.TITLE_FONT = "Times-Bold"
                print("📝 Используется встроенный Times-Bold для заголовков")
                
        except Exception as e:
            print(f"⚠️  Ошибка настройки шрифтов: {e}")
            # В случае ошибки используем встроенные шрифты
            DesignConfig.TITLE_FONT = "Times-Bold"
            DesignConfig.BODY_FONT = "Times-Roman"
            DesignConfig.SMALL_FONT = "Times-Roman"
            print("📝 Используются встроенные шрифты Times")
        
    def create_visual_bar(self, value: float, max_value: float = 10, 
                         width: int = 100) -> str:
        """Создаёт текстовый индикатор для таблиц"""
        filled = int((value / max_value) * width) if max_value > 0 else 0
        empty = width - filled
        return '█' * (filled // 10) + '░' * (empty // 10)
    
    def generate_enhanced_report(self, 
                               participant_name: str,
                               test_date: str,
                               paei_scores: Dict[str, float],
                               disc_scores: Dict[str, float], 
                               hexaco_scores: Dict[str, float],
                               soft_skills_scores: Dict[str, float],
                               ai_interpretations: Dict[str, str],
                               out_path: Path) -> Path:
        """Генерирует улучшенный PDF отчёт"""
        
        # Создание PDF документа
        doc = SimpleDocTemplate(str(out_path), pagesize=A4,
                              rightMargin=DesignConfig.MARGIN*mm,
                              leftMargin=DesignConfig.MARGIN*mm,
                              topMargin=DesignConfig.MARGIN*mm,
                              bottomMargin=DesignConfig.MARGIN*mm)
        
        # Стили
        styles = self._get_custom_styles()
        story = []
        
        # === СТРАНИЦА 1: Основная информация ===
        
        # Шапка документа
        story.append(Paragraph("ПСИХОЛОГИЧЕСКИЙ ПОРТРЕТ СОТРУДНИКА", 
                              styles['MainTitle']))
        story.append(Spacer(1, 8*mm))
        
        # Информация о тестируемом
        info_data = [
            ['Имя сотрудника:', participant_name],
            ['Дата тестирования:', test_date],
            ['Статус:', 'Анализ завершён']
        ]
        
        info_table = Table(info_data, colWidths=[40*mm, 120*mm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), DesignConfig.BODY_FONT),
            ('FONTSIZE', (0, 0), (-1, -1), DesignConfig.BODY_SIZE),
            ('TEXTCOLOR', (0, 0), (0, -1), DesignConfig.PRIMARY_COLOR),
            ('TEXTCOLOR', (1, 0), (1, -1), DesignConfig.TEXT_COLOR),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 10*mm))
        
        # Создание всех диаграмм
        chart_paths = self._create_all_charts(paei_scores, disc_scores, hexaco_scores, soft_skills_scores)
        
        # Размещение радарных диаграмм (2 на первой странице)
        story.append(Paragraph("ОБЗОР РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ", styles['SectionTitle']))
        story.append(Spacer(1, 5*mm))
        
        # TODO: Добавить изображения радарных диаграмм
        # Пока добавляем плейсхолдеры
        story.append(Paragraph("• Диаграмма PAEI (Адизес): " + self._format_scores(paei_scores), 
                              styles['Body']))
        story.append(Paragraph("• Диаграмма DISC: " + self._format_scores(disc_scores), 
                              styles['Body']))
        story.append(Spacer(1, 5*mm))
        
        # Краткие выводы
        story.append(Paragraph("КРАТКИЕ ВЫВОДЫ", styles['SectionTitle']))
        story.append(Spacer(1, 3*mm))
        
        if 'paei' in ai_interpretations:
            brief_paei = ai_interpretations['paei'][:200] + "..."
            story.append(Paragraph(f"<b>По Адизесу:</b> {brief_paei}", styles['Body']))
        
        # Переход на вторую страницу
        story.append(PageBreak())
        
        # === СТРАНИЦА 2: Детальный анализ ===
        
        story.append(Paragraph("ДЕТАЛЬНЫЙ АНАЛИЗ РЕЗУЛЬТАТОВ", styles['MainTitle']))
        story.append(Spacer(1, 8*mm))
        
        # Диаграмма HEXACO
        story.append(Paragraph("ТЕСТ HEXACO", styles['SectionTitle']))
        story.append(Paragraph(self._format_scores(hexaco_scores), styles['Body']))
        story.append(Spacer(1, 5*mm))
        
        # Столбчатая диаграмма Soft Skills
        story.append(Paragraph("SOFT SKILLS", styles['SectionTitle']))
        soft_skills_table = self._create_skills_table(soft_skills_scores, styles)
        story.append(soft_skills_table)
        story.append(Spacer(1, 8*mm))
        
        # AI интерпретации
        story.append(Paragraph("РЕКОМЕНДАЦИИ И ВЫВОДЫ", styles['SectionTitle']))
        story.append(Spacer(1, 3*mm))
        
        for test_name, interpretation in ai_interpretations.items():
            if interpretation:
                story.append(Paragraph(interpretation, styles['Body']))
                story.append(Spacer(1, 5*mm))
        
        # Футер с информацией об AI
        story.append(Spacer(1, 10*mm))
        story.append(Paragraph("🤖 Интерпретации сгенерированы с помощью OpenAI GPT-3.5", 
                              styles['Footer']))
        story.append(Paragraph("Powered by OpenAI (https://openai.com)", 
                              styles['Footer']))
        
        # Генерация PDF
        doc.build(story)
        
        return out_path
    
    def _get_custom_styles(self):
        """Создаёт пользовательские стили"""
        styles = getSampleStyleSheet()
        
        # Основной заголовок
        styles.add(ParagraphStyle(
            name='MainTitle',
            parent=styles['Title'],
            fontSize=DesignConfig.TITLE_SIZE,
            fontName=DesignConfig.TITLE_FONT,
            textColor=DesignConfig.PRIMARY_COLOR,
            alignment=1,  # CENTER
            spaceAfter=6,
        ))
        
        # Заголовок секции
        styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=styles['Heading2'],
            fontSize=12,
            fontName=DesignConfig.TITLE_FONT,
            textColor=DesignConfig.PRIMARY_COLOR,
            spaceBefore=6,
            spaceAfter=3,
        ))
        
        # Основной текст
        styles.add(ParagraphStyle(
            name='Body',
            parent=styles['Normal'],
            fontSize=DesignConfig.BODY_SIZE,
            fontName=DesignConfig.BODY_FONT,
            textColor=DesignConfig.TEXT_COLOR,
            leading=12,
        ))
        
        # Футер
        styles.add(ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            fontSize=DesignConfig.SMALL_SIZE,
            fontName=DesignConfig.SMALL_FONT,
            textColor=DesignConfig.ACCENT_COLOR,
            alignment=1,  # CENTER
        ))
        
        return styles
    
    def _create_all_charts(self, paei_scores: Dict, disc_scores: Dict, 
                         hexaco_scores: Dict, soft_skills_scores: Dict) -> Dict[str, Path]:
        """Создаёт все диаграммы для отчета"""
        charts = {}
        
        # PAEI диаграмма (радарная)
        paei_labels = list(paei_scores.keys())
        paei_values = list(paei_scores.values())
        paei_path = self.template_dir / "paei_radar.png"
        EnhancedCharts.create_minimalist_radar(paei_labels, paei_values, 
                                             "PAEI (Адизес)", paei_path)
        charts['paei'] = paei_path
        
        # Soft Skills диаграмма (радарная)
        soft_labels = list(soft_skills_scores.keys())
        soft_values = list(soft_skills_scores.values())
        soft_radar_path = self.template_dir / "soft_skills_radar.png"
        EnhancedCharts.create_minimalist_radar(soft_labels, soft_values,
                                             "Soft Skills", soft_radar_path)
        charts['soft_skills'] = soft_radar_path
        
        # HEXACO диаграмма (радарная)
        hexaco_labels = list(hexaco_scores.keys())
        hexaco_values = list(hexaco_scores.values())
        hexaco_path = self.template_dir / "hexaco_radar.png"
        EnhancedCharts.create_minimalist_radar(hexaco_labels, hexaco_values,
                                             "HEXACO", hexaco_path)
        charts['hexaco'] = hexaco_path
        
        # DISC диаграмма (радарная)  
        disc_labels = list(disc_scores.keys())
        disc_values = list(disc_scores.values())
        disc_path = self.template_dir / "disc_radar.png"
        EnhancedCharts.create_minimalist_radar(disc_labels, disc_values,
                                             "DISC", disc_path)
        charts['disc'] = disc_path
        
        return charts
    
    def _create_skills_table(self, soft_skills: Dict[str, float], styles) -> Table:
        """Создаёт таблицу с визуальными индикаторами"""
        
        data = [['Навык', 'Балл', 'Уровень', 'Индикатор']]
        
        for skill, score in soft_skills.items():
            level = self._get_level_name(score)
            indicator = self.create_visual_bar(score)
            data.append([skill, f"{score}/10", level, indicator])
        
        table = Table(data, colWidths=[50*mm, 20*mm, 30*mm, 50*mm])
        table.setStyle(TableStyle([
            # Заголовок
            ('BACKGROUND', (0, 0), (-1, 0), DesignConfig.LIGHT_GRAY),
            ('TEXTCOLOR', (0, 0), (-1, 0), DesignConfig.PRIMARY_COLOR),
            ('FONTNAME', (0, 0), (-1, 0), DesignConfig.TITLE_FONT),
            ('FONTSIZE', (0, 0), (-1, 0), DesignConfig.BODY_SIZE),
            
            # Данные
            ('FONTNAME', (0, 1), (-1, -1), DesignConfig.BODY_FONT),
            ('FONTSIZE', (0, 1), (-1, -1), DesignConfig.BODY_SIZE),
            ('TEXTCOLOR', (0, 1), (-1, -1), DesignConfig.TEXT_COLOR),
            
            # Границы
            ('GRID', (0, 0), (-1, -1), 0.5, DesignConfig.TEXT_COLOR),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        return table
    
    def _format_scores(self, scores: Dict[str, float]) -> str:
        """Форматирует баллы для отображения"""
        return ", ".join([f"{k}: {v}" for k, v in scores.items()])
    
    def _get_level_name(self, score: float) -> str:
        """Возвращает название уровня по баллам"""
        if score >= 8:
            return "Высокий"
        elif score >= 5:
            return "Средний"
        else:
            return "Низкий"