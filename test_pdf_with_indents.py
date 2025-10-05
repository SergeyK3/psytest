#!/usr/bin/env python3
"""
Сценарий для тестирования генерации PDF с правильными отступами
и загрузки в Google Drive для проверки внешнего вида
"""

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from pathlib import Path
import datetime


def create_test_pdf_with_google_drive():
    """Создаёт тестовый PDF с отступами и загружает в Google Drive"""
    
    print("🎯 Создание тестового PDF с исправленными отступами")
    print("=" * 60)
    
    # Тестовые данные для демонстрации отступов
    test_data = {
        'paei_scores': {
            'P': 4.5,  # Производитель - доминирующая роль
            'A': 3.2,  # Администратор
            'E': 3.8,  # Предприниматель  
            'I': 3.1   # Интегратор
        },
        'disc_scores': {
            'D': 7,    # Доминирование - высокий
            'I': 5,    # Влияние
            'S': 3,    # Устойчивость
            'C': 6     # Подчинение правилам
        },
        'hexaco_scores': {
            'H': 3.9,  # Честность-Скромность
            'E': 4.1,  # Эмоциональность
            'X': 4.3,  # Экстраверсия - доминирующая
            'A': 3.7,  # Доброжелательность
            'C': 4.0,  # Добросовестность
            'O': 3.8   # Открытость
        },
        'soft_skills_scores': {
            'Коммуникация': 8.5,            # Высокий уровень
            'Лидерство': 9.0,               # Доминирующий навык
            'Критическое мышление': 7.8,    
            'Креативность': 7.2,
            'Работа в команде': 8.1,
            'Адаптивность': 7.5,
            'Эмоциональный интеллект': 8.3,
            'Решение проблем': 8.7,
            'Управление временем': 7.9,
            'Презентационные навыки': 8.0
        },
        'ai_interpretations': {
            'paei': """
            Ярко выраженный тип Производитель (P=4.5) с сильной ориентацией на результат. 
            Характеризуется высокой эффективностью в выполнении задач, стремлением к достижению 
            конкретных целей и способностью работать в условиях дедлайнов. Хорошо развиты 
            предпринимательские качества (E=3.8), что позволяет сочетать выполнение текущих 
            задач с поиском новых возможностей.
            """,
            'disc': """
            Доминирующий поведенческий стиль (D=7) указывает на решительность, прямолинейность 
            и ориентацию на результат. Высокие показатели по Подчинению правилам (C=6) создают 
            сбалансированный профиль лидера, который сочетает напористость с вниманием к деталям 
            и качеству. Такой тип эффективен в управленческих позициях, требующих быстрых решений.
            """,
            'hexaco': """
            Экстравертированная личность (X=4.3) с высокой социальной активностью и энергичностью. 
            Сбалансированные показатели по другим факторам указывают на адаптивность и способность 
            эффективно взаимодействовать в различных ситуациях. Умеренная эмоциональность (E=4.1) 
            способствует стрессоустойчивости в руководящих позициях.
            """,
            'soft_skills': """
            Выдающиеся лидерские качества (9.0 баллов) подкреплены сильными коммуникативными 
            навыками (8.5) и способностью решать проблемы (8.7). Высокий эмоциональный интеллект 
            (8.3) позволяет эффективно управлять командой и мотивировать сотрудников. Профиль 
            указывает на готовность к руководящим позициям высокого уровня.
            """
        }
    }
    
    # Генерируем уникальное имя файла
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_indents_report_{timestamp}.pdf"
    output_path = Path(filename)
    
    print(f"📄 Создание PDF: {filename}")
    print(f"📊 Тестовые данные:")
    print(f"   • PAEI: Производитель (P={test_data['paei_scores']['P']})")
    print(f"   • DISC: Доминирование (D={test_data['disc_scores']['D']})")
    print(f"   • HEXACO: Экстраверсия (X={test_data['hexaco_scores']['X']})")
    print(f"   • Soft Skills: Лидерство ({test_data['soft_skills_scores']['Лидерство']} баллов)")
    print()
    
    try:
        # Создаём генератор отчетов
        generator = EnhancedPDFReportV2()
        
        # Генерируем PDF с отступами
        print("🔄 Генерация PDF с исправленными отступами...")
        result_path = generator.generate_enhanced_report(
            participant_name='Тест Отступов',
            test_date='2025-10-04',
            paei_scores=test_data['paei_scores'],
            disc_scores=test_data['disc_scores'],
            hexaco_scores=test_data['hexaco_scores'],
            soft_skills_scores=test_data['soft_skills_scores'],
            ai_interpretations=test_data['ai_interpretations'],
            out_path=output_path
        )
        
        print(f"✅ PDF создан: {result_path}")
        
        # Загружаем в Google Drive
        print("🔄 Загрузка в Google Drive...")
        drive_url = generator.generate_enhanced_report_with_gdrive(
            participant_name='Тест Отступов',
            test_date='2025-10-04',
            paei_scores=test_data['paei_scores'],
            disc_scores=test_data['disc_scores'],
            hexaco_scores=test_data['hexaco_scores'],
            soft_skills_scores=test_data['soft_skills_scores'],
            ai_interpretations=test_data['ai_interpretations'],
            out_path=output_path
        )
        
        print("🎉 УСПЕШНО ЗАВЕРШЕНО!")
        print("=" * 60)
        print(f"📁 Локальный файл: {result_path.absolute()}")
        print(f"☁️  Google Drive: {drive_url}")
        print()
        print("🔍 ЧТО ПРОВЕРИТЬ В PDF:")
        print("   1. Рекомендации по профессиональному развитию:")
        print("      • Делегировать задачи... (с отступом)")
        print("      • Развивать лидерство... (с отступом)")
        print("      • Использовать доминирование... (с отступом)")
        print()
        print("   2. Ключевые характеристики профиля:")
        print("      • Управленческий стиль... (с отступом)")
        print("      • Поведенческий тип DISC... (с отступом)")
        print()
        print("   3. Использованные методики:")
        print("      • Тест Адизеса (PAEI)... (с отступом)")
        print("      • Оценка Soft Skills... (с отступом)")
        print()
        print("   4. Расшифровки PAEI, HEXACO, DISC:")
        print("      • Все пункты должны иметь отступы")
        
        return result_path, drive_url
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None, None


if __name__ == "__main__":
    create_test_pdf_with_google_drive()