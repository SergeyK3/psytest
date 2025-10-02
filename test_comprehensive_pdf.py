#!/usr/bin/env python3
"""
Комплексный тест создания PDF отчетов для всех тестовых сценариев
"""

from pathlib import Path
from src.psytest.enhanced_pdf_report import EnhancedPDFReport
from test_scenarios import TEST_SCENARIOS
import time

def test_all_scenarios():
    """Создает PDF отчеты для всех тестовых сценариев"""
    
    # Создаем папку для результатов
    output_dir = Path("comprehensive_test_reports")
    output_dir.mkdir(exist_ok=True)
    
    print("🎯 Комплексное тестирование PDF отчетов")
    print(f"📂 Результаты будут сохранены в: {output_dir}")
    print(f"📊 Тестируется {len(TEST_SCENARIOS)} сценариев")
    print("=" * 60)
    
    # Создаем экземпляр генератора отчетов
    pdf_generator = EnhancedPDFReport(template_dir=output_dir / "temp_charts")
    
    total_size = 0
    successful_reports = 0
    
    for scenario_key, scenario_data in TEST_SCENARIOS.items():
        print(f"\n📋 Сценарий: {scenario_key}")
        print(f"👤 Участник: {scenario_data['name']}")
        
        # Подготавливаем данные
        participant_name = scenario_data["name"].split(" (")[0]  # Убираем типаж
        
        # Тестовые soft skills на основе данных сценария
        soft_skills = {
            "Коммуникация": scenario_data["disc_scores"]["I"],
            "Лидерство": scenario_data["paei_scores"]["E"], 
            "Планирование": scenario_data["paei_scores"]["A"],
            "Адаптивность": scenario_data["hexaco_scores"]["O"],
            "Аналитика": scenario_data["disc_scores"]["C"],
            "Творчество": scenario_data["hexaco_scores"]["X"]
        }
        
        # Базовые AI интерпретации
        ai_interpretations = {
            "paei": f"Анализ PAEI показывает {scenario_data['description']}. " +
                   f"Преобладающие роли: {max(scenario_data['paei_scores'], key=scenario_data['paei_scores'].get)}",
            "disc": f"DISC профиль соответствует характеристикам: {scenario_data['dialog_context'][:100]}...",
            "hexaco": f"Личностные черты HEXACO демонстрируют сбалансированный профиль с особенностями в области взаимодействия."
        }
        
        # Создаем PDF отчет
        output_path = output_dir / f"report_{scenario_key}.pdf"
        
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
    print("\n" + "=" * 60)
    print("📊 ИТОГОВАЯ СТАТИСТИКА")
    print(f"✅ Успешно создано отчетов: {successful_reports}/{len(TEST_SCENARIOS)}")
    print(f"📦 Общий размер файлов: {total_size:.1f} KB")
    print(f"📈 Средний размер отчета: {total_size/successful_reports:.1f} KB")
    
    # Проверяем созданные диаграммы
    temp_charts_dir = output_dir / "temp_charts"
    if temp_charts_dir.exists():
        chart_files = list(temp_charts_dir.glob("*.png"))
        chart_size = sum(f.stat().st_size for f in chart_files) / 1024
        print(f"🎨 Создано диаграмм: {len(chart_files)}")
        print(f"🖼️  Размер диаграмм: {chart_size:.1f} KB")
    
    print(f"\n💡 Все отчеты доступны в папке: {output_dir}")
    print("🖨️  Рекомендуется проверить качество печати на одном из файлов")

if __name__ == "__main__":
    test_all_scenarios()