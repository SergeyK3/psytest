#!/usr/bin/env python3
"""
Тест динамических интерпретаций под диаграммами на основе промптов
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from datetime import datetime

def test_dynamic_interpretations():
    """Тест динамических интерпретаций на основе промптов *_system_res.txt"""
    print("🔄 ТЕСТ ДИНАМИЧЕСКИХ ИНТЕРПРЕТАЦИЙ")
    print("=" * 60)
    print("✅ Проверяем генерацию интерпретаций на основе промптов")
    print("✅ Интерпретации должны быть под каждой диаграммой")
    print("📤 Загружаем в Google Drive для визуального контроля")
    print()
    
    # Создаем генератор отчетов
    report_generator = EnhancedPDFReportV2()
    
    # Тестовые данные с разными профилями
    participant_name = "ДИНАМИЧЕСКИЕ ИНТЕРПРЕТАЦИИ ТЕСТ"
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    # Профиль с доминирующим Предпринимателем
    paei_scores = {
        "Предприниматель (E)": 95,
        "Администратор (A)": 78,
        "Производитель (P)": 82,
        "Интегратор (I)": 71
    }
    
    # Профиль с высоким Доминированием
    disc_scores = {
        "Доминирование (D)": 92,
        "Влияние (I)": 74,
        "Постоянство (S)": 68,
        "Соответствие (C)": 88
    }
    
    # Профиль с высокой Добросовестностью
    hexaco_scores = {
        "Честность": 89,
        "Эмоциональность": 63,
        "Экстраверсия": 77,
        "Доброжелательность": 84,
        "Добросовестность": 97,
        "Открытость опыту": 72
    }
    
    # Профиль с высоким Решением проблем
    soft_skills_scores = {
        "Коммуникация": 86,
        "Лидерство": 91,
        "Командная работа": 83,
        "Адаптивность": 79,
        "Решение проблем": 98
    }
    
    # Пустые AI интерпретации - будут заменены динамическими
    ai_interpretations = {}
    
    # Создаем имя файла
    out_path = Path(f"DYNAMIC_INTERPRETATIONS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    print(f"👤 Участник: {participant_name}")
    print("📊 Профиль:")
    print(f"   • PAEI: Доминирует {max(paei_scores, key=paei_scores.get)} ({max(paei_scores.values())} баллов)")
    print(f"   • DISC: Доминирует {max(disc_scores, key=disc_scores.get)} ({max(disc_scores.values())} баллов)")
    print(f"   • HEXACO: Доминирует {max(hexaco_scores, key=hexaco_scores.get)} ({max(hexaco_scores.values())} баллов)")
    print(f"   • Soft Skills: Доминирует {max(soft_skills_scores, key=soft_skills_scores.get)} ({max(soft_skills_scores.values())} баллов)")
    print()
    print("📄 Генерация PDF с динамическими интерпретациями...")
    print()
    
    # Генерируем отчет
    result = report_generator.generate_enhanced_report(
        participant_name=participant_name,
        test_date=test_date,
        paei_scores=paei_scores,
        disc_scores=disc_scores,
        hexaco_scores=hexaco_scores,
        soft_skills_scores=soft_skills_scores,
        ai_interpretations=ai_interpretations,
        out_path=out_path
    )
    
    print()
    print("🔍 РЕЗУЛЬТАТ:")
    if isinstance(result, str) and result.startswith("https://"):
        print(f"✅ PDF создан и загружен в Google Drive!")
        print(f"🔗 ССЫЛКА ДЛЯ ВИЗУАЛЬНОГО КОНТРОЛЯ:")
        print(f"🔗 {result}")
        print()
        print("👁️ ЧТО ПРОВЕРИТЬ В PDF:")
        print("   1. Под каждой диаграммой есть раздел 'Интерпретация:'")
        print("   2. Интерпретации содержат:")
        print("      • Конкретные баллы по тестам")
        print("      • Доминирующие характеристики")
        print("      • Анализ на основе реальных результатов")
        print("   3. Интерпретации PAEI должны содержать:")
        print("      • Упоминание Предпринимателя (95 баллов)")
        print("      • Анализ управленческих ролей")
        print("   4. Интерпретации DISC должны содержать:")
        print("      • Упоминание Доминирования (92 балла)")
        print("      • Анализ поведенческого профиля")
        print("   5. Интерпретации должны соответствовать промптам *_system_res.txt")
        
        return result
    else:
        print(f"❌ Ошибка создания отчета: {result}")
        return None

if __name__ == "__main__":
    test_dynamic_interpretations()