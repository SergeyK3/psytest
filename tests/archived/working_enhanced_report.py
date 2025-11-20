#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Рабочий enhanced отчет с упрощенной логикой
"""

from pathlib import Path
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def setup_fonts():
    """Настройка шрифтов с кириллицей"""
    try:
        windows_fonts = "C:/Windows/Fonts/"
        font_candidates = [
            ("arial.ttf", "Arial-Regular"),
            ("arialbd.ttf", "Arial-Bold"),
        ]
        
        for font_file, font_name in font_candidates:
            font_path = os.path.join(windows_fonts, font_file)
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    print(f"✅ Зарегистрирован: {font_name}")
                except Exception as e:
                    print(f"⚠️ Ошибка регистрации {font_name}: {e}")
    except Exception as e:
        print(f"⚠️ Ошибка настройки шрифтов: {e}")

def create_working_enhanced_report():
    """Создает рабочий enhanced отчет"""
    
    print("🚀 СОЗДАНИЕ РАБОЧЕГО ENHANCED ОТЧЕТА")
    print("=" * 50)
    
    # Настройка шрифтов
    setup_fonts()
    
    # Данные для отчета
    participant_name = "Тестовый Пользователь Enhanced"
    test_date = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"working_enhanced_{timestamp}.pdf"
    
    print(f"📄 Создание: {filename}")
    print(f"👤 Участник: {participant_name}")
    print(f"📅 Дата: {test_date}")
    
    # Создаем документ
    doc = SimpleDocTemplate(filename, pagesize=A4,
                          rightMargin=20*mm, leftMargin=20*mm,
                          topMargin=25*mm, bottomMargin=20*mm)
    
    # Стили
    styles = getSampleStyleSheet()
    
    # Добавляем кастомные стили
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=16,
        fontName='Arial-Bold' if 'Arial-Bold' in [f.fontName for f in pdfmetrics.getRegisteredFontNames()] else 'Times-Bold',
        textColor=Color(0.18, 0.25, 0.34),
        alignment=1,
        spaceAfter=8
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=12,
        fontName='Arial-Bold' if 'Arial-Bold' in [f.fontName for f in pdfmetrics.getRegisteredFontNames()] else 'Times-Bold',
        textColor=Color(0.18, 0.25, 0.34),
        spaceBefore=6,
        spaceAfter=3
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Arial-Regular' if 'Arial-Regular' in [f.fontName for f in pdfmetrics.getRegisteredFontNames()] else 'Times-Roman',
        spaceBefore=2,
        spaceAfter=2
    )
    
    # Создаем содержимое
    story = []
    
    # === ТИТУЛЬНАЯ СТРАНИЦА ===
    story.append(Paragraph("ОЦЕНКА КОМАНДНЫХ НАВЫКОВ", title_style))
    story.append(Spacer(1, 8*mm))
    
    # Информация о тестируемом
    info_data = [
        ['Имя сотрудника:', participant_name],
        ['Дата тестирования:', test_date],
    ]
    
    info_table = Table(info_data, colWidths=[50*mm, 80*mm])
    info_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Arial-Regular', 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (0, -1), Color(0.18, 0.25, 0.34)),
        ('FONTNAME', (0, 0), (0, -1), 'Arial-Bold'),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 15*mm))
    
    # === ОБЩЕЕ ЗАКЛЮЧЕНИЕ ===
    story.append(Paragraph("ОБЩЕЕ ЗАКЛЮЧЕНИЕ И РЕКОМЕНДАЦИИ", section_style))
    story.append(Spacer(1, 5*mm))
    
    conclusion_text = f"""
    На основе комплексного психологического тестирования сотрудника <b>{participant_name}</b> 
    проведен анализ управленческого потенциала, личностных особенностей, поведенческих стилей 
    и профессиональных компетенций. Результаты позволяют составить целостное представление 
    о профессиональном профиле и потенциале развития.
    """
    story.append(Paragraph(conclusion_text, body_style))
    story.append(Spacer(1, 10*mm))
    
    # === 1. ТЕСТ АДИЗЕСА (PAEI) ===
    story.append(Paragraph("1. ТЕСТ АДИЗЕСА (PAEI) - УПРАВЛЕНЧЕСКИЕ РОЛИ", section_style))
    story.append(Spacer(1, 5*mm))
    
    paei_description = """
    <b>Тест Адизеса (PAEI)</b> - оценка управленческих ролей и стилей руководства:<br/><br/>
    • <b>P (Producer - Производитель)</b> - ориентация на результат, выполнение задач<br/>
    • <b>A (Administrator - Администратор)</b> - организация процессов, контроль<br/>
    • <b>E (Entrepreneur - Предприниматель)</b> - инновации, стратегическое мышление<br/>
    • <b>I (Integrator - Интегратор)</b> - командная работа, мотивация людей<br/><br/>
    <b>Результаты:</b> P: 8, A: 6, E: 9, I: 7<br/>
    <b>Доминирующая роль:</b> Предприниматель (E) - 9 баллов
    """
    story.append(Paragraph(paei_description, body_style))
    story.append(Spacer(1, 8*mm))
    
    # === 2. SOFT SKILLS ===
    story.append(Paragraph("2. ОЦЕНКА SOFT SKILLS - НАДПРОФЕССИОНАЛЬНЫЕ КОМПЕТЕНЦИИ", section_style))
    story.append(Spacer(1, 5*mm))
    
    soft_description = """
    <b>Soft Skills</b> - надпрофессиональные навыки для решения жизненных и рабочих задач:<br/><br/>
    <b>Результаты:</b><br/>
    • Лидерство: 8 баллов<br/>
    • Коммуникация: 9 баллов<br/>
    • Креативность: 7 баллов<br/>
    • Аналитика: 6 баллов<br/>
    • Адаптивность: 8 баллов<br/>
    • Командная работа: 9 баллов<br/>
    • Эмпатия: 8 баллов<br/>
    • Критическое мышление: 7 баллов<br/>
    • Управление временем: 6 баллов<br/>
    • Решение проблем: 8 баллов<br/><br/>
    <b>Сильные стороны:</b> Коммуникация и командная работа (9 баллов)
    """
    story.append(Paragraph(soft_description, body_style))
    story.append(Spacer(1, 8*mm))
    
    # === 3. HEXACO ===
    story.append(Paragraph("3. HEXACO - ШЕСТИФАКТОРНАЯ МОДЕЛЬ ЛИЧНОСТИ", section_style))
    story.append(Spacer(1, 5*mm))
    
    hexaco_description = """
    <b>HEXACO</b> - современная модель личности из 6 факторов:<br/><br/>
    • <b>H (Honesty-Humility)</b> - честность, скромность: 4 балла<br/>
    • <b>E (Emotionality)</b> - эмоциональность, чувствительность: 3 балла<br/>
    • <b>X (eXtraversion)</b> - экстраверсия, общительность: 5 баллов<br/>
    • <b>A (Agreeableness)</b> - доброжелательность, сотрудничество: 4 балла<br/>
    • <b>C (Conscientiousness)</b> - добросовестность, организованность: 5 баллов<br/>
    • <b>O (Openness)</b> - открытость опыту, креативность: 4 балла<br/><br/>
    <b>Профиль:</b> Сбалансированная личность с выраженной экстраверсией и добросовестностью
    """
    story.append(Paragraph(hexaco_description, body_style))
    story.append(Spacer(1, 8*mm))
    
    # === 4. DISC ===
    story.append(Paragraph("4. DISC - ПОВЕДЕНЧЕСКИЕ СТИЛИ", section_style))
    story.append(Spacer(1, 5*mm))
    
    disc_description = """
    <b>DISC</b> - методика оценки поведенческих стилей:<br/><br/>
    • <b>D (Dominance)</b> - доминирование, решительность: 7 баллов<br/>
    • <b>I (Influence)</b> - влияние, общительность: 8 баллов<br/>
    • <b>S (Steadiness)</b> - постоянство, стабильность: 5 баллов<br/>
    • <b>C (Compliance)</b> - соответствие, аналитичность: 6 баллов<br/><br/>
    <b>Доминирующий стиль:</b> Влияние (I) - 8 баллов<br/>
    Характеризуется высокой общительностью и способностью воздействовать на других
    """
    story.append(Paragraph(disc_description, body_style))
    story.append(Spacer(1, 10*mm))
    
    # === ИТОГОВЫЕ РЕКОМЕНДАЦИИ ===
    story.append(Paragraph("ИТОГОВЫЕ РЕКОМЕНДАЦИИ", section_style))
    story.append(Spacer(1, 5*mm))
    
    recommendations = """
    <b>Профессиональные рекомендации:</b><br/><br/>
    
    <b>1. Использование сильных сторон:</b><br/>
    • Развивать предпринимательские качества в рамках текущей роли<br/>
    • Использовать коммуникативные навыки для влияния на команду<br/>
    • Применять способности к командной работе в проектах<br/><br/>
    
    <b>2. Области для развития:</b><br/>
    • Усилить административные навыки для лучшего контроля процессов<br/>
    • Развивать аналитические способности для принятия решений<br/>
    • Улучшить навыки управления временем<br/><br/>
    
    <b>3. Карьерные перспективы:</b><br/>
    • Рассмотреть руководящие позиции с акцентом на инновации<br/>
    • Развивать экспертизу в области командного лидерства<br/>
    • Участвовать в стратегических проектах компании
    """
    story.append(Paragraph(recommendations, body_style))
    
    print(f"✅ Подготовлено {len(story)} элементов контента")
    
    # Строим PDF
    try:
        doc.build(story)
        
        # Проверяем результат
        file_path = Path(filename)
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ PDF создан: {filename}")
            print(f"📊 Размер: {size} байт ({size/1024:.1f} KB)")
            
            if size > 10000:
                print("✅ Размер соответствует полному отчету!")
                
                # Пробуем загрузить в Google Drive
                try:
                    from oauth_google_drive import upload_to_google_drive_oauth
                    print("\n📤 Загрузка в Google Drive...")
                    
                    gdrive_link = upload_to_google_drive_oauth(
                        file_path=filename,
                        folder_name="PsychTest Reports",
                        use_monthly_structure=True
                    )
                    
                    if gdrive_link:
                        print(f"✅ Google Drive: {gdrive_link}")
                    else:
                        print("⚠️ Загрузка в Google Drive не удалась")
                        
                except ImportError:
                    print("⚠️ Google Drive интеграция недоступна")
                except Exception as e:
                    print(f"⚠️ Ошибка Google Drive: {e}")
                    
            else:
                print("⚠️ Размер меньше ожидаемого")
                
            return filename
        else:
            print("❌ Файл не создан")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка создания PDF: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    create_working_enhanced_report()