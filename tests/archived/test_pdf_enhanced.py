#!/usr/bin/env python3
"""
Тест создания полного PDF отчета с улучшенными диаграммами
"""

from pathlib import Path
from src.psytest.enhanced_pdf_report import EnhancedPDFReport
from test_scenarios import TEST_SCENARIOS

def test_enhanced_pdf_report():
    """Тестирует создание полного PDF отчета"""
    
    # Создаем папку для результатов
    output_dir = Path("test_pdf_output")
    output_dir.mkdir(exist_ok=True)
    
    # Берем тестовый сценарий
    scenario = TEST_SCENARIOS["manager_leader"]
    print(f"🎯 Создание PDF отчета для: {scenario['name']}")
    
    # Создаем экземпляр генератора отчетов
    pdf_generator = EnhancedPDFReport(template_dir=output_dir / "temp_charts")
    
    # Подготавливаем данные
    report_data = {
        "name": scenario["name"].split(" (")[0],  # Убираем типаж из имени
        "paei_scores": scenario["paei_scores"],
        "disc_scores": scenario["disc_scores"], 
        "hexaco_scores": scenario["hexaco_scores"],
        "ai_interpretations": {
            "paei": "Ярко выраженный Producer (Производитель) с сильными административными навыками. Отличается высокой результативностью и способностью к планированию.",
            "disc": "Доминирующий тип с высокой инициативностью. Предпочитает прямое общение и быстрое принятие решений.",
            "hexaco": "Высокая добросовестность и экстраверсия. Открыт к новому опыту, но сохраняет практичный подход к задачам."
        },
        "summary": "Эффективный руководитель с сильными управленческими качествами и ориентацией на результат."
    }
    
    # Создаем PDF отчет
    output_path = output_dir / f"enhanced_report_{scenario['name'].split()[0].lower()}.pdf"
    
    try:
        # Создаем тестовые soft skills
        soft_skills = {
            "Коммуникация": 8,
            "Лидерство": 9,
            "Планирование": 7,
            "Адаптивность": 6,
            "Аналитика": 8,
            "Творчество": 5
        }
        
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
        
        print(f"✅ PDF отчет создан: {output_path}")
        
        # Статистика файла
        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"📊 Размер файла: {size_kb:.1f} KB")
        
        # Проверяем созданные диаграммы
        temp_charts_dir = output_dir / "temp_charts"
        if temp_charts_dir.exists():
            chart_files = list(temp_charts_dir.glob("*.png"))
            print(f"📈 Создано диаграмм: {len(chart_files)}")
            for chart in chart_files:
                print(f"   - {chart.name}")
        
        print("\n🎉 Тест PDF отчета завершен успешно!")
        print(f"💡 Откройте файл {output_path} для проверки качества")
        
    except Exception as e:
        print(f"❌ Ошибка при создании PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_pdf_report()