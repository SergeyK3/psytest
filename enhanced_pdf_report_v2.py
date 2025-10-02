#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенный модуль для создания PDF отчётов с детальными описани            if "Arial-Bold" in fonts_registered:
                DesignConfig.HEADER_FONT = "Arial-Bold"
                print("[INFO] Используется Arial-Bold для заголовков")
            elif "Times-Bold" in fonts_registered:
                DesignConfig.HEADER_FONT = "Times-Bold"
                print("[INFO] Используется Times-Bold для заголовков")
            else:
                DesignConfig.HEADER_FONT = "Times-Bold"
                print("[INFO] Используется встроенный Times-Bold для заголовков")ия 2.0 с расширенным контентом и правильной последовательностью тестов
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
from reportlab.platypus import PageBreak, KeepTogether, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import numpy as np

from src.psytest.charts import make_radar, make_bar_chart

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
    
    # Размеры графиков (в мм) - оптимизированы для баланса с текстом
    RADAR_SIZE = 100  # было 120, уменьшено для баланса с увеличенным текстом
    BAR_CHART_WIDTH = 160
    BAR_CHART_HEIGHT = 80  # было 60
    
    # Шрифты (используем встроенные Unicode шрифты)
    TITLE_FONT = "Times-Bold"
    BODY_FONT = "Times-Roman"
    SMALL_FONT = "Times-Roman"
    
    TITLE_SIZE = 14
    BODY_SIZE = 11  # было 10, увеличено для лучшей читаемости
    SMALL_SIZE = 9   # было 8


class EnhancedCharts:
    """Класс для создания улучшенных диаграмм"""
    
    @staticmethod
    def create_minimalist_radar(labels: List[str], values: List[float], 
                               title: str, out_path: Path) -> Path:
        """Создаёт минималистичную радарную диаграмму с автоматической нормализацией"""
        return make_radar(labels, values, out_path, title=title, 
                         normalize=True, normalize_method="adaptive")
    
    @staticmethod
    def create_minimalist_bar_chart(labels: List[str], values: List[float],
                                   title: str, out_path: Path) -> Path:
        """Создаёт минималистичную столбчатую диаграмму с автоматической нормализацией"""
        return make_bar_chart(labels, values, out_path, title=title, 
                             normalize=True, normalize_method="adaptive")


class EnhancedPDFReportV2:
    """Класс для создания улучшенных PDF отчётов версии 2.0"""
    
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
                        print(f"[OK] Зарегистрирован шрифт: {font_name}")
                    except Exception as e:
                        print(f"[WARN] Ошибка регистрации {font_name}: {e}")
            
            # Устанавливаем шрифты в зависимости от того, что удалось зарегистрировать
            if "Arial-Regular" in fonts_registered:
                DesignConfig.BODY_FONT = "Arial-Regular"
                DesignConfig.SMALL_FONT = "Arial-Regular"
                print("[INFO] Используется Arial для основного текста")
            else:
                DesignConfig.BODY_FONT = "Times-Roman"
                DesignConfig.SMALL_FONT = "Times-Roman"
                print("[INFO] Используется Times-Roman для основного текста")
            
            if "Arial-Bold" in fonts_registered:
                DesignConfig.TITLE_FONT = "Arial-Bold"
                print("[INFO] Используется Arial-Bold для заголовков")
            elif "Times-Bold" in fonts_registered:
                DesignConfig.TITLE_FONT = "Times-Bold"
                print("[INFO] Используется Times-Bold для заголовков")
            else:
                DesignConfig.TITLE_FONT = "Times-Bold"
                print("[INFO] Используется встроенный Times-Bold для заголовков")
                
        except Exception as e:
            print(f"[WARN] Ошибка настройки шрифтов: {e}")
            # В случае ошибки используем встроенные шрифты
            DesignConfig.TITLE_FONT = "Times-Bold"
            DesignConfig.BODY_FONT = "Times-Roman"
            DesignConfig.SMALL_FONT = "Times-Roman"
            print("[INFO] Используются встроенные шрифты Times")
    
    def _add_chart_to_story(self, story, chart_path: Path, width: int = None, height: int = None):
        """Добавляет диаграмму в документ с оптимизированными размерами"""
        if chart_path.exists():
            try:
                # Используем увеличенные размеры из конфигурации если не указаны явно
                if width is None:
                    width = DesignConfig.RADAR_SIZE
                if height is None:
                    height = DesignConfig.RADAR_SIZE
                    
                # Конвертируем размеры в миллиметры
                img = Image(str(chart_path), width=width*mm, height=height*mm)
                img.hAlign = 'CENTER'
                story.append(img)
                story.append(Spacer(1, 5*mm))
            except Exception as e:
                print(f"[WARN] Ошибка при добавлении диаграммы {chart_path}: {e}")
                # Добавляем плейсхолдер
                story.append(Paragraph(f"[Диаграмма: {chart_path.name}]", self._get_custom_styles()['Body']))
                story.append(Spacer(1, 5*mm))
    
    def generate_enhanced_report(self, 
                               participant_name: str,
                               test_date: str,
                               paei_scores: Dict[str, float],
                               disc_scores: Dict[str, float], 
                               hexaco_scores: Dict[str, float],
                               soft_skills_scores: Dict[str, float],
                               ai_interpretations: Dict[str, str],
                               out_path: Path) -> Path:
        """Генерирует улучшенный PDF отчёт с детальными описаниями"""
        
        # Создание PDF документа
        doc = SimpleDocTemplate(str(out_path), pagesize=A4,
                              rightMargin=DesignConfig.MARGIN*mm,
                              leftMargin=DesignConfig.MARGIN*mm,
                              topMargin=DesignConfig.MARGIN*mm,
                              bottomMargin=DesignConfig.MARGIN*mm)
        
        # Создание всех диаграмм (радарные для всех тестов)
        chart_paths = self._create_all_charts(paei_scores, disc_scores, hexaco_scores, soft_skills_scores)
        
        # Стили
        styles = self._get_custom_styles()
        story = []
        
        # === ЗАГОЛОВОК ДОКУМЕНТА ===
        story.append(Paragraph("ОЦЕНКА КОМАНДНЫХ НАВЫКОВ", styles['MainTitle']))
        story.append(Spacer(1, 8*mm))
        
        # === ИНФОРМАЦИЯ О ТЕСТИРУЕМОМ ===
        info_data = [
            ['Имя сотрудника:', participant_name],
            ['Дата тестирования:', test_date],
        ]
        
        info_table = Table(info_data, colWidths=[50*mm, 80*mm])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), DesignConfig.BODY_FONT, 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TEXTCOLOR', (0, 0), (0, -1), DesignConfig.PRIMARY_COLOR),
            ('FONTNAME', (0, 0), (0, -1), DesignConfig.TITLE_FONT),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 10*mm))
        
        # === ОБЩЕЕ ЗАКЛЮЧЕНИЕ И РЕКОМЕНДАЦИИ ===
        story.append(Paragraph("ОБЩЕЕ ЗАКЛЮЧЕНИЕ И РЕКОМЕНДАЦИИ", styles['SectionTitle']))
        story.append(Spacer(1, 5*mm))
        
        # Определяем доминирующие черты для заключения
        max_paei = max(paei_scores, key=paei_scores.get)
        max_disc = max(disc_scores, key=disc_scores.get)
        max_hexaco = max(hexaco_scores, key=hexaco_scores.get)
        max_soft = max(soft_skills_scores, key=soft_skills_scores.get)
        
        paei_names = {"P": "Производитель", "A": "Администратор", "E": "Предприниматель", "I": "Интегратор"}
        disc_names = {"D": "Доминирование", "I": "Влияние", "S": "Постоянство", "C": "Соответствие"}
        
        # Синтез результатов
        synthesis_text = f"""
        На основе комплексного психологического тестирования сотрудника <b>{participant_name}</b> 
        проведен анализ управленческого потенциала, личностных особенностей, поведенческих стилей 
        и профессиональных компетенций. Результаты позволяют составить целостное представление 
        о профессиональном профиле и потенциале развития.
        """
        story.append(Paragraph(synthesis_text, styles['Body']))
        story.append(Spacer(1, 5*mm))
        
        # Сводка по ключевым характеристикам
        story.append(Paragraph("<b>Ключевые характеристики профиля:</b>", styles['SubTitle']))
        
        key_traits = f"""
        • <b>Управленческий стиль по Адизесу:</b> Преобладает роль {paei_names.get(max_paei, max_paei)} ({paei_scores[max_paei]} баллов)<br/>
        • <b>Поведенческий тип DISC:</b> {disc_names.get(max_disc, max_disc)} ({disc_scores[max_disc]} баллов)<br/>
        • <b>Выраженная личностная черта HEXACO:</b> {max_hexaco} ({hexaco_scores[max_hexaco]} баллов)<br/>
        • <b>Наиболее развитый навык:</b> {max_soft} ({soft_skills_scores[max_soft]} баллов)
        """
        story.append(Paragraph(key_traits, styles['Body']))
        story.append(Spacer(1, 8*mm))
        
        # Профессиональные рекомендации
        story.append(Paragraph("<b>Рекомендации по профессиональному развитию:</b>", styles['SubTitle']))
        recommendations = f"""
        <b>1. Использование сильных сторон:</b><br/>
        • Делегировать задачи, соответствующие профилю {paei_names.get(max_paei, max_paei)}<br/>
        • Развивать {max_soft.lower()} через специализированные проекты<br/>
        • Использовать {disc_names.get(max_disc, max_disc).lower()} в командном взаимодействии<br/><br/>
        
        <b>2. Области для развития:</b><br/>
        • Работать над менее выраженными управленческими ролями<br/>
        • Развивать дополнительные soft skills для универсальности<br/>
        • Балансировать поведенческий стиль в зависимости от ситуации<br/><br/>
        
        <b>3. Карьерные перспективы:</b><br/>
        • Рассмотреть позиции, требующие качеств {paei_names.get(max_paei, max_paei).lower()}а<br/>
        • Планировать развитие с учетом личностного профиля HEXACO<br/>
        • Выстраивать команду с учетом комплементарных ролей по DISC
        """
        story.append(Paragraph(recommendations, styles['Body']))
        story.append(Spacer(1, 10*mm))
        
        # Методологическая справка
        story.append(Paragraph("<b>Использованные методики:</b>", styles['SubTitle']))
        methodology = """
        • <b>Тест Адизеса (PAEI)</b> - оценка управленческих ролей и стилей руководства<br/>
        • <b>Оценка Soft Skills</b> - анализ надпрофессиональных компетенций<br/>
        • <b>HEXACO</b> - современная модель личности (Lee & Ashton, 2004)<br/>
        • <b>DISC</b> - методика оценки поведенческих стилей (Marston, 1928)
        """
        story.append(Paragraph(methodology, styles['Body']))
        story.append(Spacer(1, 15*mm))
        
        # Переход к детальным разделам
        story.append(PageBreak())
        
        # === 1. ТЕСТ АДИЗЕСА (PAEI) ===
        story.append(Paragraph("1. ТЕСТ АДИЗЕСА (PAEI) - УПРАВЛЕНЧЕСКИЕ РОЛИ", styles['SectionTitle']))
        story.append(Spacer(1, 5*mm))
        
        # Расшифровка PAEI
        paei_description = """
        <b>Расшифровка PAEI:</b><br/>
        • <b>P (Producer - Производитель)</b> - ориентация на результат, выполнение задач, достижение целей<br/>
        • <b>A (Administrator - Администратор)</b> - организация процессов, контроль, систематизация работы<br/>
        • <b>E (Entrepreneur - Предприниматель)</b> - инновации, стратегическое мышление, креативность<br/>
        • <b>I (Integrator - Интегратор)</b> - командная работа, мотивация людей, создание единства
        """
        story.append(Paragraph(paei_description, styles['Body']))
        story.append(Spacer(1, 5*mm))
        
        # Результаты PAEI
        paei_results = f"<b>Результаты:</b> {self._format_scores(paei_scores)}"
        story.append(Paragraph(paei_results, styles['Body']))
        story.append(Spacer(1, 3*mm))
        
        # Встраиваем диаграмму PAEI
        if 'paei' in chart_paths:
            self._add_chart_to_story(story, chart_paths['paei'])
        
        # Интерпретация PAEI
        if 'paei' in ai_interpretations:
            story.append(Paragraph("<b>Интерпретация:</b>", styles['SubTitle']))
            story.append(Paragraph(ai_interpretations['paei'], styles['Body']))
        story.append(Spacer(1, 8*mm))
        
        # === 2. SOFT SKILLS - МЯГКИЕ НАВЫКИ ===
        story.append(Paragraph("2. SOFT SKILLS - ОЦЕНКА МЯГКИХ НАВЫКОВ", styles['SectionTitle']))
        story.append(Spacer(1, 5*mm))
        
        soft_description = """
        <b>Soft Skills</b> - это надпрофессиональные навыки, которые помогают решать жизненные и рабочие задачи 
        независимо от специальности. Включают коммуникативные способности, лидерские качества, креативность, 
        аналитическое мышление и адаптивность. Эти навыки определяют эффективность взаимодействия с людьми 
        и способность к профессиональному росту в любой сфере деятельности.
        """
        story.append(Paragraph(soft_description, styles['Body']))
        story.append(Spacer(1, 5*mm))
        
        # Результаты Soft Skills
        soft_results = f"<b>Результаты:</b> {self._format_scores(soft_skills_scores)}"
        story.append(Paragraph(soft_results, styles['Body']))
        story.append(Spacer(1, 3*mm))
        
        # AI интерпретация Soft Skills
        if 'soft_skills' in ai_interpretations:
            story.append(Spacer(1, 3*mm))
            story.append(Paragraph(ai_interpretations['soft_skills'], styles['Body']))
        
        # Встраиваем диаграмму Soft Skills
        if 'soft_skills' in chart_paths:
            self._add_chart_to_story(story, chart_paths['soft_skills'])
        
        story.append(Spacer(1, 8*mm))
        
        # === 3. ТЕСТ HEXACO - ЛИЧНОСТНЫЕ ЧЕРТЫ ===
        story.append(Paragraph("3. ТЕСТ HEXACO - МОДЕЛЬ ЛИЧНОСТИ", styles['SectionTitle']))
        story.append(Spacer(1, 5*mm))
        
        hexaco_description = """
        <b>HEXACO</b> - современная шестифакторная модель личности, включающая основные измерения:<br/>
        • <b>H (Honesty-Humility)</b> - честность, скромность, искренность в отношениях<br/>
        • <b>E (Emotionality)</b> - эмоциональность, чувствительность, эмпатия<br/>
        • <b>X (eXtraversion)</b> - экстраверсия, социальная активность, общительность<br/>
        • <b>A (Agreeableness)</b> - доброжелательность, сотрудничество, терпимость<br/>
        • <b>C (Conscientiousness)</b> - добросовестность, организованность, дисциплина<br/>
        • <b>O (Openness)</b> - открытость опыту, креативность, любознательность
        """
        story.append(Paragraph(hexaco_description, styles['Body']))
        story.append(Spacer(1, 5*mm))
        
        # Результаты HEXACO
        hexaco_results = f"<b>Результаты:</b> {self._format_scores(hexaco_scores)}"
        story.append(Paragraph(hexaco_results, styles['Body']))
        story.append(Spacer(1, 3*mm))
        
        # Встраиваем диаграмму HEXACO
        if 'hexaco' in chart_paths:
            self._add_chart_to_story(story, chart_paths['hexaco'])
        
        # Интерпретация HEXACO
        if 'hexaco' in ai_interpretations:
            story.append(Paragraph("<b>Интерпретация:</b>", styles['SubTitle']))
            story.append(Paragraph(ai_interpretations['hexaco'], styles['Body']))
        story.append(Spacer(1, 8*mm))
        
        # === 4. ТЕСТ DISC - ПОВЕДЕНЧЕСКИЕ СТИЛИ ===
        story.append(Paragraph("4. ТЕСТ DISC - МОДЕЛЬ ПОВЕДЕНИЯ", styles['SectionTitle']))
        story.append(Spacer(1, 5*mm))
        
        disc_description = """
        <b>DISC</b> - методика оценки поведенческих особенностей и стилей общения:<br/>
        • <b>D (Dominance)</b> - доминирование, прямота, решительность, ориентация на результат<br/>
        • <b>I (Influence)</b> - влияние, общительность, оптимизм, ориентация на людей<br/>
        • <b>S (Steadiness)</b> - постоянство, терпение, командная работа, стабильность<br/>
        • <b>C (Compliance)</b> - соответствие стандартам, аналитичность, точность, осторожность
        """
        story.append(Paragraph(disc_description, styles['Body']))
        story.append(Spacer(1, 5*mm))
        
        # Результаты DISC
        disc_results = f"<b>Результаты:</b> {self._format_scores(disc_scores)}"
        story.append(Paragraph(disc_results, styles['Body']))
        story.append(Spacer(1, 3*mm))
        
        # Встраиваем диаграмму DISC
        if 'disc' in chart_paths:
            self._add_chart_to_story(story, chart_paths['disc'])
        
        # Интерпретация DISC
        if 'disc' in ai_interpretations:
            story.append(Paragraph("<b>Интерпретация:</b>", styles['SubTitle']))
            story.append(Paragraph(ai_interpretations['disc'], styles['Body']))
        story.append(Spacer(1, 8*mm))
        
        # === ПЕРЕХОД НА НОВУЮ СТРАНИЦУ ===
        
        # Сборка PDF
        doc.build(story)
        return out_path
    
    def _create_all_charts(self, paei_scores: Dict, disc_scores: Dict, 
                         hexaco_scores: Dict, soft_skills_scores: Dict) -> Dict[str, Path]:
        """Создаёт все радарные диаграммы для отчета"""
        charts = {}
        
        # PAEI диаграмма (радарная) - данные уже в шкале 1-10
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
        
        # HEXACO диаграмма (радарная) - данные уже в шкале 1-10
        hexaco_labels = list(hexaco_scores.keys())
        hexaco_values = list(hexaco_scores.values())
        hexaco_path = self.template_dir / "hexaco_radar.png"
        EnhancedCharts.create_minimalist_radar(hexaco_labels, hexaco_values,
                                             "HEXACO", hexaco_path)
        charts['hexaco'] = hexaco_path
        
        # DISC диаграмма (радарная) - данные уже в шкале 1-10
        disc_labels = list(disc_scores.keys())
        disc_values = list(disc_scores.values())
        disc_path = self.template_dir / "disc_radar.png"
        EnhancedCharts.create_minimalist_radar(disc_labels, disc_values,
                                             "DISC", disc_path)
        charts['disc'] = disc_path
        
        return charts
    
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
        
        # Подзаголовок
        styles.add(ParagraphStyle(
            name='SubTitle',
            parent=styles['Heading3'],
            fontSize=11,
            fontName=DesignConfig.TITLE_FONT,
            textColor=DesignConfig.PRIMARY_COLOR,
            spaceBefore=4,
            spaceAfter=2,
        ))
        
        # Основной текст
        styles.add(ParagraphStyle(
            name='Body',
            parent=styles['Normal'],
            fontSize=DesignConfig.BODY_SIZE,
            fontName=DesignConfig.BODY_FONT,
            textColor=DesignConfig.TEXT_COLOR,
            spaceAfter=4,
            leading=14,  # было 12, увеличено для лучшей читаемости
        ))
        
        return styles
    
    def _format_scores(self, scores: Dict[str, float]) -> str:
        """Форматирует результаты в читаемую строку"""
        return ", ".join([f"{k}: {v}" for k, v in scores.items()])