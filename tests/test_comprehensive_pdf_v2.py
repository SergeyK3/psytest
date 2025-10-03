#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Комплексный тест новой версии PDF отчетов для всех сценариев
"""

from pathlib import Path
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from test_scenarios import TEST_SCENARIOS
import time

def test_all_scenarios_v2():
    """Создает PDF отчеты v2.0 для всех тестовых сценариев"""
    
    # Создаем папку для результатов
    output_dir = Path("comprehensive_test_reports_v2")
    output_dir.mkdir(exist_ok=True)
    
    print("🎯 Комплексное тестирование PDF отчетов v2.0")
    print("🔄 Новые возможности:")
    print("   ✅ Правильная последовательность тестов")
    print("   ✅ Расшифровка всех аббревиатур")
    print("   ✅ Радарные диаграммы для всех тестов")
    print("   ✅ Детальные описания методик")
    print("   ✅ Убрана реклама OpenAI")
    print(f"📂 Результаты будут сохранены в: {output_dir}")
    print(f"📊 Тестируется {len(TEST_SCENARIOS)} сценариев")
    print("=" * 70)
    
    # Создаем экземпляр генератора отчетов
    pdf_generator = EnhancedPDFReportV2(template_dir=output_dir / "temp_charts_v2")
    
    total_size = 0
    successful_reports = 0
    
    # Детальные AI интерпретации для разных типов
    ai_templates = {
        "manager_leader": {
            "paei": """Ярко выраженный Producer с сильными административными навыками. Профиль эффективного 
                      менеджера среднего звена, способного достигать целей и организовывать процессы. Высокие 
                      показатели по P и A указывают на способность к планированию и контролю. Рекомендуется 
                      развивать предпринимательские (E) и интеграционные (I) навыки.""",
            "disc": """Доминирующий тип с высокой инициативностью. Прямое общение, быстрые решения, ориентация 
                      на результат. Эффективен в условиях вызовов. Может проявлять нетерпеливость к медленным 
                      процессам. Рекомендуется развивать терпение и навыки работы с S-типами.""",
            "hexaco": """Высокая добросовестность и экстраверсия. Организованность сочетается с социальной 
                        активностью. Открытость к опыту с практичным подходом. Профиль подходит для руководящих 
                        позиций, требующих баланса инноваций и стабильности."""
        },
        "creative_innovator": {
            "paei": """Предпринимательский профиль с высокими показателями по E и O. Ориентация на инновации 
                      и стратегическое мышление. Хорошие интеграционные способности. Рекомендуется развивать 
                      административные навыки для лучшей реализации идей.""",
            "disc": """I-тип с высокой социальной активностью и оптимизмом. Влияние через вдохновение и 
                      энтузиазм. Может недооценивать детали и сроки. Рекомендуется партнерство с C-типами 
                      для контроля качества.""",
            "hexaco": """Высокая открытость опыту и экстраверсия. Креативность сочетается с социальными 
                        навыками. Умеренная добросовестность требует внешней поддержки в организации."""
        }
    }
    
    for scenario_key, scenario_data in TEST_SCENARIOS.items():
        print(f"\n📋 Сценарий: {scenario_key}")
        print(f"👤 Участник: {scenario_data['name']}")
        
        # Подготавливаем данные
        participant_name = scenario_data["name"].split(" (")[0]
        
        # Тестовые soft skills на основе данных сценария
        soft_skills = {
            "Коммуникация": scenario_data["disc_scores"]["I"],
            "Лидерство": scenario_data["paei_scores"]["E"], 
            "Планирование": scenario_data["paei_scores"]["A"],
            "Адаптивность": scenario_data["hexaco_scores"]["O"],
            "Аналитика": scenario_data["disc_scores"]["C"],
            "Творчество": scenario_data["hexaco_scores"]["X"]
        }
        
        # Используем шаблоны интерпретаций или базовые
        ai_interpretations = ai_templates.get(scenario_key, {
            "paei": f"Управленческий профиль с преобладанием роли {max(scenario_data['paei_scores'], key=scenario_data['paei_scores'].get)}. {scenario_data['description']}",
            "disc": f"Поведенческий стиль соответствует описанию: {scenario_data['dialog_context'][:100]}...",
            "hexaco": "Личностные черты демонстрируют сбалансированный профиль с особенностями в области взаимодействия."
        })
        
        # Создаем PDF отчет
        output_path = output_dir / f"report_v2_{scenario_key}.pdf"
        
        try:
            start_time = time.time()
            
            pdf_generator.generate_enhanced_report(
                participant_name=participant_name,
                test_date="2025-01-25",
                paei_scores=scenario_data["paei_scores"],
                disc_scores=scenario_data["disc_scores"],
                hexaco_scores=scenario_data["hexaco_scores"],
                soft_skills_scores=soft_skills,
                ai_interpretations=ai_interpretations,
                out_path=output_path
            )
            
            generation_time = time.time() - start_time
            
            if output_path.exists():
                file_size = output_path.stat().st_size / 1024
                total_size += file_size
                successful_reports += 1
                
                print(f"   ✅ Создан: {output_path.name}")
                print(f"   📊 Размер: {file_size:.1f} KB")
                print(f"   ⏱️  Время: {generation_time:.2f} сек")
            else:
                print(f"   ❌ Файл не создан")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    # Финальная статистика
    print("\n" + "=" * 70)
    print("📊 ИТОГОВАЯ СТАТИСТИКА V2.0")
    print(f"✅ Успешно создано отчетов: {successful_reports}/{len(TEST_SCENARIOS)}")
    print(f"📦 Общий размер файлов: {total_size:.1f} KB")
    print(f"📈 Средний размер отчета: {total_size/successful_reports:.1f} KB")
    
    # Проверяем созданные диаграммы
    temp_charts_dir = output_dir / "temp_charts_v2"
    if temp_charts_dir.exists():
        chart_files = list(temp_charts_dir.glob("*.png"))
        chart_size = sum(f.stat().st_size for f in chart_files) / 1024
        print(f"🎨 Создано диаграмм: {len(chart_files)}")
        print(f"🖼️  Размер диаграмм: {chart_size:.1f} KB")
    
    print(f"\n💡 Все отчеты v2.0 доступны в папке: {output_dir}")
    print("🆕 Ключевые улучшения v2.0:")
    print("   📑 Последовательность: Адизес → Soft Skills → HEXACO → DISC")
    print("   🔤 Полная расшифровка аббревиатур PAEI, DISC, HEXACO")
    print("   📊 Все диаграммы радарные для единообразия")
    print("   📝 Детальные описания методик и интерпретации")
    print("   🎯 Практические рекомендации по развитию")
    print("   🧹 Убрана реклама OpenAI")
    print("🖨️  Рекомендуется проверить качество печати")

if __name__ == "__main__":
    test_all_scenarios_v2()