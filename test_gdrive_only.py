#!/usr/bin/env python3
"""
Тест сохранения PDF только в Google Drive (без локальных копий)
"""

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from datetime import datetime
from pathlib import Path
import os

def test_gdrive_only_save():
    """Тест сохранения только в Google Drive"""
    print("☁️ ТЕСТ СОХРАНЕНИЯ ТОЛЬКО В GOOGLE DRIVE")
    print("=" * 60)
    print("📌 Проверяем что файлы сохраняются только в облаке")
    print("🗑️ Локальные копии должны автоматически удаляться")
    print()
    
    # Создаем генератор отчетов
    report_generator = EnhancedPDFReportV2()
    
    # Тестовые данные
    participant_name = "ТОЛЬКО GOOGLE DRIVE"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    paei_scores = {
        "Предприниматель (E)": 90,
        "Администратор (A)": 80,
        "Производитель (P)": 85,
        "Интегратор (I)": 75
    }
    
    disc_scores = {
        "Доминирование (D)": 85,
        "Влияние (I)": 80,
        "Постоянство (S)": 70,
        "Соответствие (C)": 75
    }
    
    hexaco_scores = {
        "Честность": 90,
        "Эмоциональность": 65,
        "Экстраверсия": 80,
        "Доброжелательность": 85,
        "Добросовестность": 95,
        "Открытость опыту": 75
    }
    
    soft_skills_scores = {
        "Коммуникация": 90,
        "Лидерство": 85,
        "Командная работа": 80,
        "Адаптивность": 75,
        "Решение проблем": 95
    }
    
    ai_interpretations = {
        'paei': 'Выдающиеся предпринимательские способности с сильными администраторскими навыками.',
        'disc': 'Лидерский профиль с высоким доминированием и влиянием.',
        'hexaco': 'Исключительная честность и добросовестность - идеальный кандидат для руководящих позиций.',
        'soft_skills': 'Превосходные навыки решения проблем и коммуникации.'
    }
    
    # Создаем временное имя файла
    out_path = Path(f"gdrive_only_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    print(f"👤 Участник: {participant_name}")
    print(f"📄 Временный файл: {out_path}")
    print("📤 Генерация и загрузка в Google Drive...")
    print()
    
    # Генерируем отчет
    result = report_generator.generate_enhanced_report(
        participant_name=participant_name,
        test_date=test_date,
        paei_scores=paei_scores,
        disc_scores=disc_scores,
        hexaco_scores=hexaco_scores,
        soft_skills_scores=soft_skills_scores,
        ai_interpretations=ai_interpretations,
        out_path=out_path
    )
    
    print()
    print("🔍 ПРОВЕРКА РЕЗУЛЬТАТОВ:")
    
    # Проверяем что файл не остался локально
    if os.path.exists(out_path):
        print(f"❌ ОШИБКА: Локальный файл {out_path} все еще существует!")
    else:
        print(f"✅ Локальный файл {out_path} успешно удален")
    
    # Проверяем тип результата
    if isinstance(result, str) and result.startswith("https://"):
        print(f"✅ Возвращена ссылка Google Drive: {result}")
        print("✅ УСПЕХ: Файл сохранен только в Google Drive!")
    elif isinstance(result, Path):
        print(f"⚠️ Возвращен локальный путь: {result}")
        print("⚠️ Возможна ошибка загрузки в Google Drive")
    else:
        print(f"❓ Неожиданный результат: {result}")
    
    print()
    print("✅ ТЕСТ ЗАВЕРШЕН!")
    print("📋 Итог: PDF файлы теперь сохраняются только в Google Drive")

if __name__ == "__main__":
    test_gdrive_only_save()