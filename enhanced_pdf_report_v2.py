#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенный модуль для создания PDF отчётов с детальными описаниями
Версия 2.0 с расширенным контентом и правильной последовательностью тестов
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional
from io import BytesIO
from copy import deepcopy
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
import sys
from pathlib import Path

# Добавляем путь к модулям проекта
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from src.psytest.ai_interpreter import get_ai_interpreter
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️ AI интерпретатор недоступен - будут использованы статические интерпретации")
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
        """Создаёт минималистичную радарную диаграмму"""
        return make_radar(labels, values, out_path, title=title, max_value=10)
    
    @staticmethod
    def create_minimalist_bar_chart(labels: List[str], values: List[float],
                                   title: str, out_path: Path) -> Path:
        """Создаёт минималистичную столбчатую диаграмму"""
        return make_bar_chart(labels, values, out_path, title=title, max_value=10)


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
                print(f"⚠️  Ошибка при добавлении диаграммы {chart_path}: {e}")
                # Добавляем плейсхолдер
                story.append(Paragraph(f"[Диаграмма: {chart_path.name}]", self._get_custom_styles()['Body']))
                story.append(Spacer(1, 5*mm))
    
    def _generate_dynamic_interpretations(self, paei_scores: Dict[str, float], 
                                        disc_scores: Dict[str, float],
                                        hexaco_scores: Dict[str, float], 
                                        soft_skills_scores: Dict[str, float]) -> Dict[str, str]:
        """Генерирует динамические интерпретации тестов используя AI интерпретатор с промптами *_system_res.txt"""
        interpretations = {}
        
        if AI_AVAILABLE:
            try:
                # Создаем AI интерпретатор
                ai = get_ai_interpreter()
                if ai:
                    print("🤖 Генерируем динамические интерпретации с помощью AI...")
                    
                    # PAEI интерпретация с промптом adizes_system_res.txt
                    interpretations['paei'] = ai.interpret_paei(paei_scores)
                    
                    # Soft Skills интерпретация с промптом soft_system_res.txt  
                    interpretations['soft_skills'] = ai.interpret_soft_skills(soft_skills_scores)
                    
                    # HEXACO интерпретация с промптом hexaco_system_res.txt
                    interpretations['hexaco'] = ai.interpret_hexaco(hexaco_scores)
                    
                    # DISC интерпретация с промптом disk_system_res.txt
                    interpretations['disc'] = ai.interpret_disc(disc_scores)
                    
                    print("✅ Динамические интерпретации сгенерированы успешно")
                    return interpretations
                    
            except Exception as e:
                print(f"⚠️ Ошибка AI интерпретации: {e}")
        
        print("📝 Используем статические интерпретации...")
        # Fallback к статическим интерпретациям
        try:
            # PAEI интерпретация
            paei_text = f"""
            На основе тестирования Адизеса получены следующие результаты:
            
            {self._format_scores_detailed(paei_scores)}
            
            Доминирующий стиль: {max(paei_scores, key=paei_scores.get)} ({max(paei_scores.values())} баллов)
            
            Анализ показывает сбалансированное/доминирующее распределение управленческих ролей с акцентом на 
            {max(paei_scores, key=paei_scores.get).lower()}.
            """
            interpretations['paei'] = paei_text.strip()
            
            # Soft Skills интерпретация
            top_soft = max(soft_skills_scores, key=soft_skills_scores.get)
            soft_text = f"""
            Анализ мягких навыков выявляет следующий профиль:
            
            {self._format_scores_detailed(soft_skills_scores)}
            
            Наиболее развитый навык: {top_soft} ({soft_skills_scores[top_soft]} баллов)
            
            Демонстрирует высокий уровень развития в области {top_soft.lower()}, что является ключевым 
            преимуществом для профессиональной деятельности.
            """
            interpretations['soft_skills'] = soft_text.strip()
            
            # HEXACO интерпретация  
            top_hexaco = max(hexaco_scores, key=hexaco_scores.get)
            hexaco_text = f"""
            Анализ личностного профиля HEXACO:
            
            {self._format_scores_detailed(hexaco_scores)}
            
            Наиболее выраженная черта: {top_hexaco} ({hexaco_scores[top_hexaco]} баллов)
            
            Профиль характеризуется высокими показателями по шкале {top_hexaco.lower()}, что указывает на 
            соответствующие личностные особенности и поведенческие тенденции.
            """
            interpretations['hexaco'] = hexaco_text.strip()
            
            # DISC интерпретация
            top_disc = max(disc_scores, key=disc_scores.get)
            disc_text = f"""
            Анализ поведенческого профиля DISC:
            
            {self._format_scores_detailed(disc_scores)}
            
            Доминирующий стиль: {top_disc} ({disc_scores[top_disc]} баллов)
            
            Поведенческий профиль характеризуется преобладанием стиля {top_disc.lower()}, что определяет 
            основные паттерны взаимодействия и рабочие предпочтения.
            """
            interpretations['disc'] = disc_text.strip()
            
        except Exception as e:
            print(f"⚠️ Ошибка генерации статических интерпретаций: {e}")
            # Базовые интерпретации
            interpretations = {
                'paei': 'Результаты теста Адизеса показывают управленческий профиль.',
                'soft_skills': 'Анализ мягких навыков демонстрирует профессиональные компетенции.',
                'hexaco': 'Личностный профиль HEXACO характеризует основные черты личности.',
                'disc': 'Поведенческий профиль DISC отражает стили взаимодействия.'
            }
        
        return interpretations

    def _format_scores_detailed(self, scores: Dict[str, float]) -> str:
        """Форматирует результаты в детальную строку"""
        return "\n".join([f"• {k}: {v} баллов" for k, v in scores.items()])

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
        
        # Генерируем динамические интерпретации
        dynamic_interpretations = self._generate_dynamic_interpretations(
            paei_scores, disc_scores, hexaco_scores, soft_skills_scores
        )
        
        # Используем динамические интерпретации вместо переданных
        ai_interpretations = dynamic_interpretations
        
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
        story.append(Spacer(1, 4*mm))  # уменьшен отступ с 8мм до 4мм
        
        # === ИМЯ УЧАСТНИКА (ПО ЦЕНТРУ, УВЕЛИЧЕННЫЙ ШРИФТ) ===
        story.append(Paragraph(participant_name, styles['ParticipantName']))
        story.append(Spacer(1, 2*mm))
        
        # === ДАТА ТЕСТИРОВАНИЯ ===
        date_text = f"Дата тестирования: {test_date}"
        story.append(Paragraph(date_text, styles['Body']))
        story.append(Spacer(1, 6*mm))  # уменьшен отступ с 10мм до 6мм
        
        # === ОБЩЕЕ ЗАКЛЮЧЕНИЕ И РЕКОМЕНДАЦИИ ===
        story.append(Paragraph("ОБЩЕЕ ЗАКЛЮЧЕНИЕ И РЕКОМЕНДАЦИИ", styles['SectionTitle']))
        story.append(Spacer(1, 3*mm))  # уменьшен отступ с 5мм до 3мм
        
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
        story.append(Spacer(1, 3*mm))  # уменьшен отступ с 5мм до 3мм
        
        # Сводка по ключевым характеристикам и методикам
        story.append(Paragraph("<b>Ключевые характеристики профиля и использованные методики:</b>", styles['SubTitle']))
        
        # Результаты тестирования с детальным описанием методик
        results_text = f"""
        <b>Результаты тестирования:</b><br/>
        • <b>Тест Адизеса (PAEI)</b> - оценка управленческих ролей и стилей руководства (5 вопросов по 4 типам). Преобладает роль {paei_names.get(max_paei, max_paei)} - {paei_scores[max_paei]} баллов<br/>
        • <b>Оценка Soft Skills</b> - анализ надпрофессиональных компетенций (10 вопросов по 10-балльной шкале). Наиболее развитый навык: {max_soft} - {soft_skills_scores[max_soft]} баллов<br/>
        • <b>HEXACO</b> - современная шестифакторная модель личности (10 вопросов по 5-балльной шкале). Выраженная личностная черта: {max_hexaco} ({hexaco_scores[max_hexaco]} баллов)<br/>
        • <b>DISC</b> - методика оценки поведенческих особенностей и стилей (8 вопросов по 4 типам). {disc_names.get(max_disc, max_disc)} ({disc_scores[max_disc]} баллов)
        """
        story.append(Paragraph(results_text, styles['Body']))
        story.append(Spacer(1, 3*mm))
        
        # Описание использованных методик
        story.append(Paragraph("<b>Использованные методики:</b>", styles['SubTitle']))
        methodologies_text = """
        • <b>Тест Адизеса (PAEI)</b> - оценка управленческих ролей и стилей руководства<br/>
        • <b>Оценка Soft Skills</b> - анализ надпрофессиональных компетенций<br/>
        • <b>HEXACO</b> - современная модель личности (Lee & Ashton, 2004)<br/>
        • <b>DISC</b> - методика оценки поведенческих стилей (Marston, 1928)
        """
        story.append(Paragraph(methodologies_text, styles['Body']))
        story.append(Spacer(1, 6*mm))
        
        # Профессиональные рекомендации
        story.append(Paragraph("<b>Рекомендации по профессиональному развитию:</b>", styles['SubTitle']))
        
        # 1. Использование сильных сторон
        story.append(Paragraph("<b>1. Использование сильных сторон:</b>", styles['Body']))
        story.append(Paragraph(f"• (PAEI): Делегировать задачи, соответствующие профилю {paei_names.get(max_paei, max_paei)}", styles['ListWithIndent']))
        story.append(Paragraph(f"• (Soft Skills): Развивать {max_soft.lower()} через специализированные проекты", styles['ListWithIndent']))
        story.append(Paragraph(f"• (DISC): Использовать {disc_names.get(max_disc, max_disc).lower()} в командном взаимодействии", styles['ListWithIndent']))
        story.append(Spacer(1, 2*mm))
        
        # 2. Области для развития  
        story.append(Paragraph("<b>2. Области для развития:</b>", styles['Body']))
        story.append(Paragraph("• (PAEI): Работать над менее выраженными управленческими ролями", styles['ListWithIndent']))
        story.append(Paragraph("• (Soft Skills): Развивать дополнительные soft skills для универсальности [поиск курсов в Google]", styles['ListWithIndent']))
        story.append(Paragraph("• (DISC): Балансировать поведенческий стиль в зависимости от ситуации", styles['ListWithIndent']))
        story.append(Spacer(1, 2*mm))
        
        # 3. Карьерные перспективы
        story.append(Paragraph("<b>3. Карьерные перспективы:</b>", styles['Body']))
        story.append(Paragraph(f"• (PAEI): Рассмотреть позиции, требующие качеств {paei_names.get(max_paei, max_paei)}", styles['ListWithIndent']))
        story.append(Paragraph("• (HEXACO): Планировать развитие с учетом личностного профиля HEXACO", styles['ListWithIndent']))
        story.append(Paragraph("• (DISC): Выстраивать команду с учетом комплементарных ролей по DISC", styles['ListWithIndent']))
        story.append(Spacer(1, 6*mm))  # уменьшен отступ с 10мм до 6мм
        
        # Переход к детальным разделам
        story.append(PageBreak())
        
        # === 1. ТЕСТ АДИЗЕСА (PAEI) ===
        story.append(Paragraph("1. ТЕСТ АДИЗЕСА (PAEI) - УПРАВЛЕНЧЕСКИЕ РОЛИ", styles['SectionTitle']))
        
        # Описание теста в красной рамке (как на скриншоте)
        test_description = "Тест Адизеса (PAEI) - оценка управленческих ролей и стилей руководства (5 вопросов по 4 типам)."
        story.append(Paragraph(test_description, styles['Body']))
        story.append(Spacer(1, 3*mm))
        
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
        story.append(Spacer(1, 6*mm))  # уменьшен отступ с 8мм до 6мм
        
        # === 2. SOFT SKILLS - МЯГКИЕ НАВЫКИ ===
        story.append(Paragraph("2. SOFT SKILLS - ОЦЕНКА МЯГКИХ НАВЫКОВ", styles['SectionTitle']))
        
        # Описание теста в красной рамке (как на скриншоте)
        test_description = "Оценка Soft Skills - анализ надпрофессиональных компетенций (10 вопросов по 10-балльной шкале)."
        story.append(Paragraph(test_description, styles['Body']))
        story.append(Spacer(1, 3*mm))
        
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
        
        # Интерпретация Soft Skills (динамическая из промптов)
        if 'soft_skills' in ai_interpretations:
            story.append(Paragraph("<b>Интерпретация:</b>", styles['SubTitle']))
            story.append(Paragraph(ai_interpretations['soft_skills'], styles['Body']))
        
        story.append(Spacer(1, 8*mm))
        
        # === 3. ТЕСТ HEXACO - ЛИЧНОСТНЫЕ ЧЕРТЫ ===
        story.append(Paragraph("3. ТЕСТ HEXACO - МОДЕЛЬ ЛИЧНОСТИ", styles['SectionTitle']))
        
        # Описание теста в красной рамке (как на скриншоте)
        test_description = "HEXACO - современная шестифакторная модель личности (10 вопросов по 5-балльной шкале)."
        story.append(Paragraph(test_description, styles['Body']))
        story.append(Spacer(1, 3*mm))
        
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
        
        # Описание теста в красной рамке (как на скриншоте)
        test_description = "DISC - методика оценки поведенческих особенностей и стилей (8 вопросов по 4 типам)."
        story.append(Paragraph(test_description, styles['Body']))
        story.append(Spacer(1, 3*mm))
        
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
        
        # Сборка PDF с нумерацией страниц в верхнем правом углу
        # Двухэтапный процесс: сначала определяем общее количество страниц, потом генерируем с нумерацией
        
        # Этап 1: Предварительная сборка для подсчета страниц (без нумерации)
        temp_buffer = BytesIO()
        temp_doc = SimpleDocTemplate(temp_buffer, pagesize=A4, 
                                   rightMargin=DesignConfig.MARGIN*mm, 
                                   leftMargin=DesignConfig.MARGIN*mm,
                                   topMargin=DesignConfig.MARGIN*mm, 
                                   bottomMargin=DesignConfig.MARGIN*mm)
        
        # Создаем новые экземпляры элементов для предварительной сборки
        from copy import deepcopy
        temp_story = deepcopy(story)
        temp_doc.build(temp_story)
        total_pages = temp_doc.page
        
        # Этап 2: Финальная сборка с правильной нумерацией
        def add_page_number_with_total(canvas, doc):
            """Добавляет номер страницы в верхний правый угол в формате 'Стр. X из N'"""
            canvas.saveState()
            canvas.setFont('Arial-Regular', 10)
            page_num = canvas.getPageNumber()
            text = f"Стр. {page_num} из {total_pages}"
            # Позиция в верхнем правом углу (отступ 20мм от краев)
            canvas.drawRightString(A4[0] - DesignConfig.MARGIN*mm, 
                                 A4[1] - DesignConfig.MARGIN*mm + 5, 
                                 text)
            canvas.restoreState()
        
        doc.build(story, onFirstPage=add_page_number_with_total, onLaterPages=add_page_number_with_total)
        
        # СОХРАНЕНИЕ ТОЛЬКО В GOOGLE DRIVE (БЕЗ ЛОКАЛЬНЫХ КОПИЙ)
        print("📤 Сохранение PDF только в Google Drive...")
        try:
            from oauth_google_drive import upload_to_google_drive_oauth
            import os
            
            drive_link = upload_to_google_drive_oauth(str(out_path), "PsychTest Reports")
            if drive_link:
                print(f"✅ PDF сохранен в Google Drive!")
                print(f"🔗 Ссылка: {drive_link}")
                
                # Удаляем локальный файл после успешной загрузки
                try:
                    os.remove(str(out_path))
                    print(f"🗑️ Локальный файл удален: {out_path.name}")
                except Exception as e:
                    print(f"⚠️ Не удалось удалить локальный файл: {e}")
                
                # Возвращаем ссылку на Google Drive вместо локального пути
                return drive_link
            else:
                print("❌ Ошибка загрузки в Google Drive - файл остается локально")
                return out_path
        except Exception as e:
            print(f"❌ Ошибка загрузки в Google Drive: {e}")
            print("📄 Файл сохранен локально")
            return out_path
    
    def _create_all_charts(self, paei_scores: Dict, disc_scores: Dict, 
                         hexaco_scores: Dict, soft_skills_scores: Dict) -> Dict[str, Path]:
        """Создаёт все радарные диаграммы для отчета"""
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
        
        # Имя участника (увеличенный шрифт, по центру)
        styles.add(ParagraphStyle(
            name='ParticipantName',
            parent=styles['Normal'],
            fontSize=14,  # увеличенный шрифт
            fontName=DesignConfig.TITLE_FONT,
            textColor=DesignConfig.PRIMARY_COLOR,
            alignment=1,  # CENTER
            spaceAfter=2,
            spaceBefore=2,
        ))
        
        # Стиль для списков с отступом (как на скриншоте)
        styles.add(ParagraphStyle(
            name='ListWithIndent',
            parent=styles['Normal'],
            fontSize=DesignConfig.BODY_SIZE,
            fontName=DesignConfig.BODY_FONT,
            textColor=DesignConfig.TEXT_COLOR,
            leftIndent=15,  # отступ слева для элементов списка
            spaceAfter=2,
            leading=14,
        ))
        
        return styles
    
    def _format_scores(self, scores: Dict[str, float]) -> str:
        """Форматирует результаты в читаемую строку"""
        return ", ".join([f"{k}: {v}" for k, v in scores.items()])
    
    def upload_to_google_drive(self, file_path: Path, participant_name: str = None) -> Optional[str]:
        """
        Загрузка PDF в Google Drive (интеграция с oauth_google_drive.py)
        
        Args:
            file_path: Путь к файлу для загрузки
            participant_name: Имя участника (для логирования)
            
        Returns:
            Optional[str]: Ссылка на файл в Google Drive или None при ошибке
        """
        try:
            from oauth_google_drive import upload_to_google_drive_oauth
            
            print(f"📤 Загрузка PDF отчета в Google Drive: {participant_name or 'неизвестный пользователь'}")
            
            # Загружаем с месячной структурой папок: PsychTest Reports/2025/10-October
            web_link = upload_to_google_drive_oauth(
                file_path=str(file_path),
                folder_name="PsychTest Reports",
                use_monthly_structure=True
            )
            
            if web_link:
                print(f"🎉 PDF успешно загружен в Google Drive!")
                print(f"🔗 Ссылка для просмотра: {web_link}")
                return web_link
            else:
                print("❌ Не удалось загрузить PDF в Google Drive")
                return None
                
        except ImportError:
            print("⚠️ Google Drive интеграция недоступна (отсутствует oauth_google_drive)")
            return None
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
        Генерирует PDF отчёт и загружает в Google Drive
        
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
            gdrive_link = self.upload_to_google_drive(pdf_path, participant_name)
        
        return pdf_path, gdrive_link