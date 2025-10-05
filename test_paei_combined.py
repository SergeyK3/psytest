#!/usr/bin/env python3#!/usr/bin/env python3#!/usr/bin/env python3

"""

Тест комбинированной диаграммы PAEI (столбиковая + круговая)"""# -*- coding: utf-8 -*-

"""

Тест комбинированной диаграммы PAEI (столбиковая + круговая)"""

from pathlib import Path

from src.psytest.charts import make_paei_combined_chart"""Тест для проверки комбинированной диаграммы PAEI (столбиковая + пироговая)



def test_paei_combined():"""

    """Тестирует создание комбинированной диаграммы PAEI"""

    from pathlib import Path

    # Тестовые данные как на изображении

    labels = ['P', 'A', 'E', 'I']from src.psytest.charts import make_paei_combined_chartfrom pathlib import Path

    values = [8, 5, 7, 4]  # Пример данных из изображения

    from datetime import datetime

    # Путь для сохранения

    output_path = Path("temp_charts/test_paei_combined.png")def test_paei_combined():from enhanced_pdf_report_v2 import EnhancedPDFReportV2

    output_path.parent.mkdir(exist_ok=True)

        """Тестирует создание комбинированной диаграммы PAEI"""

    # Создание диаграммы

    try:    def test_paei_combined_chart():

        result_path = make_paei_combined_chart(

            labels=labels,    # Тестовые данные как на изображении    """Тестирует создание комбинированной диаграммы PAEI"""

            values=values,

            out_path=output_path,    labels = ['P', 'A', 'E', 'I']    

            title="PAEI - Тест комбинированной диаграммы"

        )    values = [8, 5, 7, 4]  # Пример данных из изображения    print("🔄 Тестирование комбинированной диаграммы PAEI...")

        

        print(f"✅ Комбинированная диаграмма PAEI создана: {result_path}")        

        print(f"📊 Данные: {dict(zip(labels, values))}")

            # Путь для сохранения    # Тестовые данные

        if result_path.exists():

            print(f"📁 Размер файла: {result_path.stat().st_size} байт")    output_path = Path("temp_charts/test_paei_combined.png")    test_cases = [

            return True

        else:    output_path.parent.mkdir(exist_ok=True)        {

            print("❌ Файл не создан")

            return False                "name": "Сбалансированный профиль",

            

    except Exception as e:    # Создание диаграммы            "scores": {"P": 3, "A": 4, "E": 3, "I": 4}

        print(f"❌ Ошибка создания диаграммы: {e}")

        return False    try:        },



def test_various_data():        result_path = make_paei_combined_chart(        {

    """Тестирует диаграмму с различными наборами данных"""

                labels=labels,            "name": "Доминирующий Предприниматель", 

    test_cases = [

        {            values=values,            "scores": {"P": 2, "A": 1, "E": 5, "I": 2}

            'name': 'Сбалансированные',

            'values': [6, 7, 6, 5],            out_path=output_path,        },

            'filename': 'paei_balanced.png'

        },            title="PAEI - Тест комбинированной диаграммы"        {

        {

            'name': 'Производитель доминирует',        )            "name": "Высокий Производитель",

            'values': [12, 3, 4, 2],

            'filename': 'paei_producer_dominant.png'                    "scores": {"P": 5, "A": 2, "E": 1, "I": 3}

        },

        {        print(f"✅ Комбинированная диаграмма PAEI создана: {result_path}")        }

            'name': 'Интегратор высокий',

            'values': [4, 5, 3, 11],        print(f"📊 Данные: {dict(zip(labels, values))}")    ]

            'filename': 'paei_integrator_high.png'

        },            

        {

            'name': 'Как на изображении',        if result_path.exists():    pdf_generator = EnhancedPDFReportV2()

            'values': [8, 5, 7, 4],

            'filename': 'paei_from_image.png'            print(f"📁 Размер файла: {result_path.stat().st_size} байт")    

        }

    ]            return True    for i, test_case in enumerate(test_cases, 1):

    

    labels = ['P', 'A', 'E', 'I']        else:        print(f"\n--- Тест {i}: {test_case['name']} ---")

    

    print("\n🧪 Тестирование различных наборов данных:")            print("❌ Файл не создан")        

    

    for test_case in test_cases:            return False        # Создаем тестовые данные

        output_path = Path(f"temp_charts/{test_case['filename']}")

                            test_data = {

        try:

            result_path = make_paei_combined_chart(    except Exception as e:            "participant_name": f"Тестовый Участник {i}",

                labels=labels,

                values=test_case['values'],        print(f"❌ Ошибка создания диаграммы: {e}")            "test_date": datetime.now().strftime("%d.%m.%Y"),

                out_path=output_path,

                title=f"PAEI - {test_case['name']}"        return False            "paei_scores": test_case["scores"],

            )

                        "disc_scores": {"D": 5, "I": 4, "S": 3, "C": 6},

            print(f"  ✅ {test_case['name']}: {test_case['values']} → {result_path.name}")

            def test_various_data():            "hexaco_scores": {"H": 3.5, "E": 3.0, "X": 4.0, "A": 3.2, "C": 3.8, "O": 3.1},

        except Exception as e:

            print(f"  ❌ {test_case['name']}: Ошибка - {e}")    """Тестирует диаграмму с различными наборами данных"""            "soft_skills_scores": {"Лидерство": 6, "Коммуникация": 7},



if __name__ == "__main__":                "ai_interpretations": {

    print("🎯 Тестирование комбинированной диаграммы PAEI")

    print("=" * 50)    test_cases = [                "paei": f"ИИ анализ для {test_case['name']}",

    

    # Основной тест        {                "disc": "Тестовый анализ DISC", 

    success = test_paei_combined()

                'name': 'Сбалансированные',                "hexaco": "Тестовый анализ HEXACO",

    if success:

        # Дополнительные тесты            'values': [6, 7, 6, 5],                "soft_skills": "Тестовый анализ Soft Skills",

        test_various_data()

                    'filename': 'paei_balanced.png'                "general": "Общие выводы"

        print("\n🎉 Все тесты завершены!")

        print("📁 Результаты сохранены в temp_charts/")        },            }

    else:

        print("\n❌ Основной тест не прошел")        {        }

            'name': 'Производитель доминирует',        

            'values': [12, 3, 4, 2],        # Путь для PDF

            'filename': 'paei_producer_dominant.png'        output_path = Path(f"test_paei_combined_{i}.pdf")

        },        

        {        try:

            'name': 'Интегратор высокий',            # Генерируем отчет

            'values': [4, 5, 3, 11],            result_path = pdf_generator.generate_enhanced_report(

            'filename': 'paei_integrator_high.png'                participant_name=test_data["participant_name"],

        },                test_date=test_data["test_date"],

        {                paei_scores=test_data["paei_scores"],

            'name': 'Как на изображении',                disc_scores=test_data["disc_scores"],

            'values': [8, 5, 7, 4],                hexaco_scores=test_data["hexaco_scores"],

            'filename': 'paei_from_image.png'                soft_skills_scores=test_data["soft_skills_scores"],

        }                ai_interpretations=test_data["ai_interpretations"],

    ]                out_path=output_path

                )

    labels = ['P', 'A', 'E', 'I']            

                if result_path.exists():

    print("\n🧪 Тестирование различных наборов данных:")                size_kb = result_path.stat().st_size / 1024

                    print(f"✅ PDF создан: {result_path.name} ({size_kb:.1f} KB)")

    for test_case in test_cases:                

        output_path = Path(f"temp_charts/{test_case['filename']}")                # Проверяем создание комбинированной диаграммы

                        combined_chart = pdf_generator.template_dir / "paei_combined.png"

        try:                if combined_chart.exists():

            result_path = make_paei_combined_chart(                    print(f"✅ Комбинированная диаграмма PAEI создана: {combined_chart}")

                labels=labels,                else:

                values=test_case['values'],                    print("⚠️ Комбинированная диаграмма PAEI не найдена")

                out_path=output_path,                    

                title=f"PAEI - {test_case['name']}"            else:

            )                print(f"❌ Ошибка: PDF файл не создан")

                            

            print(f"  ✅ {test_case['name']}: {test_case['values']} → {result_path.name}")        except Exception as e:

                        print(f"❌ Ошибка при создании отчета: {e}")

        except Exception as e:            import traceback

            print(f"  ❌ {test_case['name']}: Ошибка - {e}")            traceback.print_exc()



if __name__ == "__main__":def test_paei_chart_components():

    print("🎯 Тестирование комбинированной диаграммы PAEI")    """Тестирует создание отдельных компонентов диаграммы PAEI"""

    print("=" * 50)    

        print("\n🔍 Тестирование компонентов диаграммы PAEI...")

    # Основной тест    

    success = test_paei_combined()    pdf_generator = EnhancedPDFReportV2()

        

    if success:    # Тестовые данные

        # Дополнительные тесты    paei_scores = {"P": 4, "A": 2, "E": 5, "I": 3}

        test_various_data()    

            # Создаем все диаграммы

        print("\n🎉 Все тесты завершены!")    charts = pdf_generator._create_all_charts(

        print("📁 Результаты сохранены в temp_charts/")        paei_scores=paei_scores,

    else:        disc_scores={"D": 5, "I": 4, "S": 3, "C": 6},

        print("\n❌ Основной тест не прошел")        hexaco_scores={"H": 3.5, "E": 3.0, "X": 4.0, "A": 3.2, "C": 3.8, "O": 3.1},
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