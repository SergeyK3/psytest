#!/usr/bin/env python3
"""
Тест новых минималистичных диаграмм для PDF отчетов
"""

from pathlib import Path
from src.psytest.charts import make_radar, make_bar_chart
from test_scenarios import TEST_SCENARIOS

def test_charts():
    """Тестирует создание диаграмм с данными из тестовых сценариев"""
    
    # Создаем папку для результатов
    output_dir = Path("test_charts_output")
    output_dir.mkdir(exist_ok=True)
    
    # Берем первый тестовый сценарий
    scenario = TEST_SCENARIOS["manager_leader"]
    paei_scores = scenario["paei_scores"]
    disc_scores = scenario["disc_scores"]
    hexaco_scores = scenario["hexaco_scores"]
    
    # Создаем тестовые soft skills (поскольку их нет в сценариях)
    soft_skills = {
        "Коммуникация": 8,
        "Лидерство": 9,
        "Планирование": 7,
        "Адаптивность": 6,
        "Аналитика": 8,
        "Творчество": 5
    }
    
    print("🎯 Тестирование улучшенных диаграмм...")
    
    # Тест радарных диаграмм
    print("\n📊 Создание радарных диаграмм:")
    
    # PAEI радар
    paei_labels = list(paei_scores.keys())
    paei_values = list(paei_scores.values())
    paei_path = output_dir / "paei_radar.png"
    
    make_radar(paei_labels, paei_values, paei_path, 
              title="PAEI - Стили управления", max_value=10)
    print(f"✅ PAEI радар: {paei_path}")
    
    # DISC радар  
    disc_labels = list(disc_scores.keys())
    disc_values = list(disc_scores.values())
    disc_path = output_dir / "disc_radar.png"
    
    make_radar(disc_labels, disc_values, disc_path,
              title="DISC - Поведенческие стили", max_value=10)
    print(f"✅ DISC радар: {disc_path}")
    
    # HEXACO радар
    hexaco_labels = list(hexaco_scores.keys())
    hexaco_values = list(hexaco_scores.values())
    hexaco_path = output_dir / "hexaco_radar.png"
    
    make_radar(hexaco_labels, hexaco_values, hexaco_path,
              title="HEXACO - Личностные черты", max_value=10)
    print(f"✅ HEXACO радар: {hexaco_path}")
    
    # Тест столбчатых диаграмм
    print("\n📈 Создание столбчатых диаграмм:")
    
    # Soft Skills столбчатая
    soft_labels = list(soft_skills.keys())
    soft_values = list(soft_skills.values())
    soft_path = output_dir / "soft_skills_bar.png"
    
    make_bar_chart(soft_labels, soft_values, soft_path,
                  title="Soft Skills", max_value=10)
    print(f"✅ Soft Skills столбчатая: {soft_path}")
    
    # Горизонтальная столбчатая для PAEI
    paei_horizontal_path = output_dir / "paei_horizontal_bar.png"
    make_bar_chart(paei_labels, paei_values, paei_horizontal_path,
                  title="PAEI - Горизонтальная", max_value=10, horizontal=True)
    print(f"✅ PAEI горизонтальная: {paei_horizontal_path}")
    
    print(f"\n🎉 Все диаграммы созданы в папке: {output_dir}")
    print("💡 Проверьте качество диаграмм для печати")
    
    # Статистика по созданным файлам
    chart_files = list(output_dir.glob("*.png"))
    total_size = sum(f.stat().st_size for f in chart_files)
    
    print(f"\n📋 Статистика:")
    print(f"   Создано файлов: {len(chart_files)}")
    print(f"   Общий размер: {total_size / 1024:.1f} KB")
    
    for chart_file in chart_files:
        size_kb = chart_file.stat().st_size / 1024
        print(f"   {chart_file.name}: {size_kb:.1f} KB")

if __name__ == "__main__":
    test_charts()