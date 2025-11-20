#!/usr/bin/env python3
"""
Тест автоматической загрузки PDF в Google Drive
"""

from enhanced_pdf_report_v2 import EnhancedPDFReportV2

def test_auto_gdrive_upload():
    """Тест автоматической загрузки в Google Drive"""
    print("🚀 ТЕСТ АВТОМАТИЧЕСКОЙ ЗАГРУЗКИ В GOOGLE DRIVE")
    print("=" * 60)
    
    # Создаем генератор отчетов
    report_generator = EnhancedPDFReportV2()
    
    # Тестовые данные
    participant_name = "ТЕСТ АВТОЗАГРУЗКИ"
    
    paei_scores = {
        "Предприниматель (E)": 85,
        "Администратор (A)": 75,
        "Производитель (P)": 90,
        "Интегратор (I)": 70
    }
    
    disc_scores = {
        "Доминирование (D)": 80,
        "Влияние (I)": 75,
        "Постоянство (S)": 70,
        "Соответствие (C)": 85
    }
    
    hexaco_scores = {
        "Честность": 85,
        "Эмоциональность": 60,
        "Экстраверсия": 75,
        "Доброжелательность": 80,
        "Добросовестность": 90,
        "Открытость опыту": 70
    }
    
    soft_skills_scores = {
        "Коммуникация": 85,
        "Лидерство": 80,
        "Командная работа": 75,
        "Адаптивность": 70,
        "Решение проблем": 90
    }
    
    print(f"👤 Участник: {participant_name}")
    print("📄 Генерация PDF с автоматической загрузкой...")
    
    # Дополнительные параметры
    from datetime import datetime
    from pathlib import Path
    
    test_date = datetime.now().strftime("%Y-%m-%d")
    ai_interpretations = {
        'paei': 'Высокие результаты по всем показателям PAEI.',
        'disc': 'Сбалансированный профиль DISC.',
        'hexaco': 'Отличные показатели честности и добросовестности.',
        'soft_skills': 'Сильные навыки решения проблем.'
    }
    out_path = Path(f"auto_gdrive_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    # Генерируем отчет (должен автоматически загрузиться в Google Drive)
    pdf_path = report_generator.generate_enhanced_report(
        participant_name=participant_name,
        test_date=test_date,
        paei_scores=paei_scores,
        disc_scores=disc_scores,
        hexaco_scores=hexaco_scores,
        soft_skills_scores=soft_skills_scores,
        ai_interpretations=ai_interpretations,
        out_path=out_path
    )
    
    print(f"📄 Локальный файл: {pdf_path}")
    print("\n✅ ТЕСТ ЗАВЕРШЕН!")
    print("📤 PDF должен был автоматически загрузиться в Google Drive")

if __name__ == "__main__":
    test_auto_gdrive_upload()