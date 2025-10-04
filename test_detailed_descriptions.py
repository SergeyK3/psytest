#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест для проверки генерации детальных описаний в PDF отчете
на основе примеров из промптов _res.txt
"""

from pathlib import Path
from datetime import datetime
from enhanced_pdf_report_v2 import EnhancedPDFReportV2

def test_detailed_descriptions():
    """Тестирует генерацию PDF с детальными описаниями"""
    
    # Тестовые данные для всех тестов
    test_data = {
        "participant_name": "Иванов Иван Иванович",
        "test_date": datetime.now().strftime("%d.%m.%Y"),
        
        # PAEI данные (5-балльная шкала)
        "paei_scores": {
            "P": 4,  # Производитель
            "A": 2,  # Администратор
            "E": 5,  # Предприниматель
            "I": 3   # Интегратор
        },
        
        # DISC данные (сумма баллов по 2 вопроса = максимум 10)
        "disc_scores": {
            "D": 7,  # Доминирование
            "I": 5,  # Влияние
            "S": 3,  # Постоянство
            "C": 6   # Соответствие
        },
        
        # HEXACO данные (5-балльная шкала)
        "hexaco_scores": {
            "H": 4.2,  # Честность-Скромность
            "E": 3.1,  # Эмоциональность
            "X": 4.8,  # Экстраверсия
            "A": 3.5,  # Доброжелательность
            "C": 4.1,  # Добросовестность
            "O": 2.8   # Открытость опыту
        },
        
        # Soft Skills данные (10-балльная шкала)
        "soft_skills_scores": {
            "Лидерство": 7,
            "Эмоциональный интеллект": 8,
            "Коммуникация": 6,
            "Критическое мышление": 4,
            "Управление временем": 7,
            "Разрешение конфликтов": 8,
            "Адаптивность": 6,
            "Развитие сотрудников": 5
        },
        
        # ИИ интерпретации (для сравнения с детальными описаниями)
        "ai_interpretations": {
            "paei": "ИИ анализ PAEI: Преобладает предпринимательский стиль с акцентом на инновации.",
            "disc": "ИИ анализ DISC: Доминирующий тип с высокой решительностью.",
            "hexaco": "ИИ анализ HEXACO: Сбалансированный профиль с высокой экстраверсией.",
            "soft_skills": "ИИ анализ Soft Skills: Развитые навыки эмоционального интеллекта.",
            "general": "Общие выводы ИИ: Сильный лидерский потенциал с предпринимательским мышлением."
        }
    }
    
    # Создаем генератор отчетов
    pdf_generator = EnhancedPDFReportV2()
    
    # Путь для выходного файла
    output_path = Path("test_detailed_descriptions.pdf")
    
    try:
        print("🔄 Генерация PDF отчета с детальными описаниями...")
        
        # Генерируем отчет
        result_path = pdf_generator.generate_enhanced_report(
            participant_name=test_data["participant_name"],
            test_date=test_data["test_date"],
            paei_scores=test_data["paei_scores"],
            disc_scores=test_data["disc_scores"],
            hexaco_scores=test_data["hexaco_scores"],
            soft_skills_scores=test_data["soft_skills_scores"],
            ai_interpretations=test_data["ai_interpretations"],
            out_path=output_path
        )
        
        if result_path.exists():
            print(f"✅ PDF отчет успешно создан: {result_path}")
            print(f"📄 Размер файла: {result_path.stat().st_size / 1024:.1f} KB")
            
            # Проверяем содержимое детальных описаний
            print("\n📋 Проверка детальных описаний:")
            
            # Тестируем отдельные методы генерации описаний
            test_methods = [
                ("PAEI", test_data["paei_scores"]),
                ("DISC", test_data["disc_scores"]),
                ("HEXACO", test_data["hexaco_scores"]),
                ("SOFT_SKILLS", test_data["soft_skills_scores"])
            ]
            
            for test_type, scores in test_methods:
                description = pdf_generator._generate_detailed_test_description(test_type, scores)
                if description and len(description) > 50:
                    print(f"✅ {test_type}: детальное описание сгенерировано ({len(description)} символов)")
                else:
                    print(f"❌ {test_type}: описание слишком короткое или отсутствует")
            
            print(f"\n🎯 Результат: Отчет с детальными описаниями готов!")
            print(f"📁 Файл сохранен: {result_path.absolute()}")
            
        else:
            print("❌ Ошибка: PDF файл не был создан")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при генерации отчета: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_individual_descriptions():
    """Тестирует отдельные методы генерации описаний"""
    
    print("\n🔍 Тестирование отдельных методов описаний:")
    
    pdf_generator = EnhancedPDFReportV2()
    
    # Тестовые данные
    test_cases = [
        ("PAEI", {"P": 4, "A": 2, "E": 5, "I": 3}),
        ("DISC", {"D": 7, "I": 5, "S": 3, "C": 6}),
        ("HEXACO", {"H": 4.2, "E": 3.1, "X": 4.8, "A": 3.5, "C": 4.1, "O": 2.8}),
        ("SOFT_SKILLS", {"Лидерство": 7, "Эмоциональный интеллект": 8, "Коммуникация": 6})
    ]
    
    for test_type, scores in test_cases:
        try:
            description = pdf_generator._generate_detailed_test_description(test_type, scores)
            print(f"\n--- {test_type} ---")
            print(f"Длина описания: {len(description)} символов")
            print(f"Первые 200 символов: {description[:200]}...")
            
            # Проверяем наличие ключевых элементов
            if test_type == "PAEI":
                if "Производитель" in description and "Предприниматель" in description:
                    print("✅ Содержит правильные термины PAEI")
                else:
                    print("⚠️ Отсутствуют ключевые термины PAEI")
            
            elif test_type == "DISC":
                if "Доминирование" in description and "баллов" in description:
                    print("✅ Содержит правильные термины DISC")
                else:
                    print("⚠️ Отсутствуют ключевые термины DISC")
            
            elif test_type == "HEXACO":
                if "Честность-Скромность" in description and "уровень" in description:
                    print("✅ Содержит правильные термины HEXACO")
                else:
                    print("⚠️ Отсутствуют ключевые термины HEXACO")
            
            elif test_type == "SOFT_SKILLS":
                if "Лидерство" in description and "навык" in description:
                    print("✅ Содержит правильные термины Soft Skills")
                else:
                    print("⚠️ Отсутствуют ключевые термины Soft Skills")
                    
        except Exception as e:
            print(f"❌ Ошибка в тесте {test_type}: {e}")

if __name__ == "__main__":
    print("🚀 Запуск тестирования детальных описаний...")
    
    # Основной тест генерации PDF
    success = test_detailed_descriptions()
    
    # Тест отдельных методов
    test_individual_descriptions()
    
    if success:
        print("\n🎉 Все тесты завершены успешно!")
    else:
        print("\n❌ Обнаружены ошибки в тестах!")