#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенный модуль для создания PDF отчётов с детальными описаниями
Версия 2.0 с расширенным контентом и правильной последовательностью тестов
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
from io import BytesIO
from copy import deepcopy
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import sys
from interpretation_utils import generate_interpretations_from_prompt

# Добавляем путь к модулям проекта
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from src.psytest.ai_interpreter import get_ai_interpreter
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️ AI интерпретатор недоступен - будут использованы статические интерпретации")

from src.psytest.charts import make_radar, make_bar_chart, make_paei_combined_chart, make_disc_combined_chart, make_hexaco_radar

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
    
    # Размеры графиков (в мм) - расширены на всю ширину страницы
    RADAR_SIZE = 160  # увеличено для использования полной ширины
    BAR_CHART_WIDTH = 180  # увеличено для полной ширины
    BAR_CHART_HEIGHT = 90  # увеличено пропорционально
    PAEI_COMBINED_WIDTH = 180  # специальный размер для комбинированной диаграммы PAEI
    PAEI_COMBINED_HEIGHT = 90  # высота комбинированной диаграммы
    
    # Шрифты (используем встроенные Unicode шрифты) - изменяемые атрибуты
    TITLE_FONT: str = "Times-Bold"
    BODY_FONT: str = "Times-Roman"
    SMALL_FONT: str = "Times-Roman"
    
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
    
    @staticmethod
    def create_paei_combined_chart(labels: List[str], values: List[float],
                                  title: str, out_path: Path) -> Path:
        """Создаёт комбинированную диаграмму PAEI (столбиковая + круговая)"""
        return make_paei_combined_chart(labels, values, out_path, title=title)
    
    @staticmethod
    def create_disc_combined_chart(labels: List[str], values: List[float],
                                  title: str, out_path: Path) -> Path:
        """Создаёт комбинированную диаграмму DISC (столбиковая + круговая)"""
        return make_disc_combined_chart(labels, values, out_path, title=title)
        
    @staticmethod
    def create_hexaco_radar(labels: List[str], values: List[float], 
                          title: str, out_path: Path) -> Path:
        """Создаёт радарную диаграмму HEXACO с расшифровками аббревиатур"""
        return make_hexaco_radar(labels, values, out_path, title=title)


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
    
    def _add_chart_to_story(
        self,
        story,
        chart_path: Path,
        styles,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        """Добавляет диаграмму в документ с оптимизированными размерами"""
        if chart_path.exists():
            try:
                # Специальные размеры для комбинированных диаграмм
                if "paei_combined" in str(chart_path) or "disc_combined" in str(chart_path):
                    chart_width = DesignConfig.PAEI_COMBINED_WIDTH
                    chart_height = DesignConfig.PAEI_COMBINED_HEIGHT
                # Используем стандартные размеры если не указаны явно
                elif width is None:
                    chart_width = DesignConfig.RADAR_SIZE
                    if height is None:
                        chart_height = DesignConfig.RADAR_SIZE
                    else:
                        chart_height = height
                else:
                    chart_width = width
                    chart_height = height or DesignConfig.RADAR_SIZE
                    
                # Конвертируем размеры в миллиметры
                img = Image(str(chart_path), width=chart_width*mm, height=chart_height*mm)
                img.hAlign = 'CENTER'
                story.append(img)
                story.append(Spacer(1, 3*mm))  # уменьшен с 5мм до 3мм
            except Exception as e:
                print(f"⚠️  Ошибка при добавлении диаграммы {chart_path}: {e}")
                # Добавляем плейсхолдер
                story.append(Paragraph(f"[Диаграмма: {chart_path.name}]", styles['Body']))
                story.append(Spacer(1, 3*mm))  # уменьшен с 5мм до 3мм

    def _create_doc_template(self, target) -> SimpleDocTemplate:
        """Создаёт настроенный шаблон документа для ReportLab."""
        return SimpleDocTemplate(
            target,
            pagesize=A4,
            rightMargin=DesignConfig.MARGIN * mm,
            leftMargin=DesignConfig.MARGIN * mm,
            topMargin=DesignConfig.MARGIN * mm,
            bottomMargin=DesignConfig.MARGIN * mm,
        )

    def _count_story_pages(self, story) -> int:
        """Подсчитывает итоговое количество страниц, не записывая файл на диск."""
        temp_buffer = BytesIO()
        temp_doc = self._create_doc_template(temp_buffer)
        temp_doc.build(deepcopy(story))
        return temp_doc.page

    def _draw_page_number(self, canvas_obj, total_pages: int) -> None:
        """Рисует нумерацию страниц в формате 'Стр. X из N'."""
        canvas_obj.saveState()
        canvas_obj.setFont(DesignConfig.BODY_FONT, 10)
        page_num = canvas_obj.getPageNumber()
        text = f"Стр. {page_num} из {total_pages}"
        canvas_obj.drawRightString(
            A4[0] - DesignConfig.MARGIN * mm,
            A4[1] - DesignConfig.MARGIN * mm + 5,
            text,
        )
        canvas_obj.restoreState()
    
    def _generate_dynamic_interpretations(self, paei_scores: Dict[str, float], 
                                        disc_scores: Dict[str, float],
                                        hexaco_scores: Dict[str, float], 
                                        soft_skills_scores: Dict[str, float]) -> Dict[str, str]:
        """Генерирует динамические интерпретации тестов используя AI интерпретатор с промптами *_system_res.txt"""
        interpretations = {}
        
        print(f"[DEBUG] USE_AI_INTERPRETATIONS: {os.getenv('USE_AI_INTERPRETATIONS')}")
        print(f"[DEBUG] OPENAI_API_KEY: {'set' if os.getenv('OPENAI_API_KEY') else 'not set'}")
        print(f"[DEBUG] AI_AVAILABLE: {AI_AVAILABLE}")
        try:
            import openai
            print(f"[DEBUG] openai version: {openai.__version__}")
        except Exception as e:
            print(f"[DEBUG] openai import error: {e}")
        if AI_AVAILABLE:
            try:
                # Создаем AI интерпретатор
                ai = get_ai_interpreter()
                if ai:
                    print("🤖 Генерируем динамические интерпретации с помощью AI...")
                    
                    # PAEI интерпретация с промптом adizes_system_res.txt
                    # Явно требуем развернутую интерпретацию в стиле психологического портрета
                    user_prompt = (
                        f"Проанализируй результаты теста PAEI: {', '.join([f'{k}: {v}' for k, v in paei_scores.items()])}\n"
                        "Составь подробную интерпретацию в стиле психологического портрета, как в примерах, с выделением доминирующего стиля, сильных сторон, зон роста, рекомендаций и подходящих профессиональных ролей. Используй структуру и разметку, как в образцах."
                    )
                    ai_result = ai.interpret_paei(paei_scores, dialog_context=user_prompt)
                    print("\n===== AI PAEI INTERPRETATION (DEBUG) =====\n" + ai_result + "\n==========================================\n")
                    interpretations['paei'] = ai_result
                    
                    # Soft Skills интерпретация с промптом soft_system_res.txt
                    soft_skills_result = ai.interpret_soft_skills(soft_skills_scores)
                    print("\n===== AI SOFT SKILLS INTERPRETATION (DEBUG) =====\n" + soft_skills_result + "\n===============================================\n")
                    interpretations['soft_skills'] = soft_skills_result
                    
                    # HEXACO интерпретация с промптом hexaco_system_res.txt
                    interpretations['hexaco'] = ai.interpret_hexaco(hexaco_scores)
                    
                    # DISC интерпретация с промптом disk_system_res.txt
                    interpretations['disc'] = ai.interpret_disc(disc_scores)
                    
                    print("✅ Динамические интерпретации сгенерированы успешно")
                    return interpretations
                    
            except Exception as e:
                print(f"⚠️ Ошибка AI интерпретации: {e}")
        
        print("📝 Используем статические интерпретации через generate_interpretations_from_prompt...")
        try:
            interpretations = generate_interpretations_from_prompt(
                paei_scores, disc_scores, hexaco_scores, soft_skills_scores
            )
            print("✅ Статические интерпретации сгенерированы успешно через generate_interpretations_from_prompt")
            return interpretations
        except Exception as e:
            print(f"⚠️ Ошибка статической интерпретации: {e}")
            # Если всё совсем плохо — возвращаем пустые строки
            interpretations = {
                'paei': '',
                'soft_skills': '',
                'hexaco': '',
                'disc': ''
            }
            return interpretations

    def _format_scores_detailed(self, scores: Dict[str, float]) -> str:
        """Форматирует результаты в детальную строку"""
        return "\n".join([f"• {k}: {v} баллов" for k, v in scores.items()])

    def _build_story(
        self,
        participant_name: str,
        test_date: str,
        paei_scores: Dict[str, float],
        disc_scores: Dict[str, float],
        hexaco_scores: Dict[str, float],
        soft_skills_scores: Dict[str, float],
        ai_interpretations: Dict[str, str],
        chart_paths: Dict[str, Path],
    ):
        """Формирует последовательность элементов отчёта (story)."""
        styles = self._get_custom_styles()
        story = []

        # === ЗАГОЛОВОК ДОКУМЕНТА ===
        story.append(Paragraph("ОЦЕНКА КОМАНДНЫХ НАВЫКОВ", styles['MainTitle']))
        story.append(Spacer(1, 1 * mm))

        # === ИМЯ УЧАСТНИКА (ПО ЦЕНТРУ, уменьшенный шрифт) ===
        if participant_name.strip():
            story.append(Paragraph(participant_name, styles['ParticipantName']))
            story.append(Spacer(1, 1 * mm))

        # === ДАТА ТЕСТИРОВАНИЯ ===
        date_text = f"Дата тестирования: {test_date}"
        story.append(Paragraph(date_text, styles['Body']))
        story.append(Spacer(1, 2 * mm))

        # === ОБЩЕЕ ЗАКЛЮЧЕНИЕ И РЕКОМЕНДАЦИИ ===
        story.append(Paragraph("ОБЩЕЕ ЗАКЛЮЧЕНИЕ И РЕКОМЕНДАЦИИ", styles['SectionTitle']))
        story.append(Spacer(1, 2 * mm))

        # Определяем доминирующие черты для заключения
        max_paei = max(paei_scores, key=lambda k: paei_scores[k])
        max_disc = max(disc_scores, key=lambda k: disc_scores[k])
        max_hexaco = max(hexaco_scores, key=lambda k: hexaco_scores[k])
        max_soft = max(soft_skills_scores, key=lambda k: soft_skills_scores[k])

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
        story.append(Spacer(1, 3 * mm))  # уменьшен отступ с 5мм до 3мм

        # Сводка по ключевым характеристикам и методикам
        story.append(Paragraph("<b>Ключевые характеристики профиля и использованные методики:</b>", styles['SubTitle']))

        # Результаты тестирования с детальным описанием методик
        story.append(Paragraph("<b>Результаты тестирования:</b>", styles['Body']))
        bullet_items = [
            f"<b>Тест Адизеса (PAEI)</b> - оценка управленческих ролей и стилей руководства (5 вопросов по 4 типам). Преобладает роль {paei_names.get(max_paei, max_paei)} - {paei_scores[max_paei]} баллов",
            f"<b>Оценка Soft Skills</b> - анализ надпрофессиональных компетенций (10 вопросов по 10-балльной шкале). Наиболее развитый навык: {max_soft} - {soft_skills_scores[max_soft]} баллов",
            f"<b>HEXACO</b> - современная шестифакторная модель личности (10 вопросов по 5-балльной шкале). Выраженная личностная черта: {max_hexaco} ({hexaco_scores[max_hexaco]} баллов)",
            f"<b>DISC</b> - методика оценки поведенческих особенностей и стилей (8 вопросов по 4 типам). {disc_names.get(max_disc, max_disc)} ({disc_scores[max_disc]} баллов)",
        ]
        for item in bullet_items:
            story.append(Paragraph(item, style=styles['ListWithIndent'], bulletText='•'))
        story.append(Spacer(1, 2 * mm))

        # Профессиональные рекомендации
        story.append(Paragraph("<b>Рекомендации по профессиональному развитию:</b>", styles['SubTitle']))

        # 1. Использование сильных сторон
        story.append(Paragraph("<b>1. Использование сильных сторон:</b>", styles['Body']))
        story.append(Paragraph(f"• (PAEI): Делегировать задачи, соответствующие профилю {paei_names.get(max_paei, max_paei)}", styles['ListWithIndent']))
        story.append(Paragraph(f"• (Soft Skills): Развивать {max_soft.lower()} через специализированные проекты", styles['ListWithIndent']))
        story.append(Paragraph(f"• (DISC): Использовать {disc_names.get(max_disc, max_disc)} в командном взаимодействии", styles['ListWithIndent']))
        story.append(Spacer(1, 2 * mm))

        # 2. Области для развития
        story.append(Paragraph("<b>2. Области для развития:</b>", styles['Body']))
        story.append(Paragraph("• (PAEI): Работать над менее выраженными управленческими ролями", styles['ListWithIndent']))
        story.append(Paragraph("• (Soft Skills): Развивать дополнительные soft skills для универсальности [поиск курсов в Google]", styles['ListWithIndent']))
        story.append(Paragraph("• (DISC): Балансировать поведенческий стиль в зависимости от ситуации", styles['ListWithIndent']))
        story.append(Spacer(1, 2 * mm))

        # 3. Карьерные перспективы
        story.append(Paragraph("<b>3. Карьерные перспективы:</b>", styles['Body']))
        story.append(Paragraph(f"• (PAEI): Рассмотреть позиции, требующие качеств {paei_names.get(max_paei, max_paei)}", styles['ListWithIndent']))
        story.append(Paragraph("• (HEXACO): Планировать развитие с учетом личностного профиля HEXACO", styles['ListWithIndent']))
        story.append(Paragraph("• (DISC): Выстраивать команду с учетом комплементарных ролей по DISC", styles['ListWithIndent']))
        story.append(Spacer(1, 6 * mm))  # уменьшен отступ с 10мм до 6мм

        # Переход к детальным разделам
        story.append(PageBreak())

        # === 1. ТЕСТ АДИЗЕСА (PAEI) ===
        story.append(Paragraph("1. ТЕСТ АДИЗЕСА (PAEI) - УПРАВЛЕНЧЕСКИЕ РОЛИ", styles['SectionTitle']))

        test_description = "Тест Адизеса (PAEI) - оценка управленческих ролей и стилей руководства (5 вопросов по 4 типам)."
        story.append(Paragraph(test_description, styles['Body']))
        story.append(Spacer(1, 3 * mm))

        story.append(Paragraph("<b>Расшифровка PAEI:</b>", styles['Body']))
        paei_bullets = [
            f"<b>P (Producer - Производитель)</b> - ориентация на результат, выполнение задач, достижение целей: {paei_scores.get('P', '')} баллов",
            f"<b>A (Administrator - Администратор)</b> - организация процессов, контроль, систематизация работы: {paei_scores.get('A', '')} баллов.",
            f"<b>E (Entrepreneur - Предприниматель)</b> - инновации, стратегическое мышление, креативность: {paei_scores.get('E', '')} баллов.",
            f"<b>I (Integrator - Интегратор)</b> - командная работа, мотивация людей, создание единства: {paei_scores.get('I', '')} баллов.",
        ]
        for item in paei_bullets:
            story.append(Paragraph(item, style=styles['ListWithIndent'], bulletText='•'))
        story.append(Spacer(1, 5 * mm))

        if 'paei' in chart_paths:
            self._add_chart_to_story(story, chart_paths['paei'], styles)

        if 'paei' in ai_interpretations:
            story.append(Paragraph("<b>Интерпретация:</b>", styles['SubTitle']))
            paei_text = ai_interpretations['paei'].replace('\n', '<br/>')
            story.append(Paragraph(paei_text, styles['Body']))
        story.append(Spacer(1, 6 * mm))

        # === 2. SOFT SKILLS - МЯГКИЕ НАВЫКИ ===
        story.append(Paragraph("2. SOFT SKILLS - ОЦЕНКА МЯГКИХ НАВЫКОВ", styles['SectionTitle']))

        test_description = "Оценка Soft Skills - анализ надпрофессиональных компетенций (10 вопросов по 10-балльной шкале)."
        story.append(Paragraph(test_description, styles['Body']))
        story.append(Spacer(1, 3 * mm))

        soft_description = """
        <b>Soft Skills</b> - это надпрофессиональные навыки, которые помогают решать жизненные и рабочие задачи 
        независимо от специальности. Включают коммуникативные способности, лидерские качества, креативность, 
        аналитическое мышление и адаптивность. Эти навыки определяют эффективность взаимодействия с людьми 
        и способность к профессиональному росту в любой сфере деятельности.
        """
        story.append(Paragraph(soft_description, styles['Body']))
        story.append(Spacer(1, 5 * mm))

        soft_results = f"<b>Результаты:</b> {self._format_scores(soft_skills_scores)}"
        story.append(Paragraph(soft_results, styles['Body']))
        story.append(Spacer(1, 3 * mm))

        if 'soft_skills' in chart_paths:
            self._add_chart_to_story(story, chart_paths['soft_skills'], styles)

        if 'soft_skills' in ai_interpretations:
            story.append(Paragraph("<b>Интерпретация:</b>", styles['SubTitle']))
            story.append(Paragraph(ai_interpretations['soft_skills'], styles['Body']))

        story.append(Spacer(1, 4 * mm))

        # === 3. ТЕСТ HEXACO - ЛИЧНОСТНЫЕ ЧЕРТЫ ===
        story.append(Paragraph("3. ТЕСТ HEXACO - МОДЕЛЬ ЛИЧНОСТИ", styles['SectionTitle']))

        test_description = "HEXACO - современная шестифакторная модель личности (10 вопросов по 5-балльной шкале)."
        story.append(Paragraph(test_description, styles['Body']))
        story.append(Spacer(1, 3 * mm))

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
        story.append(Spacer(1, 5 * mm))

        hexaco_results = f"<b>Результаты:</b> {self._format_scores(hexaco_scores)}"
        story.append(Paragraph(hexaco_results, styles['Body']))
        story.append(Spacer(1, 3 * mm))

        if 'hexaco' in chart_paths:
            self._add_chart_to_story(story, chart_paths['hexaco'], styles)

        if 'hexaco' in ai_interpretations:
            story.append(Paragraph("<b>Интерпретация:</b>", styles['SubTitle']))
            story.append(Paragraph(ai_interpretations['hexaco'], styles['Body']))
        story.append(Spacer(1, 4 * mm))

        # === 4. ТЕСТ DISC - ПОВЕДЕНЧЕСКИЕ СТИЛИ ===
        story.append(Paragraph("4. ТЕСТ DISC - МОДЕЛЬ ПОВЕДЕНИЯ", styles['SectionTitle']))

        test_description = "DISC - методика оценки поведенческих особенностей и стилей (8 вопросов по 4 типам)."
        story.append(Paragraph(test_description, styles['Body']))
        story.append(Spacer(1, 3 * mm))

        disc_description = """
        <b>DISC</b> - методика оценки поведенческих особенностей и стилей общения:<br/>
        • <b>D (Dominance)</b> - доминирование, прямота, решительность, ориентация на результат<br/>
        • <b>I (Influence)</b> - влияние, общительность, оптимизм, ориентация на людей<br/>
        • <b>S (Steadiness)</b> - постоянство, терпение, командная работа, стабильность<br/>
        • <b>C (Compliance)</b> - соответствие стандартам, аналитичность, точность, осторожность
        """
        story.append(Paragraph(disc_description, styles['Body']))
        story.append(Spacer(1, 5 * mm))

        disc_results = f"<b>Результаты:</b> {self._format_scores(disc_scores)}"
        story.append(Paragraph(disc_results, styles['Body']))
        story.append(Spacer(1, 3 * mm))

        if 'disc' in chart_paths:
            self._add_chart_to_story(story, chart_paths['disc'], styles)

        if 'disc' in ai_interpretations:
            story.append(Paragraph("<b>Интерпретация:</b>", styles['SubTitle']))
            story.append(Paragraph(ai_interpretations['disc'], styles['Body']))
        story.append(Spacer(1, 4 * mm))

        return story

    def generate_enhanced_report(self, 
                               participant_name: str,
                               test_date: str,
                               paei_scores: Dict[str, float],
                               disc_scores: Dict[str, float], 
                               hexaco_scores: Dict[str, float],
                               soft_skills_scores: Dict[str, float],
                               ai_interpretations: Optional[Dict[str, str]],
                               out_path: Path) -> Tuple[Path, Optional[str]]:
        """Генерирует улучшенный PDF отчёт с детальными описаниями"""
        prepared_interpretations = dict(ai_interpretations or {})
        expected_keys = {'paei', 'disc', 'hexaco', 'soft_skills'}
        missing_keys = expected_keys - set(prepared_interpretations)
        if missing_keys:
            generated = self._generate_dynamic_interpretations(
                paei_scores, disc_scores, hexaco_scores, soft_skills_scores
            )
            prepared_interpretations = {**generated, **prepared_interpretations}

        chart_paths = self._create_all_charts(
            paei_scores,
            disc_scores,
            hexaco_scores,
            soft_skills_scores,
        )

        story = self._build_story(
            participant_name,
            test_date,
            paei_scores,
            disc_scores,
            hexaco_scores,
            soft_skills_scores,
            prepared_interpretations,
            chart_paths,
        )

        total_pages = self._count_story_pages(story)
        doc = self._create_doc_template(str(out_path))

        def _draw_page(canvas_obj, _doc):
            self._draw_page_number(canvas_obj, total_pages)

        doc.build(story, onFirstPage=_draw_page, onLaterPages=_draw_page)
        return out_path, None
    
    def _create_all_charts(self, paei_scores: Dict, disc_scores: Dict, 
                         hexaco_scores: Dict, soft_skills_scores: Dict) -> Dict[str, Path]:
        """Создаёт все радарные диаграммы для отчета"""
        charts = {}
        
        # PAEI диаграмма (комбинированная - столбиковая + круговая)
        paei_labels = list(paei_scores.keys())
        paei_values = list(paei_scores.values())
        paei_path = self.template_dir / "paei_combined.png"
        EnhancedCharts.create_paei_combined_chart(paei_labels, paei_values, 
                                                "PAEI (Адизес) - Управленческие роли", paei_path)
        charts['paei'] = paei_path
        
        # Soft Skills диаграмма (радарная)
        # Жёстко задаём порядок и названия soft skills для диаграммы, чтобы совпадало с skills_mapping
        soft_labels = [
            "Коммуникация",
            "Работа в команде",
            "Лидерство",
            "Критическое мышление",
            "Управление временем",
            "Стрессоустойчивость",
            "Эмоциональный интеллект",
            "Адаптивность",
            "Решение проблем",
            "Креативность"
        ]
        soft_values = list(soft_skills_scores.values())
        soft_radar_path = self.template_dir / "soft_skills_radar.png"
        EnhancedCharts.create_minimalist_radar(soft_labels, soft_values,
                                             "Soft Skills", soft_radar_path)
        charts['soft_skills'] = soft_radar_path
        
        # HEXACO диаграмма (радарная с расшифровками)
        hexaco_labels = list(hexaco_scores.keys())
        hexaco_values = list(hexaco_scores.values())
        hexaco_path = self.template_dir / "hexaco_radar.png"
        EnhancedCharts.create_hexaco_radar(hexaco_labels, hexaco_values,
                                         "HEXACO", hexaco_path)
        charts['hexaco'] = hexaco_path
        
        # DISC диаграмма (комбинированная - столбиковая + круговая)  
        disc_labels = list(disc_scores.keys())
        disc_values = list(disc_scores.values())
        disc_path = self.template_dir / "disc_combined.png"
        EnhancedCharts.create_disc_combined_chart(disc_labels, disc_values,
                                                "DISC - Поведенческие стили", disc_path)
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
            fontSize=12,  # уменьшенный шрифт
            fontName=DesignConfig.TITLE_FONT,
            textColor=DesignConfig.PRIMARY_COLOR,
            alignment=1,  # CENTER
            spaceAfter=1,
            spaceBefore=1,
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
    
    def upload_to_google_drive(self, file_path: Path, participant_name: Optional[str] = None) -> Optional[str]:
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
        pdf_result = self.generate_enhanced_report(
            participant_name, test_date, paei_scores, disc_scores,
            hexaco_scores, soft_skills_scores, ai_interpretations, out_path
        )
        
        # Распаковываем результат
        pdf_path, existing_gdrive_link = pdf_result
        
        # Загружаем в Google Drive если нужно и еще не загружен
        gdrive_link = existing_gdrive_link
        if upload_to_gdrive and not existing_gdrive_link:
            gdrive_link = self.upload_to_google_drive(pdf_path, participant_name)
        
        return pdf_path, gdrive_link
