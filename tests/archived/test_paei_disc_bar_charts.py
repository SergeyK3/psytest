#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест столбиковых диаграмм для PAEI и DISC
"""

import sys
sys.path.append('.')
sys.path.append('src')

from pathlib import Path
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from scale_normalizer import ScaleNormalizer
from datetime import datetime
from pdf_paths import get_docs_pdf_path

def test_bar_charts_paei_disc():
    """Тестируем новые столбиковые диаграммы для PAEI и DISC"""
    print("📊 Тест столбиковых диаграмм для PAEI и DISC")
    print("=" * 60)
    
    # Подготавливаем тестовые данные
    test_data = {
        "paei": {"P": 1, "A": 5, "E": 2, "I": 0},     # Будет нормализовано
        "disc": {"D": 6, "I": 1, "S": 2, "C": 0},     # Будет нормализовано 
        "hexaco": {"H": 2.3, "E": 4.7, "X": 1.9, "A": 3.6, "C": 2.1, "O": 4.4},  # Оригинал
        "soft_skills": {"Коммуникация": 7.8, "Лидерство": 6.3, "Креативность": 8.9, "Адаптивность": 5.4}  # Оригинал
    }
    
    print("📈 Исходные данные:")
    for test_type, scores in test_data.items():
        print(f"   {test_type.upper()}: {scores}")
    
    # Применяем нормализацию
    print("\n🔄 Применяем селективную нормализацию...")
    normalized_data = {}
    
    for test_type, scores in test_data.items():
        normalized_scores, method = ScaleNormalizer.auto_normalize(test_type.upper(), scores)
        normalized_data[test_type] = normalized_scores
        print(f"   {test_type.upper()}: {normalized_scores}")
        print(f"      └─ {method}")
    
    # Создаем отчет с новыми столбиковыми диаграммами
    print("\n📄 Создание PDF отчета с столбиковыми диаграммами...")
    
    try:
        generator = EnhancedPDFReportV2()
        
        # AI интерпретации
        ai_interpretations = {
            "paei": "PAEI столбиковая диаграмма: четко показывает доминирование фактора A (Администратор) после нормализации",
            "disc": "DISC столбиковая диаграмма: наглядно демонстрирует преобладание фактора D (Доминирование) после нормализации", 
            "hexaco": "HEXACO радарная диаграмма: сохраняет оригинальную шкалу 1-5 для корректной психологической интерпретации",
            "soft_skills": "Soft Skills радарная диаграмма: отображает навыки в привычной шкале 1-10"
        }
        
        # Создаем отчет в папке docs/
        pdf_path = get_docs_pdf_path("bar_charts_test", "Тест_Столбиковых_Диаграмм")
        
        pdf_path = generator.generate_enhanced_report(
            participant_name="Тест Столбиковых Диаграмм",
            test_date=datetime.now().strftime("%d.%m.%Y"),
            paei_scores=normalized_data["paei"],
            disc_scores=normalized_data["disc"],
            hexaco_scores=normalized_data["hexaco"],
            soft_skills_scores=normalized_data["soft_skills"],
            ai_interpretations=ai_interpretations,
            out_path=pdf_path
        )
        
        print(f"✅ Отчет создан: {pdf_path}")
        
        # Проверяем созданные файлы диаграмм
        print(f"\n📊 Проверка созданных диаграмм:")
        
        # Список ожидаемых диаграмм
        expected_charts = [
            "paei_bar.png",      # Новая столбиковая
            "disc_bar.png",      # Новая столбиковая
            "hexaco_radar.png",  # Остается радарная
            "soft_skills_radar.png"  # Остается радарная
        ]
        
        # Ищем папку с диаграммами рядом с PDF
        charts_dir = pdf_path.parent / "temp_charts_v2"
        if charts_dir.exists():
            for chart_name in expected_charts:
                chart_path = charts_dir / chart_name
                if chart_path.exists():
                    chart_type = "столбиковая" if "bar" in chart_name else "радарная"
                    test_name = chart_name.split("_")[0].upper()
                    print(f"   ✅ {test_name}: {chart_type} диаграмма создана")
                else:
                    print(f"   ❌ {chart_name}: файл не найден")
        else:
            print(f"   ⚠️  Папка диаграмм не найдена: {charts_dir}")
            # Проверим альтернативные места
            for possible_dir in ["temp_charts", "charts"]:
                alt_charts_dir = pdf_path.parent / possible_dir
                if alt_charts_dir.exists():
                    print(f"   📁 Найдена альтернативная папка: {alt_charts_dir}")
                    break
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Ошибка создания отчета: {e}")
        import traceback
        traceback.print_exc()
        return None

def demo_bar_vs_radar():
    """Демонстрируем разницу между столбиковыми и радарными диаграммами"""
    print(f"\n📈 Сравнение типов диаграмм:")
    print("=" * 60)
    
    print("🎯 Столбиковые диаграммы (PAEI/DISC):")
    print("   ✅ Четкое сравнение значений")
    print("   ✅ Хорошо видны пропорции")
    print("   ✅ Легко определить доминирующие факторы")
    print("   ✅ Подходят для альтернативных выборов")
    
    print(f"\n🎯 Радарные диаграммы (HEXACO/SOFT_SKILLS):")
    print("   ✅ Показывают общий профиль")
    print("   ✅ Хорошо для многомерных данных")
    print("   ✅ Визуализируют баланс характеристик")
    print("   ✅ Подходят для рейтинговых шкал")

if __name__ == "__main__":
    pdf_path = test_bar_charts_paei_disc()
    
    if pdf_path:
        demo_bar_vs_radar()
        
        print(f"\n🎉 Тест столбиковых диаграмм завершен!")
        print(f"📁 Файл: {pdf_path}")
        print(f"\n📊 Изменения:")
        print(f"   🔄 PAEI: радарная → столбиковая диаграмма")
        print(f"   🔄 DISC: радарная → столбиковая диаграмма")
        print(f"   ✅ HEXACO: остается радарная диаграмма")
        print(f"   ✅ SOFT_SKILLS: остается радарная диаграмма")
    else:
        print("❌ Тест не удался")