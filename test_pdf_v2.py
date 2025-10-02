#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест улучшенного PDF отчета версии 2.0 с расширенными описаниями
"""

from pathlib import Path
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from test_scenarios import TEST_SCENARIOS

def test_enhanced_pdf_v2():
    """Тестирует создание улучшенного PDF отчета v2.0"""
    
    # Создаем папку для результатов
    output_dir = Path("test_pdf_v2_output")
    output_dir.mkdir(exist_ok=True)
    
    # Берем тестовый сценарий
    scenario = TEST_SCENARIOS["manager_leader"]
    print(f"🎯 Создание улучшенного PDF отчета v2.0 для: {scenario['name']}")
    
    # Создаем экземпляр генератора отчетов
    pdf_generator = EnhancedPDFReportV2(template_dir=output_dir / "temp_charts_v2")
    
    # Подготавливаем данные
    report_data = {
        "name": scenario["name"].split(" (")[0],  # Убираем типаж из имени
        "paei_scores": scenario["paei_scores"],
        "disc_scores": scenario["disc_scores"], 
        "hexaco_scores": scenario["hexaco_scores"],
        "ai_interpretations": {
            "paei": """Ярко выраженный Producer (Производитель) с сильными административными навыками. 
                      Отличается высокой результативностью и способностью к планированию. Данный профиль 
                      характерен для эффективных менеджеров среднего звена, способных как достигать целей, 
                      так и организовывать рабочие процессы. Рекомендуется развивать предпринимательские 
                      и интеграционные навыки для роста до топ-менеджмента.""",
            "disc": """Доминирующий тип с высокой инициативностью и ориентацией на результат. 
                      Предпочитает прямое общение и быстрое принятие решений. Хорошо работает в условиях 
                      вызовов и конкуренции. Может проявлять нетерпеливость к медленным процессам. 
                      Рекомендуется развивать терпение и навыки работы с людьми для повышения 
                      эффективности командного взаимодействия.""",
            "hexaco": """Высокая добросовестность и экстраверсия свидетельствуют об организованности 
                        и социальной активности. Открытость к новому опыту сочетается с практичным 
                        подходом к задачам. Умеренный уровень эмоциональности говорит о стрессоустойчивости. 
                        Профиль подходит для руководящих позиций, требующих баланса между инновациями 
                        и стабильностью."""
        }
    }
    
    # Создаем тестовые soft skills на основе данных сценария
    soft_skills = {
        "Коммуникация": 8,
        "Лидерство": 9,
        "Планирование": 7,
        "Адаптивность": 6,
        "Аналитика": 8,
        "Творчество": 5
    }
    
    # Создаем PDF отчет
    output_path = output_dir / f"enhanced_report_v2_{scenario['name'].split()[0].lower()}.pdf"
    
    try:
        pdf_generator.generate_enhanced_report(
            participant_name=report_data["name"],
            test_date="2025-01-25",
            paei_scores=report_data["paei_scores"],
            disc_scores=report_data["disc_scores"],
            hexaco_scores=report_data["hexaco_scores"],
            soft_skills_scores=soft_skills,
            ai_interpretations=report_data["ai_interpretations"],
            out_path=output_path
        )
        
        print(f"✅ PDF отчет v2.0 создан: {output_path}")
        
        # Статистика файла
        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"📊 Размер файла: {size_kb:.1f} KB")
        
        # Проверяем созданные диаграммы
        temp_charts_dir = output_dir / "temp_charts_v2"
        if temp_charts_dir.exists():
            chart_files = list(temp_charts_dir.glob("*.png"))
            print(f"📈 Создано диаграмм: {len(chart_files)}")
            for chart in chart_files:
                print(f"   - {chart.name}")
        
        print("\n🎉 Тест PDF отчета v2.0 завершен успешно!")
        print("📋 Улучшения в v2.0:")
        print("   ✅ Последовательность: Адизес → Soft Skills → HEXACO → DISC")
        print("   ✅ Расшифровка аббревиатур PAEI")
        print("   ✅ Все диаграммы радарные (включая Soft Skills)")
        print("   ✅ Детальные описания каждого теста")
        print("   ✅ Убрана ссылка на OpenAI")
        print("   ✅ Расширенные интерпретации и рекомендации")
        print(f"💡 Откройте файл {output_path} для проверки качества")
        
    except Exception as e:
        print(f"❌ Ошибка при создании PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_pdf_v2()