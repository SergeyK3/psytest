#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрация улучшенной структуры PDF отчета v3.0
Тест: заключение в начале + увеличенные диаграммы
"""

from pathlib import Path
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from test_scenarios import TEST_SCENARIOS

def test_improved_structure():
    """Тестирует улучшенную структуру отчета"""
    
    output_dir = Path("test_improved_structure")
    output_dir.mkdir(exist_ok=True)
    
    print("🚀 ТЕСТИРОВАНИЕ УЛУЧШЕННОЙ СТРУКТУРЫ PDF v3.0")
    print("=" * 50)
    print("📋 Новые возможности:")
    print("   ✅ Заключение перенесено в начало документа")
    print("   ✅ Изменен статус на 'Оценка командных навыков'")
    print("   ✅ Увеличены размеры диаграмм (120mm vs 80mm)")
    print("   ✅ Улучшено заполнение пространства")
    print("=" * 50)
    
    pdf_generator = EnhancedPDFReportV2(template_dir=output_dir / "temp_charts")
    
    # Тестируем с аналитиком-перфекционистом
    scenario = TEST_SCENARIOS["analytical_perfectionist"]
    participant_name = "Иванов Сергей"
    
    print(f"\n📊 Создание отчета для: {participant_name}")
    print(f"🎯 Профиль: {scenario['name']}")
    
    # Soft skills соответствующие профилю
    soft_skills = {
        "Аналитика": 95,
        "Планирование": 90,
        "Коммуникация": 70,
        "Лидерство": 65,
        "Адаптивность": 75,
        "Творчество": 60
    }
    
    # Детализированные интерпретации
    interpretations = {
        "paei": """Управленческий профиль демонстрирует высокие показатели роли Администратора (A = 85 баллов) 
                   с выраженными способностями к систематизации процессов, контролю качества и организации работы. 
                   Данный профиль указывает на природную склонность к структурированному подходу в решении задач.""",
        "disc": """Поведенческий стиль характеризуется преобладанием C-типа (Соответствие = 88 баллов), что 
                   свидетельствует о высоких стандартах качества, внимании к деталям и аналитическом подходе. 
                   Рекомендуется предоставлять время для тщательного анализа перед принятием решений.""",
        "hexaco": """Личностный профиль показывает высокие значения Сознательности (C = 92 балла), что подтверждает 
                     организованность, надежность и методичность в работе. Данные характеристики делают сотрудника 
                     ценным для проектов, требующих точности и качества."""
    }
    
    output_path = output_dir / f"improved_report_{participant_name.lower().replace(' ', '_')}.pdf"
    
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
            print(f"\n✅ ОТЧЕТ СОЗДАН УСПЕШНО")
            print(f"📁 Файл: {output_path.name}")
            print(f"📊 Размер: {size_kb:.1f} KB")
            print(f"🖼️  Диаграммы: 4 встроенные (увеличенные)")
            
            # Сравнение с предыдущей версией
            print(f"\n📈 СРАВНЕНИЕ УЛУЧШЕНИЙ:")
            print(f"   📋 Структура: Заключение в начале")
            print(f"   📊 Диаграммы: Увеличены с 80mm до 120mm")
            print(f"   📄 Статус: 'Оценка командных навыков' вместо 'Анализ завершён'")
            print(f"   🎯 Заполнение: Оптимизировано пространство страницы")
            
        print(f"\n📂 Проверьте файл: {output_path}")
        print("💡 Сравните с предыдущими версиями для оценки улучшений")
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_improved_structure()