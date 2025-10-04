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
import os
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
from scale_normalizer import ScaleNormalizer

# Google Drive интеграция (опционально)
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False

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
    """Класс для создания улучшенных диаграмм с правильными максимальными значениями"""
    
    @staticmethod
    def create_minimalist_radar(labels: List[str], values: List[float], 
                               title: str, out_path: Path, max_value: float = None) -> Path:
        """Создаёт минималистичную радарную диаграмму без нормализации"""
        # Используем переданное максимальное значение или автоматически определяем
        if max_value is None:
            max_value = max(values) * 1.1  # Добавляем 10% отступ
        return make_radar(labels, values, out_path, title=title, 
                         normalize=False, max_value=int(max_value))
    
    @staticmethod
    def create_minimalist_bar_chart(labels: List[str], values: List[float],
                                   title: str, out_path: Path, max_value: float = None) -> Path:
        """Создаёт минималистичную столбчатую диаграмму без нормализации"""
        # Используем переданное максимальное значение или автоматически определяем
        if max_value is None:
            max_value = max(values) * 1.1  # Добавляем 10% отступ
        return make_bar_chart(labels, values, out_path, title=title, 
                             normalize=False, max_value=int(max_value))
    
    @staticmethod
    def create_pie_chart(labels: List[str], values: List[float],
                        title: str, out_path: Path) -> Path:
        """Создаёт круговую диаграмму без нормализации"""
        from src.psytest.charts import make_pie_chart
        return make_pie_chart(labels, values, out_path, title=title)


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
        
        # Встраиваем диаграмму PAEI (комбинированная)
        if 'paei' in chart_paths:
            # Используем увеличенную ширину для комбинированной диаграммы
            self._add_chart_to_story(story, chart_paths['paei'], width=180, height=90)
        
        # Детальное описание PAEI на основе промптов
        detailed_paei = self._generate_detailed_test_description("PAEI", paei_scores)
        story.append(Paragraph(detailed_paei, styles['Body']))
        story.append(Spacer(1, 3*mm))
        
        # Интерпретация PAEI (ИИ)
        if 'paei' in ai_interpretations:
            story.append(Paragraph("<b>Дополнительная интерпретация ИИ:</b>", styles['SubTitle']))
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
        
        # Встраиваем диаграмму Soft Skills
        if 'soft_skills' in chart_paths:
            self._add_chart_to_story(story, chart_paths['soft_skills'])
        
        # Детальное описание Soft Skills на основе промптов
        detailed_soft = self._generate_detailed_test_description("SOFT_SKILLS", soft_skills_scores)
        story.append(Paragraph(detailed_soft, styles['Body']))
        story.append(Spacer(1, 3*mm))

        # AI интерпретация Soft Skills
        if 'soft_skills' in ai_interpretations:
            story.append(Paragraph("<b>Дополнительная интерпретация ИИ:</b>", styles['SubTitle']))
            story.append(Paragraph(ai_interpretations['soft_skills'], styles['Body']))

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
        
        # Детальное описание HEXACO на основе промптов
        detailed_hexaco = self._generate_detailed_test_description("HEXACO", hexaco_scores)
        story.append(Paragraph(detailed_hexaco, styles['Body']))
        story.append(Spacer(1, 3*mm))
        
        # Интерпретация HEXACO (ИИ)
        if 'hexaco' in ai_interpretations:
            story.append(Paragraph("<b>Дополнительная интерпретация ИИ:</b>", styles['SubTitle']))
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
        
        # Детальное описание DISC на основе промптов
        detailed_disc = self._generate_detailed_test_description("DISC", disc_scores)
        story.append(Paragraph(detailed_disc, styles['Body']))
        story.append(Spacer(1, 3*mm))
        
        # Интерпретация DISC (ИИ)
        if 'disc' in ai_interpretations:
            story.append(Paragraph("<b>Дополнительная интерпретация ИИ:</b>", styles['SubTitle']))
            story.append(Paragraph(ai_interpretations['disc'], styles['Body']))
        story.append(Spacer(1, 8*mm))
        
        # === ОБЩЕЕ ЗАКЛЮЧЕНИЕ ===
        if 'general' in ai_interpretations:
            story.append(PageBreak())
            story.append(Paragraph("ОБЩИЕ ВЫВОДЫ И РЕКОМЕНДАЦИИ", styles['SectionTitle']))
            story.append(Spacer(1, 4*mm))
            story.append(Paragraph(ai_interpretations['general'], styles['Body']))
            story.append(Spacer(1, 8*mm))
        
        # === ПЕРЕХОД НА НОВУЮ СТРАНИЦУ ===
        
        # Сборка PDF
        doc.build(story)
        return out_path
    
    def _create_all_charts(self, paei_scores: Dict, disc_scores: Dict, 
                         hexaco_scores: Dict, soft_skills_scores: Dict) -> Dict[str, Path]:
        """Создаёт все радарные диаграммы для отчета"""
        charts = {}
        
        # PAEI диаграммы (столбиковая и пироговая) - шкала 0-5
        paei_labels = list(paei_scores.keys())
        paei_values = list(paei_scores.values())
        
        # Столбиковая диаграмма PAEI
        paei_bar_path = self.template_dir / "paei_bar.png"
        EnhancedCharts.create_minimalist_bar_chart(paei_labels, paei_values, 
                                                 "PAEI (Адизес) - Столбиковая", paei_bar_path, 
                                                 max_value=ScaleNormalizer.get_max_scale("PAEI"))
        charts['paei_bar'] = paei_bar_path
        
        # Пироговая диаграмма PAEI
        paei_pie_path = self.template_dir / "paei_pie.png"
        EnhancedCharts.create_pie_chart(paei_labels, paei_values,
                                       "PAEI (Адизес) - Пропорции", paei_pie_path)
        charts['paei_pie'] = paei_pie_path
        
        # Создаем комбинированную диаграмму PAEI (две диаграммы рядом)
        paei_combined_path = self.template_dir / "paei_combined.png"
        self._create_paei_combined_chart(paei_bar_path, paei_pie_path, paei_combined_path, paei_scores)
        charts['paei'] = paei_combined_path
        
        # Soft Skills диаграмма (радарная) - шкала 1-10
        soft_labels = list(soft_skills_scores.keys())
        soft_values = list(soft_skills_scores.values())
        soft_radar_path = self.template_dir / "soft_skills_radar.png"
        EnhancedCharts.create_minimalist_radar(soft_labels, soft_values,
                                             "Soft Skills", soft_radar_path,
                                             max_value=ScaleNormalizer.get_max_scale("SOFT_SKILLS"))
        charts['soft_skills'] = soft_radar_path
        
        # HEXACO диаграмма (радарная) - шкала 1-5
        hexaco_labels = list(hexaco_scores.keys())
        hexaco_values = list(hexaco_scores.values())
        hexaco_path = self.template_dir / "hexaco_radar.png"
        EnhancedCharts.create_minimalist_radar(hexaco_labels, hexaco_values,
                                             "HEXACO", hexaco_path,
                                             max_value=ScaleNormalizer.get_max_scale("HEXACO"))
        charts['hexaco'] = hexaco_path
        
        # DISC диаграмма (круговая) - без нормализации, показываем сырые баллы
        disc_labels = list(disc_scores.keys())
        disc_values = list(disc_scores.values())
        disc_path = self.template_dir / "disc_pie.png"
        EnhancedCharts.create_pie_chart(disc_labels, disc_values,
                                       "DISC", disc_path)
        charts['disc'] = disc_path
        
        return charts
    
    def _create_paei_combined_chart(self, bar_chart_path: Path, pie_chart_path: Path, 
                                   output_path: Path, paei_scores: Dict[str, float]) -> Path:
        """Создает комбинированную диаграмму PAEI (столбиковая + пироговая)"""
        
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        from PIL import Image
        
        try:
            # Создаем фигуру с двумя подграфиками
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
            
            # Настройки для PAEI
            paei_labels = list(paei_scores.keys())
            paei_values = list(paei_scores.values())
            paei_full_names = {
                "P": "Производитель", 
                "A": "Администратор", 
                "E": "Предприниматель", 
                "I": "Интегратор"
            }
            
            # Цвета для диаграмм
            colors = ['#2E4057', '#4A90B8', '#7BB3D3', '#A8CCE6']
            
            # === ЛЕВАЯ ДИАГРАММА: СТОЛБИКОВАЯ ===
            ax1.bar(range(len(paei_labels)), paei_values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
            ax1.set_xlabel('Типы управления по Адизесу', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Количество баллов', fontsize=12, fontweight='bold')
            ax1.set_title('PAEI - Уровни по типам', fontsize=14, fontweight='bold', pad=20)
            ax1.set_xticks(range(len(paei_labels)))
            ax1.set_xticklabels([f"{label}\n({paei_full_names[label]})" for label in paei_labels], 
                               fontsize=10, ha='center')
            ax1.set_ylim(0, 5)
            ax1.grid(True, alpha=0.3, axis='y')
            
            # Добавляем значения на столбцы
            for i, v in enumerate(paei_values):
                ax1.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold', fontsize=11)
            
            # === ПРАВАЯ ДИАГРАММА: ПИРОГОВАЯ ===
            # Только для ненулевых значений
            non_zero_data = [(label, value, paei_full_names[label]) for label, value in zip(paei_labels, paei_values) if value > 0]
            
            if non_zero_data:
                pie_labels = [f"{full_name}\n{label}: {value}" for label, value, full_name in non_zero_data]
                pie_values = [value for label, value, full_name in non_zero_data]
                pie_colors = [colors[paei_labels.index(label)] for label, value, full_name in non_zero_data]
                
                # Создаем пироговую диаграмму с процентами
                wedges, texts, autotexts = ax2.pie(pie_values, labels=pie_labels, colors=pie_colors, 
                                                 autopct='%1.1f%%', startangle=90, 
                                                 textprops={'fontsize': 10})
                
                # Улучшаем внешний вид текста
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(11)
                
                ax2.set_title('PAEI - Пропорции баллов', fontsize=14, fontweight='bold', pad=20)
            else:
                # Если все значения нулевые
                ax2.text(0.5, 0.5, 'Нет данных для\nотображения', ha='center', va='center', 
                        transform=ax2.transAxes, fontsize=12, fontweight='bold')
                ax2.set_title('PAEI - Пропорции баллов', fontsize=14, fontweight='bold', pad=20)
            
            # Общие настройки
            plt.tight_layout(pad=3.0)
            
            # Сохраняем комбинированную диаграмму
            plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
            plt.close()
            
            print(f"✅ Создана комбинированная диаграмма PAEI: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Ошибка создания комбинированной диаграммы PAEI: {e}")
            # В случае ошибки возвращаем простую столбиковую диаграмму
            return bar_chart_path
    
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
    
    def _init_google_drive(self) -> Optional[object]:
        """Инициализация Google Drive API с OAuth"""
        if not GOOGLE_DRIVE_AVAILABLE:
            return None
        
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            
            SCOPES = ['https://www.googleapis.com/auth/drive.file']
            
            creds = None
            token_file = 'token.json'
            credentials_file = 'oauth_credentials.json'
            
            # Загружаем существующие токены
            if os.path.exists(token_file):
                creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            
            # Если нет валидных токенов, запускаем OAuth flow
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(credentials_file):
                        print(f"🔑 Файл {credentials_file} не найден - Google Drive отключен")
                        return None
                        
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Сохраняем токены для будущего использования
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
            
            service = build('drive', 'v3', credentials=creds)
            print("✅ Google Drive API инициализирован (OAuth)")
            return service
            
        except Exception as e:
            print(f"❌ Ошибка инициализации Google Drive: {e}")
            return None
    
    def _upload_to_google_drive(self, file_path: Path, user_name: str = "User") -> Optional[str]:
        """Загружает PDF отчет в Google Drive"""
        service = self._init_google_drive()
        if not service:
            return None
        
        try:
            # Создаем структуру папок
            from datetime import datetime
            
            # Корневая папка
            root_folder_name = "PsychTest Reports"
            root_query = f"name='{root_folder_name}' and mimeType='application/vnd.google-apps.folder'"
            root_results = service.files().list(q=root_query).execute()
            
            if root_results.get('files'):
                root_folder_id = root_results['files'][0]['id']
            else:
                root_metadata = {
                    'name': root_folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                root_folder = service.files().create(body=root_metadata).execute()
                root_folder_id = root_folder['id']
            
            # Папка года
            year = str(datetime.now().year)
            year_query = f"name='{year}' and mimeType='application/vnd.google-apps.folder' and '{root_folder_id}' in parents"
            year_results = service.files().list(q=year_query).execute()
            
            if year_results.get('files'):
                year_folder_id = year_results['files'][0]['id']
            else:
                year_metadata = {
                    'name': year,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [root_folder_id]
                }
                year_folder = service.files().create(body=year_metadata).execute()
                year_folder_id = year_folder['id']
            
            # Папка месяца
            month = datetime.now().strftime("%m-%B")
            month_query = f"name='{month}' and mimeType='application/vnd.google-apps.folder' and '{year_folder_id}' in parents"
            month_results = service.files().list(q=month_query).execute()
            
            if month_results.get('files'):
                month_folder_id = month_results['files'][0]['id']
            else:
                month_metadata = {
                    'name': month,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [year_folder_id]
                }
                month_folder = service.files().create(body=month_metadata).execute()
                month_folder_id = month_folder['id']
            
            # Загружаем файл
            file_metadata = {
                'name': file_path.name,
                'parents': [month_folder_id]
            }
            
            media = MediaFileUpload(str(file_path), mimetype='application/pdf')
            file_obj = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            # Делаем файл публично доступным
            try:
                permission = {
                    'type': 'anyone',
                    'role': 'reader'
                }
                service.permissions().create(
                    fileId=file_obj['id'],
                    body=permission
                ).execute()
            except:
                pass  # Игнорируем ошибки прав доступа
            
            link = file_obj.get('webViewLink')
            print(f"✅ PDF загружен в Google Drive: {link}")
            return link
            
        except Exception as e:
            print(f"❌ Ошибка загрузки в Google Drive: {e}")
            return None
    
    def generate_enhanced_report_with_gdrive(self, 
                                           participant_name: str,
                                           test_date: str,
                                           paei_scores: Dict[str, float],
                                           disc_scores: Dict[str, float], 
                                           hexaco_scores: Dict[str, float],
                                           soft_skills_scores: Dict[str, float],
                                           ai_interpretations: Dict[str, str],
                                           out_path: Path,
                                           upload_to_gdrive: bool = True) -> Tuple[Path, Optional[str]]:
        """
        Генерирует PDF отчёт и опционально загружает в Google Drive
        
        Returns:
            Tuple[Path, Optional[str]]: путь к файлу и ссылка на Google Drive (если загружен)
        """
        # Генерируем обычный отчет
        pdf_path = self.generate_enhanced_report(
            participant_name, test_date, paei_scores, disc_scores,
            hexaco_scores, soft_skills_scores, ai_interpretations, out_path
        )
        
        # Загружаем в Google Drive если нужно
        gdrive_link = None
        if upload_to_gdrive:
            gdrive_link = self._upload_to_google_drive(pdf_path, participant_name)
        
        return pdf_path, gdrive_link
    
    def _generate_detailed_test_description(self, test_type: str, scores: Dict[str, float]) -> str:
        """Генерирует детальное описание результатов тестирования на основе промптов _res.txt"""
        
        if test_type == "PAEI":
            return self._generate_paei_detailed_description(scores)
        elif test_type == "DISC":
            return self._generate_disc_detailed_description(scores)
        elif test_type == "HEXACO":
            return self._generate_hexaco_detailed_description(scores)
        elif test_type == "SOFT_SKILLS":
            return self._generate_soft_skills_detailed_description(scores)
        else:
            return f"Детальное описание для {test_type} пока не доступно."
    
    def _generate_paei_detailed_description(self, scores: Dict[str, float]) -> str:
        """Генерирует детальное описание PAEI на основе реальных баллов"""
        
        # Определяем доминирующий стиль
        max_style = max(scores, key=scores.get)
        max_score = scores[max_style]
        
        # Переводим сокращения в полные названия
        style_names = {
            "P": "Производитель", "A": "Администратор", 
            "E": "Предприниматель", "I": "Интегратор"
        }
        
        # Формируем базовую статистику
        stats = f"Производитель - {scores.get('P', 0)}<br/>"
        stats += f"Администратор - {scores.get('A', 0)}<br/>"
        stats += f"Предприниматель - {scores.get('E', 0)}<br/>"
        stats += f"Интегратор - {scores.get('I', 0)}<br/><br/>"
        
        description = f"<b>Результаты тестирования по методике Адизеса (PAEI):</b><br/><br/>{stats}"
        
        # Анализ доминирующего стиля
        description += f"<b>Основной стиль поведения — {max_style} ({style_names[max_style]}):</b><br/>"
        
        if max_style == "P":
            description += (
                f"• <b>Производитель (P)</b> преобладает в результатах тестирования ({max_score} баллов), "
                "что свидетельствует о сильной ориентации на результат и выполнение конкретных задач.<br/>"
                "• Человек склонен к быстрым действиям, достижению поставленных целей и завершению проектов.<br/>"
                "• Вероятно, он чувствует себя комфортно в ситуациях, требующих оперативности и эффективности.<br/>"
                "• Этот стиль предполагает практичность, целеустремленность и фокус на измеримых результатах.<br/><br/>"
            )
        elif max_style == "A":
            description += (
                f"• <b>Администратор (A)</b> доминирует в профиле ({max_score} баллов), "
                "что указывает на склонность к организации процессов, контролю и систематизации работы.<br/>"
                "• Человек предпочитает структурированный подход, планирование и следование установленным процедурам.<br/>"
                "• Вероятно, он обладает хорошими навыками анализа, внимателен к деталям и стремится к порядку.<br/>"
                "• Этот стиль характеризуется дисциплинированностью, надежностью и методичностью.<br/><br/>"
            )
        elif max_style == "E":
            description += (
                f"• <b>Предприниматель (E)</b> выделяется как основной стиль ({max_score} баллов), "
                "что свидетельствует о сильной ориентации на инновации, изменения и долгосрочное видение.<br/>"
                "• Человек склонен к поиску новых возможностей, созданию стратегий и внедрению изменений.<br/>"
                "• Вероятно, он комфортно чувствует себя в условиях неопределенности и готов идти на обоснованный риск.<br/>"
                "• Этот стиль предполагает креативность, стратегическое мышление и стремление к трансформации.<br/><br/>"
            )
        elif max_style == "I":
            description += (
                f"• <b>Интегратор (I)</b> преобладает в результатах ({max_score} баллов), "
                "что указывает на сильную ориентацию на командную работу и взаимодействие с людьми.<br/>"
                "• Человек склонен к созданию гармонии в коллективе, решению межличностных вопросов и объединению усилий.<br/>"
                "• Вероятно, он чувствует себя комфортно в роли медиатора и заботится о моральном климате команды.<br/>"
                "• Этот стиль характеризуется эмпатией, дипломатичностью и способностью мотивировать людей.<br/><br/>"
            )
        
        # Анализ других стилей
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        description += "<b>Дополнительные характеристики профиля:</b><br/>"
        for style, score in sorted_scores[1:]:
            if score >= 3:
                description += f"• <b>{style_names[style]} ({style})</b> проявляется на уровне {score} баллов, дополняя основной стиль.<br/>"
            elif score <= 2:
                description += f"• <b>{style_names[style]} ({style})</b> выражен слабо ({score} баллов), что может указывать на зону развития.<br/>"
        
        description += "<br/><b>Рекомендации по развитию:</b><br/>"
        description += f"• Использовать сильные качества {style_names[max_style].lower()}а для достижения профессиональных целей.<br/>"
        description += "• Развивать менее выраженные управленческие роли для повышения универсальности.<br/>"
        description += "• Учитывать свой стиль при выборе задач и формировании команды.<br/>"
        
        return description
    
    def _generate_disc_detailed_description(self, scores: Dict[str, float]) -> str:
        """Генерирует детальное описание DISC на основе реальных баллов"""
        
        # Переводим сокращения в полные названия
        disc_names = {
            "D": "Доминирование", "I": "Влияние", 
            "S": "Постоянство", "C": "Соответствие"
        }
        
        # Формируем статистику
        stats = ""
        for key in ["D", "I", "S", "C"]:
            score = scores.get(key, 0)
            level = "ярко выраженный" if score >= 8 else "средний" if score >= 5 else "слабый"
            stats += f"• <b>{disc_names[key]} ({key})</b>: {score} баллов ({level} уровень)<br/>"
        
        description = f"<b>Результаты тестирования DISC:</b><br/><br/>{stats}<br/>"
        
        # Определяем доминирующий тип
        max_style = max(scores, key=scores.get)
        max_score = scores[max_style]
        
        description += f"<b>Доминирующий поведенческий тип: {disc_names[max_style]} ({max_style})</b><br/>"
        
        if max_style == "D":
            description += (
                f"Высокий уровень доминирования ({max_score} баллов) указывает на решительность, прямоту и стремление к лидерству. "
                "Человек уверен в себе, предпочитает брать ответственность за принятие решений и действует независимо. "
                "Ориентирован на достижение результатов, может проявлять настойчивость и готовность к вызовам.<br/><br/>"
            )
        elif max_style == "I":
            description += (
                f"Преобладание влияния ({max_score} баллов) характеризует общительную, оптимистичную личность. "
                "Человек легко устанавливает контакты, вдохновляет людей и создает позитивную атмосферу. "
                "Обладает природной харизмой, предпочитает работу в команде и ориентирован на людей.<br/><br/>"
            )
        elif max_style == "S":
            description += (
                f"Высокое постоянство ({max_score} баллов) указывает на терпеливость, надежность и стремление к стабильности. "
                "Человек предпочитает предсказуемую среду, хорошо работает в команде и проявляет лояльность. "
                "Ценит гармоничные отношения и избегает конфликтных ситуаций.<br/><br/>"
            )
        elif max_style == "C":
            description += (
                f"Высокое соответствие стандартам ({max_score} баллов) характеризует аналитичного, осторожного человека. "
                "Внимателен к деталям, следует правилам и стремится к точности. "
                "Предпочитает структурированные задачи и методичный подход к работе.<br/><br/>"
            )
        
        # Анализ комбинации стилей
        description += "<b>Общий портрет поведения:</b><br/>"
        high_scores = [key for key, value in scores.items() if value >= 7]
        
        if len(high_scores) > 1:
            description += f"Сочетание высоких показателей по {' и '.join([disc_names[s] for s in high_scores])} "
            description += "создает уникальный поведенческий профиль с комбинированными характеристиками.<br/>"
        
        # Рекомендации
        description += "<br/><b>Практические рекомендации:</b><br/>"
        if max_style == "D":
            description += "• Развивать навыки терпения и сотрудничества<br/>• Учитывать мнения других при принятии решений<br/>"
        elif max_style == "I":
            description += "• Работать над концентрацией и вниманием к деталям<br/>• Развивать навыки планирования и организации<br/>"
        elif max_style == "S":
            description += "• Постепенно развивать адаптивность к изменениям<br/>• Работать над уверенностью в выражении своего мнения<br/>"
        elif max_style == "C":
            description += "• Развивать гибкость и готовность к компромиссам<br/>• Работать над коммуникативными навыками<br/>"
        
        return description
    
    def _generate_hexaco_detailed_description(self, scores: Dict[str, float]) -> str:
        """Генерирует детальное описание HEXACO на основе реальных баллов"""
        
        # Полные названия факторов HEXACO
        hexaco_names = {
            "H": "Честность-Скромность",
            "E": "Эмоциональность", 
            "X": "Экстраверсия",
            "A": "Доброжелательность",
            "C": "Добросовестность",
            "O": "Открытость опыту"
        }
        
        description = "<b>Результаты тестирования HEXACO:</b><br/><br/>"
        
        # Анализ каждого фактора
        for factor, score in scores.items():
            level = "очень высокий" if score >= 4.5 else "высокий" if score >= 3.5 else "средний" if score >= 2.5 else "низкий"
            description += f"<b>{hexaco_names.get(factor, factor)}: {score} ({level} уровень)</b><br/>"
            
            if factor == "H":  # Честность-Скромность
                if score >= 4:
                    description += ("Высокая честность и скромность. Человек избегает манипуляций, следует моральным принципам "
                                  "и предпочитает справедливость личной выгоде. Проявляет искренность в отношениях.<br/><br/>")
                elif score >= 3:
                    description += ("Умеренная честность. Человек в целом следует этическим нормам, но может проявлять "
                                  "гибкость в зависимости от ситуации.<br/><br/>")
                else:
                    description += ("Прагматичный подход к этическим вопросам. Может проявлять большую гибкость "
                                  "в достижении целей, иногда в ущерб строгим моральным принципам.<br/><br/>")
            
            elif factor == "E":  # Эмоциональность
                if score >= 4:
                    description += ("Высокая эмоциональная чувствительность. Склонен к ярким переживаниям, может беспокоиться "
                                  "о будущем, но также проявляет глубокую эмпатию и привязанность к людям.<br/><br/>")
                elif score >= 3:
                    description += ("Сбалансированная эмоциональность. Способен к эмоциональным переживаниям, "
                                  "но сохраняет стабильность в большинстве ситуаций.<br/><br/>")
                else:
                    description += ("Эмоциональная устойчивость. Редко испытывает сильное беспокойство, "
                                  "сохраняет спокойствие в стрессовых ситуациях.<br/><br/>")
            
            elif factor == "X":  # Экстраверсия
                if score >= 4:
                    description += ("Высокая экстраверсия. Энергичен, общителен, оптимистичен. Предпочитает активное "
                                  "социальное взаимодействие и чувствует себя комфортно в центре внимания.<br/><br/>")
                elif score >= 3:
                    description += ("Сбалансированная социальная активность. Комфортно чувствует себя как в общении, "
                                  "так и в одиночестве, адаптируется к разным социальным ситуациям.<br/><br/>")
                else:
                    description += ("Интровертированность. Предпочитает спокойную обстановку, глубокие беседы "
                                  "с небольшим кругом людей, ценит время наедине с собой.<br/><br/>")
            
            elif factor == "A":  # Доброжелательность
                if score >= 4:
                    description += ("Высокая доброжелательность. Склонен к сотрудничеству, прощению, помощи другим. "
                                  "Ценит гармоничные отношения и старается избегать конфликтов.<br/><br/>")
                elif score >= 3:
                    description += ("Умеренная доброжелательность. Способен к сотрудничеству, но может отстаивать "
                                  "свои интересы при необходимости.<br/><br/>")
                else:
                    description += ("Низкая доброжелательность. Склонен защищать свои интересы, может проявлять "
                                  "критичность и прямолинейность в отношениях с другими.<br/><br/>")
            
            elif factor == "C":  # Добросовестность
                if score >= 4:
                    description += ("Высокая добросовестность. Организован, ответственен, дисциплинирован. "
                                  "Ставит перед собой цели и методично их достигает.<br/><br/>")
                elif score >= 3:
                    description += ("Умеренная добросовестность. В целом организован и ответственен, "
                                  "но может проявлять гибкость в планах.<br/><br/>")
                else:
                    description += ("Спонтанность и гибкость. Предпочитает действовать по ситуации, "
                                  "может испытывать трудности с долгосрочным планированием.<br/><br/>")
            
            elif factor == "O":  # Открытость опыту
                if score >= 4:
                    description += ("Высокая открытость опыту. Любознателен, креативен, интересуется искусством "
                                  "и новыми идеями. Готов к экспериментам и изменениям.<br/><br/>")
                elif score >= 3:
                    description += ("Умеренная открытость. Проявляет интерес к новому, но предпочитает "
                                  "сбалансированный подход между традицией и инновациями.<br/><br/>")
                else:
                    description += ("Предпочтение традиционных подходов. Ценит проверенные методы, "
                                  "стабильность и практичность больше, чем новшества.<br/><br/>")
        
        # Общие рекомендации
        description += "<b>Общие рекомендации для развития:</b><br/>"
        high_traits = [factor for factor, score in scores.items() if score >= 4]
        low_traits = [factor for factor, score in scores.items() if score <= 2.5]
        
        if high_traits:
            description += f"• Использовать сильные стороны: {', '.join([hexaco_names[t] for t in high_traits])}<br/>"
        
        if low_traits:
            description += f"• Развивать при необходимости: {', '.join([hexaco_names[t] for t in low_traits])}<br/>"
        
        description += "• Учитывать личностный профиль при выборе карьерного пути и рабочей среды<br/>"
        
        return description
    
    def _generate_soft_skills_detailed_description(self, scores: Dict[str, float]) -> str:
        """Генерирует детальное описание Soft Skills на основе реальных баллов"""
        
        description = "<b>Результаты оценки Soft Skills (по 10-балльной шкале):</b><br/><br/>"
        
        # Анализ каждого навыка
        for skill, score in scores.items():
            level = "очень высокий" if score >= 8 else "высокий" if score >= 6 else "средний" if score >= 4 else "низкий"
            description += f"<b>{skill}: {score} ({level} уровень)</b><br/>"
            
            # Детальное описание каждого навыка
            if "лидерство" in skill.lower() or "лидер" in skill.lower():
                if score >= 7:
                    description += ("Выраженные лидерские качества. Уверенно берет на себя ответственность за руководство группой, "
                                  "способен мотивировать команду и направлять к достижению общих целей.<br/><br/>")
                elif score >= 4:
                    description += ("Умеренные лидерские способности. Может брать на себя лидерские функции при необходимости, "
                                  "но предпочитает коллегиальный подход.<br/><br/>")
                else:
                    description += ("Предпочитает выполнять роль участника команды. Может испытывать дискомфорт "
                                  "в позиции лидера, предпочитая следовать указаниям других.<br/><br/>")
            
            elif "эмоциональн" in skill.lower():
                if score >= 7:
                    description += ("Высокий эмоциональный интеллект. Отлично понимает и управляет собственными эмоциями, "
                                  "чувствует эмоциональное состояние других людей и использует эту информацию эффективно.<br/><br/>")
                elif score >= 4:
                    description += ("Средний уровень эмоционального интеллекта. Достаточно хорошо понимает эмоции, "
                                  "но иногда может испытывать трудности в сложных ситуациях.<br/><br/>")
                else:
                    description += ("Требуется развитие эмоционального интеллекта. Может испытывать сложности "
                                  "с пониманием и управлением эмоциями - как своими, так и чужими.<br/><br/>")
            
            elif "коммуникац" in skill.lower():
                if score >= 7:
                    description += ("Отличные коммуникативные навыки. Умеет эффективно выражать свои мысли, "
                                  "активно слушает и находит общий язык с разными людьми.<br/><br/>")
                elif score >= 4:
                    description += ("Хорошие коммуникативные способности. В целом эффективно общается, "
                                  "но может нуждаться в улучшении отдельных аспектов.<br/><br/>")
                else:
                    description += ("Необходимо развитие коммуникативных навыков. Может испытывать трудности "
                                  "в выражении мыслей или понимании других людей.<br/><br/>")
            
            elif "критическ" in skill.lower() or "мышлен" in skill.lower():
                if score >= 7:
                    description += ("Развитое критическое мышление. Хорошо анализирует информацию, "
                                  "принимает обоснованные решения и эффективно решает сложные проблемы.<br/><br/>")
                elif score >= 4:
                    description += ("Умеренные аналитические способности. Способен к анализу, но в сложных ситуациях "
                                  "может нуждаться в дополнительной поддержке.<br/><br/>")
                else:
                    description += ("Требуется развитие аналитических навыков. Может испытывать трудности "
                                  "при работе со сложной информацией и принятии решений.<br/><br/>")
            
            elif "врем" in skill.lower():
                if score >= 7:
                    description += ("Отличное управление временем. Хорошо планирует и организует свою деятельность, "
                                  "эффективно расставляет приоритеты и соблюдает сроки.<br/><br/>")
                elif score >= 4:
                    description += ("Удовлетворительное планирование времени. В целом справляется с задачами, "
                                  "но иногда может испытывать трудности с приоритизацией.<br/><br/>")
                else:
                    description += ("Необходимо улучшение навыков тайм-менеджмента. Может испытывать сложности "
                                  "с планированием и соблюдением сроков.<br/><br/>")
            
            elif "конфликт" in skill.lower():
                if score >= 7:
                    description += ("Высокие навыки разрешения конфликтов. Умеет сохранять спокойствие в напряженных ситуациях "
                                  "и находить решения, учитывающие интересы всех сторон.<br/><br/>")
                elif score >= 4:
                    description += ("Средние способности к разрешению конфликтов. Может справляться с большинством ситуаций, "
                                  "но сложные конфликты могут вызывать затруднения.<br/><br/>")
                else:
                    description += ("Требуется развитие навыков работы с конфликтами. Может избегать конфликтных ситуаций "
                                  "или испытывать стресс при их возникновении.<br/><br/>")
            
            elif "адаптив" in skill.lower():
                if score >= 7:
                    description += ("Высокая адаптивность. Быстро и эффективно приспосабливается к изменениям, "
                                  "сохраняет продуктивность в новых условиях.<br/><br/>")
                elif score >= 4:
                    description += ("Умеренная гибкость. Способен адаптироваться к изменениям, "
                                  "но может потребоваться время для полного приспособления.<br/><br/>")
                else:
                    description += ("Предпочитает стабильность. Изменения могут вызывать дискомфорт, "
                                  "требуется поддержка при адаптации к новым условиям.<br/><br/>")
            
            else:  # Для остальных навыков
                if score >= 7:
                    description += f"Высокий уровень развития навыка '{skill}'. Демонстрирует уверенное владение и эффективное применение.<br/><br/>"
                elif score >= 4:
                    description += f"Средний уровень навыка '{skill}'. Есть базовые способности, но возможно улучшение.<br/><br/>"
                else:
                    description += f"Навык '{skill}' требует развития. Рекомендуется уделить внимание его улучшению.<br/><br/>"
        
        # Общие рекомендации
        top_skills = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        bottom_skills = [skill for skill, score in scores.items() if score < 5]
        
        description += "<b>Рекомендации по развитию:</b><br/>"
        description += f"• <b>Сильные стороны:</b> {', '.join([skill for skill, _ in top_skills])}<br/>"
        
        if bottom_skills:
            description += f"• <b>Области для развития:</b> {', '.join(bottom_skills)}<br/>"
        
        description += "• Использовать сильные навыки для компенсации слабых областей<br/>"
        description += "• Создать план развития приоритетных навыков для карьерного роста<br/>"
        
        return description
    
    def _format_scores(self, scores: Dict[str, float]) -> str:
        """Форматирует результаты в читаемую строку"""
        return ", ".join([f"{k}: {v}" for k, v in scores.items()])