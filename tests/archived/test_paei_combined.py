#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест для проверки комбинированной диаграммы PAEI (столбиковая + пироговая)
"""

from pathlib import Path
from datetime import datetime
from enhanced_pdf_report import EnhancedPDFReportV2

def test_paei_combined_chart():
    """Тестирует создание комбинированной диаграммы PAEI"""
    
    print("🔄 Тестирование комбинированной диаграммы PAEI...")
    
    # Тестовые данные
    test_cases = [
        {
            "name": "Сбалансированный профиль",
            "scores": {"P": 3, "A": 4, "E": 3, "I": 4}
        },
        {
            "name": "Доминирующий Предприниматель", 
            "scores": {"P": 2, "A": 1, "E": 5, "I": 2}
        },
        {
            "name": "Высокий Производитель",
            "scores": {"P": 5, "A": 2, "E": 1, "I": 3}
        }
    ]
    
    pdf_generator = EnhancedPDFReportV2()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Тест {i}: {test_case['name']} ---")
        
        # Создаем тестовые данные
        test_data = {
            "participant_name": f"Тестовый Участник {i}",
            "test_date": datetime.now().strftime("%d.%m.%Y"),
            "paei_scores": test_case["scores"],
            "disc_scores": {"D": 5, "I": 4, "S": 3, "C": 6},
            "hexaco_scores": {"H": 3.5, "E": 3.0, "X": 4.0, "A": 3.2, "C": 3.8, "O": 3.1},
            "soft_skills_scores": {"Лидерство": 6, "Коммуникация": 7},
            "ai_interpretations": {
                "paei": f"ИИ анализ для {test_case['name']}",
                "disc": "Тестовый анализ DISC", 
                "hexaco": "Тестовый анализ HEXACO",
                "soft_skills": "Тестовый анализ Soft Skills",
                "general": "Общие выводы"
            }
        }
        
        # Путь для PDF
        output_path = Path(f"test_paei_combined_{i}.pdf")
        
        try:
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
                size_kb = result_path.stat().st_size / 1024
                print(f"✅ PDF создан: {result_path.name} ({size_kb:.1f} KB)")
                
                # Проверяем создание комбинированной диаграммы
                combined_chart = pdf_generator.template_dir / "paei_combined.png"
                if combined_chart.exists():
                    print(f"✅ Комбинированная диаграмма PAEI создана: {combined_chart}")
                else:
                    print("⚠️ Комбинированная диаграмма PAEI не найдена")
                    
            else:
                print(f"❌ Ошибка: PDF файл не создан")
                
        except Exception as e:
            print(f"❌ Ошибка при создании отчета: {e}")
            import traceback
            traceback.print_exc()

def test_paei_chart_components():
    """Тестирует создание отдельных компонентов диаграммы PAEI"""
    
    print("\n🔍 Тестирование компонентов диаграммы PAEI...")
    
    pdf_generator = EnhancedPDFReportV2()
    
    # Тестовые данные
    paei_scores = {"P": 4, "A": 2, "E": 5, "I": 3}
    
    # Создаем все диаграммы
    charts = pdf_generator._create_all_charts(
        paei_scores=paei_scores,
        disc_scores={"D": 5, "I": 4, "S": 3, "C": 6},
        hexaco_scores={"H": 3.5, "E": 3.0, "X": 4.0, "A": 3.2, "C": 3.8, "O": 3.1},
        soft_skills_scores={"Лидерство": 6, "Коммуникация": 7}
    )
    
    # Проверяем созданные файлы
    expected_files = ['paei_bar', 'paei_pie', 'paei']
    
    for chart_type in expected_files:
        if chart_type in charts and charts[chart_type].exists():
            size = charts[chart_type].stat().st_size
            print(f"✅ {chart_type}: {charts[chart_type].name} ({size} bytes)")
        else:
            print(f"❌ {chart_type}: файл не создан")
    
    # Тест метода создания комбинированной диаграммы
    if 'paei_bar' in charts and 'paei_pie' in charts:
        try:
            test_combined_path = pdf_generator.template_dir / "test_paei_combined.png"
            result = pdf_generator._create_paei_combined_chart(
                charts['paei_bar'], 
                charts['paei_pie'], 
                test_combined_path, 
                paei_scores
            )
            
            if result.exists():
                print(f"✅ Тестовая комбинированная диаграмма создана: {result.name}")
            else:
                print("❌ Тестовая комбинированная диаграмма не создана")
                
        except Exception as e:
            print(f"❌ Ошибка создания тестовой комбинированной диаграммы: {e}")

def test_edge_cases():
    """Тестирует крайние случаи для PAEI диаграмм"""
    
    print("\n🔬 Тестирование крайних случаев PAEI...")
    
    pdf_generator = EnhancedPDFReportV2()
    
    edge_cases = [
        {"name": "Все нули", "scores": {"P": 0, "A": 0, "E": 0, "I": 0}},
        {"name": "Один максимум", "scores": {"P": 5, "A": 0, "E": 0, "I": 0}},
        {"name": "Все максимумы", "scores": {"P": 5, "A": 5, "E": 5, "I": 5}}
    ]
    
    for case in edge_cases:
        print(f"\n--- {case['name']} ---")
        try:
            # Создаем отдельную комбинированную диаграмму
            bar_path = pdf_generator.template_dir / f"test_bar_{case['name'].replace(' ', '_')}.png"
            pie_path = pdf_generator.template_dir / f"test_pie_{case['name'].replace(' ', '_')}.png"
            combined_path = pdf_generator.template_dir / f"test_combined_{case['name'].replace(' ', '_')}.png"
            
            # Создаем базовые диаграммы (заглушки)
            import matplotlib.pyplot as plt
            
            # Создаем простую заглушку для тестирования
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.text(0.5, 0.5, f"Test {case['name']}", ha='center', va='center')
            plt.savefig(bar_path, dpi=150)
            plt.savefig(pie_path, dpi=150)
            plt.close()
            
            # Тестируем комбинированную диаграмму
            result = pdf_generator._create_paei_combined_chart(
                bar_path, pie_path, combined_path, case["scores"]
            )
            
            if result.exists():
                print(f"✅ {case['name']}: комбинированная диаграмма создана")
            else:
                print(f"❌ {case['name']}: ошибка создания")
                
        except Exception as e:
            print(f"❌ {case['name']}: исключение - {e}")

if __name__ == "__main__":
    print("🚀 Запуск тестирования комбинированной диаграммы PAEI...")
    
    # Основной тест
    test_paei_combined_chart()
    
    # Тест компонентов
    test_paei_chart_components()
    
    # Тест крайних случаев
    test_edge_cases()
    
    print("\n🎉 Тестирование комбинированной диаграммы PAEI завершено!")