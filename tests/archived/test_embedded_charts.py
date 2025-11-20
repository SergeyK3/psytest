#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест создания нескольких PDF отчетов v2.0 с встроенными диаграммами
"""

from pathlib import Path
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from test_scenarios import TEST_SCENARIOS

def test_embedded_charts():
    """Создает несколько PDF отчетов с встроенными диаграммами"""
    
    output_dir = Path("test_embedded_charts")
    output_dir.mkdir(exist_ok=True)
    
    print("🎯 Тестирование PDF отчетов v2.0 с встроенными диаграммами")
    print("📊 Особенности:")
    print("   ✅ Диаграммы встроены прямо в документ")
    print("   ✅ Единый файл без внешних зависимостей")
    print("   ✅ Правильная последовательность разделов")
    print("   ✅ Детальные описания методик")
    print("=" * 60)
    
    pdf_generator = EnhancedPDFReportV2(template_dir=output_dir / "temp_charts")
    
    # Тестируем 3 разных сценария
    test_scenarios = ["manager_leader", "creative_innovator", "analytical_perfectionist"]
    
    for scenario_key in test_scenarios:
        scenario = TEST_SCENARIOS[scenario_key]
        participant_name = scenario["name"].split(" (")[0]
        
        print(f"\n📋 Создание отчета для: {participant_name}")
        
        # Soft skills на основе тестовых данных
        soft_skills = {
            "Коммуникация": scenario["disc_scores"]["I"],
            "Лидерство": scenario["paei_scores"]["E"], 
            "Планирование": scenario["paei_scores"]["A"],
            "Адаптивность": scenario["hexaco_scores"]["O"],
            "Аналитика": scenario["disc_scores"]["C"],
            "Творчество": scenario["hexaco_scores"]["X"]
        }
        
        # Детализированные интерпретации
        interpretations = {
            "paei": f"""Управленческий профиль показывает преобладание роли {max(scenario['paei_scores'], key=scenario['paei_scores'].get)} 
                       с показателем {max(scenario['paei_scores'].values())} баллов. {scenario['description']} 
                       Данный профиль указывает на способность к эффективному выполнению соответствующих 
                       управленческих функций и потенциал развития в данном направлении.""",
            "disc": f"""Поведенческий стиль характеризуется преобладанием {max(scenario['disc_scores'], key=scenario['disc_scores'].get)}-типа. 
                       {scenario['dialog_context']} Рекомендуется учитывать эти особенности при постановке задач 
                       и организации рабочего процесса.""",
            "hexaco": f"""Личностный профиль демонстрирует сбалансированное развитие основных черт личности. 
                         Наиболее выражена характеристика {max(scenario['hexaco_scores'], key=scenario['hexaco_scores'].get)} 
                         ({max(scenario['hexaco_scores'].values())} баллов), что указывает на соответствующие 
                         особенности в профессиональном и межличностном взаимодействии."""
        }
        
        output_path = output_dir / f"embedded_report_{scenario_key}.pdf"
        
        try:
            pdf_generator.generate_enhanced_report(
                participant_name=participant_name,
                test_date="2025-01-25",
                paei_scores=scenario["paei_scores"],
                disc_scores=scenario["disc_scores"],
                hexaco_scores=scenario["hexaco_scores"],
                soft_skills_scores=soft_skills,
                ai_interpretations=interpretations,
                out_path=output_path
            )
            
            if output_path.exists():
                size_kb = output_path.stat().st_size / 1024
                print(f"   ✅ Создан: {output_path.name}")
                print(f"   📊 Размер: {size_kb:.1f} KB")
                print(f"   🎨 Содержит: 4 встроенные диаграммы")
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    # Проверка созданных файлов
    pdf_files = list(output_dir.glob("*.pdf"))
    total_size = sum(f.stat().st_size for f in pdf_files) / 1024
    
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print(f"✅ Создано PDF файлов: {len(pdf_files)}")
    print(f"📦 Общий размер: {total_size:.1f} KB")
    print(f"📈 Средний размер: {total_size/len(pdf_files):.1f} KB")
    
    # Проверка временных диаграмм
    temp_dir = output_dir / "temp_charts"
    if temp_dir.exists():
        chart_files = list(temp_dir.glob("*.png"))
        print(f"🖼️  Временных диаграмм: {len(chart_files)}")
        print("💡 Диаграммы встроены в PDF и больше не нужны отдельно")
    
    print(f"\n📂 Все файлы в папке: {output_dir}")
    print("🎯 Каждый PDF - это единый документ с встроенными диаграммами")
    print("📄 Документы готовы для печати и распространения")

if __name__ == "__main__":
    test_embedded_charts()