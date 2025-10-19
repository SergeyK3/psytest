#!/usr/bin/env python3
"""
Демонстрация нового функционала:
- Отчет для пользователя: БЕЗ раздела вопросов
- Отчет для Google Drive: С разделом вопросов и ответов
"""

import os
from datetime import datetime
from pathlib import Path
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from bot_integration_example import UserAnswersCollector

def demo_dual_reports():
    """Демонстрация генерации двух разных отчетов"""
    
    print("🎯 Демонстрация нового функционала: два типа отчетов")
    print("=" * 60)
    
    # Тестовые данные
    participant_name = "Демо Пользователь"
    test_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Тестовые результаты
    paei_scores = {"P": 8, "A": 6, "E": 7, "I": 5}
    disc_scores = {"D": 8, "I": 6, "S": 5, "C": 7}
    hexaco_scores = {"H": 4.2, "E": 3.8, "X": 4.5, "A": 4.1, "C": 3.9, "O": 4.3}
    soft_skills_scores = {
        "Коммуникация": 8, "Лидерство": 7, "Работа в команде": 9,
        "Решение проблем": 6, "Адаптивность": 8, "Креативность": 7,
        "Эмоциональный интеллект": 8, "Управление временем": 6,
        "Критическое мышление": 7, "Стрессоустойчивость": 8
    }
    
    # Тестовые интерпретации
    ai_interpretations = {
        "paei": "Демо интерпретация PAEI методики.",
        "disc": "Демо интерпретация DISC профиля.",
        "hexaco": "Демо интерпретация личностных черт HEXACO.",
        "soft_skills": "Демо интерпретация мягких навыков."
    }
    
    # Создаем коллектор ответов с тестовыми данными
    answers_collector = UserAnswersCollector()
    
    # Добавляем тестовые ответы используя специфичные методы
    answers_collector.add_paei_answer(0, "4 - Полностью согласен")
    answers_collector.add_paei_answer(1, "3 - Скорее согласен")
    answers_collector.add_disc_answer(0, 4)
    answers_collector.add_disc_answer(1, 3)
    answers_collector.add_soft_skills_answer(0, 4)
    answers_collector.add_hexaco_answer(0, 4)
    
    user_answers = answers_collector.get_answers_dict()
    
    # Создаем папки
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    temp_charts_dir = Path("temp_charts")
    temp_charts_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Пути для отчетов
    pdf_path_user = docs_dir / f"{timestamp}_demo_user_report.pdf"
    pdf_path_gdrive = docs_dir / f"{timestamp}_demo_full_report.pdf"
    
    print(f"📄 Генерация отчета для пользователя: {pdf_path_user.name}")
    print("   ├─ Раздел вопросов: ❌ ОТКЛЮЧЕН")
    print("   └─ Назначение: Отправка пользователю в Telegram")
    
    # 1. Генерируем отчет БЕЗ вопросов (для пользователя)
    pdf_generator_user = EnhancedPDFReportV2(
        template_dir=temp_charts_dir,
        include_questions_section=False  # БЕЗ вопросов
    )
    
    pdf_generator_user.generate_enhanced_report(
        participant_name=participant_name,
        test_date=test_date,
        paei_scores=paei_scores,
        disc_scores=disc_scores,
        hexaco_scores=hexaco_scores,
        soft_skills_scores=soft_skills_scores,
        ai_interpretations=ai_interpretations,
        out_path=pdf_path_user,
        user_answers=None  # Не передаем ответы
    )
    
    print(f"✅ Пользовательский отчет сохранен: {pdf_path_user}")
    
    print(f"\n📄 Генерация отчета для Google Drive: {pdf_path_gdrive.name}")
    print("   ├─ Раздел вопросов: ✅ ВКЛЮЧЕН")  
    print("   ├─ Детализация ответов: ✅ ВКЛЮЧЕНА")
    print("   └─ Назначение: Загрузка в Google Drive для специалиста")
    
    # 2. Генерируем отчет С вопросами (для Google Drive)
    pdf_generator_gdrive = EnhancedPDFReportV2(
        template_dir=temp_charts_dir,
        include_questions_section=True   # С вопросами
    )
    
    pdf_generator_gdrive.generate_enhanced_report(
        participant_name=participant_name,
        test_date=test_date,
        paei_scores=paei_scores,
        disc_scores=disc_scores,
        hexaco_scores=hexaco_scores,
        soft_skills_scores=soft_skills_scores,
        ai_interpretations=ai_interpretations,
        out_path=pdf_path_gdrive,
        user_answers=user_answers  # Передаем детальные ответы
    )
    
    print(f"✅ Полный отчет сохранен: {pdf_path_gdrive}")
    
    print("\n" + "=" * 60)
    print("🎯 РЕЗУЛЬТАТ:")
    print(f"📱 Пользователю в Telegram: {pdf_path_user} (краткий)")
    print(f"☁️  Специалисту в Google Drive: {pdf_path_gdrive} (полный)")
    print("\n💡 Теперь пользователи получают лаконичные отчеты,")
    print("   а специалисты - детальные с анализом каждого ответа!")

if __name__ == "__main__":
    demo_dual_reports()