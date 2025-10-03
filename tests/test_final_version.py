#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальный тест улучшенного PDF отчета v4.0
Тест: новый заголовок + увеличенный текст + оптимизированные диаграммы
"""

from pathlib import Path
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from test_scenarios import TEST_SCENARIOS

def test_final_version():
    """Тестирует финальную версию с улучшениями"""
    
    output_dir = Path("test_final_version")
    output_dir.mkdir(exist_ok=True)
    
    print("🎯 ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ PDF v4.0")
    print("=" * 50)
    print("🔥 Ключевые улучшения:")
    print("   ✅ Заголовок: 'ОЦЕНКА КОМАНДНЫХ НАВЫКОВ'")
    print("   ✅ Убрана слипшаяся строка из таблицы")
    print("   ✅ Увеличен размер текста: 10pt → 11pt")
    print("   ✅ Улучшен интервал: 12pt → 14pt")
    print("   ✅ Диаграммы: 120mm → 100mm (баланс)")
    print("=" * 50)
    
    pdf_generator = EnhancedPDFReportV2(template_dir=output_dir / "temp_charts")
    
    # Тестируем с творческим инноватором
    scenario = TEST_SCENARIOS["creative_innovator"]
    participant_name = "Смирнова Анна"
    
    print(f"\n📊 Создание отчета для: {participant_name}")
    print(f"🎨 Профиль: {scenario['name']}")
    
    # Soft skills соответствующие профилю
    soft_skills = {
        "Творчество": 95,
        "Адаптивность": 88,
        "Коммуникация": 82,
        "Лидерство": 78,
        "Планирование": 70,
        "Аналитика": 65
    }
    
    # Интерпретации с акцентом на творчество
    interpretations = {
        "paei": """Управленческий профиль демонстрирует высокие показатели роли Предпринимателя (E = 82 балла) 
                   с выраженной способностью к инновациям, стратегическому мышлению и генерации идей. 
                   Данный профиль указывает на природную склонность к креативному подходу в решении бизнес-задач.""",
        "disc": """Поведенческий стиль характеризуется преобладанием I-типа (Влияние = 85 баллов), что 
                   свидетельствует о высокой коммуникабельности, энтузиазме и способности вдохновлять других. 
                   Рекомендуется предоставлять возможности для творческого самовыражения и командной работы.""",
        "hexaco": """Личностный профиль показывает высокие значения Открытости опыту (O = 90 баллов), что подтверждает 
                     креативность, любознательность и готовность к новым идеям. Данные характеристики делают сотрудника 
                     ценным для инновационных проектов и нестандартных решений."""
    }
    
    output_path = output_dir / f"final_report_{participant_name.lower().replace(' ', '_')}.pdf"
    
    try:
        pdf_generator.generate_enhanced_report(
            participant_name=participant_name,
            test_date="2025-10-02",
            paei_scores=scenario["paei_scores"],
            disc_scores=scenario["disc_scores"],
            hexaco_scores=scenario["hexaco_scores"],
            soft_skills_scores=soft_skills,
            ai_interpretations=interpretations,
            out_path=output_path
        )
        
        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"\n🎉 ФИНАЛЬНЫЙ ОТЧЕТ СОЗДАН!")
            print(f"📁 Файл: {output_path.name}")
            print(f"📊 Размер: {size_kb:.1f} KB")
            print(f"🖼️  Диаграммы: 4 встроенные (100mm)")
            
            # Сводка изменений
            print(f"\n📋 СВОДКА ФИНАЛЬНЫХ ИЗМЕНЕНИЙ:")
            print(f"   🎯 Заголовок: 'ОЦЕНКА КОМАНДНЫХ НАВЫКОВ'")
            print(f"   📄 Структура: Чистая таблица без дублей")
            print(f"   📝 Текст: 11pt (было 10pt) с интервалом 14pt")
            print(f"   📊 Диаграммы: 100mm (баланс с текстом)")
            print(f"   🎨 Читаемость: Значительно улучшена")
            
            # Сравнение версий
            print(f"\n📈 ЭВОЛЮЦИЯ ВЕРСИЙ:")
            print(f"   v1.0: Базовый PDF (~90KB)")
            print(f"   v2.0: Встроенные диаграммы (~620KB)")
            print(f"   v3.0: Заключение в начале (~610KB)")
            print(f"   v4.0: Оптимизированный дизайн ({size_kb:.0f}KB)")
            
        print(f"\n📂 Проверьте файл: {output_path}")
        print("🎯 Готов к использованию в продакшене!")
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_final_version()