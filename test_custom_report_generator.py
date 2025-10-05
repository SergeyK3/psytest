#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест удобной функции создания психологических отчетов с Google Drive
"""

from final_full_numbered_generator import create_psychological_report

def test_custom_report():
    """Тестирует создание отчета с настраиваемыми параметрами"""
    
    print("🧪 Тест создания персонального отчета...")
    
    # Создаем отчет с настраиваемыми данными
    file_path, gdrive_link = create_psychological_report(
        participant_name="Анна Тестовая",
        paei_scores={"P": 9, "A": 6, "E": 8, "I": 7},
        disc_scores={"D": 7, "I": 9, "S": 5, "C": 6},
        hexaco_scores={"H": 4, "E": 3, "X": 5, "A": 4, "C": 5, "O": 4},
        soft_skills_scores={
            "Лидерство": 9, "Коммуникация": 10, "Креативность": 8, "Аналитика": 7,
            "Адаптивность": 9, "Командная работа": 8, "Эмпатия": 9, 
            "Критическое мышление": 7, "Управление временем": 8, "Решение проблем": 8
        },
        upload_to_google_drive=True
    )
    
    print(f"✅ Локальный файл: {file_path}")
    if gdrive_link:
        print(f"✅ Google Drive: {gdrive_link}")
    else:
        print("⚠️ Google Drive: загрузка не выполнена")

if __name__ == "__main__":
    test_custom_report()