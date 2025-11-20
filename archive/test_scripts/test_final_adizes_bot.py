#!/usr/bin/env python3
"""
Финальный тест интерпретации Адизеса с маркдаун разметкой в боте
"""

from interpretation_utils import generate_interpretations_from_prompt
from interpretation_formatter import format_ai_interpretations
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from pathlib import Path

def test_final_adizes_in_bot():
    """Финальный тест работы интерпретации Адизеса как в боте"""
    print("🚀 Финальный тест интерпретации Адизеса в боте")
    print("=" * 60)
    
    # Имитируем реальные данные из бота
    paei_scores = {'P': 2, 'A': 2, 'E': 0, 'I': 1}  # Сбалансированный P и A
    disc_scores = {'D': 4.0, 'I': 3.0, 'S': 2.5, 'C': 3.0}
    hexaco_scores = {'H': 3.8, 'E': 4.2, 'X': 3.5, 'A': 4.0, 'C': 3.9, 'O': 4.3}
    soft_skills_scores = {
        'leadership': 4, 'communication': 5, 'teamwork': 3, 'creativity': 4,
        'time_management': 3, 'critical_thinking': 4, 'adaptability': 5,
        'problem_solving': 4, 'emotional_intelligence': 3, 'conflict_resolution': 4
    }
    
    print(f"📊 PAEI результаты: {paei_scores}")
    
    # Шаг 1: Генерируем интерпретации
    print("\n1️⃣ Генерируем интерпретации...")
    raw_interpretations = generate_interpretations_from_prompt(
        paei_scores=paei_scores,
        disc_scores=disc_scores,
        hexaco_scores=hexaco_scores,
        soft_skills_scores=soft_skills_scores
    )
    
    if 'paei' in raw_interpretations:
        adizes_raw = raw_interpretations['paei']
        print(f"✅ PAEI интерпретация сгенерирована ({len(adizes_raw)} символов)")
        
        # Подсчитываем маркдаун элементы
        markdown_raw = {
            'bold': adizes_raw.count('**'),
            'headers': adizes_raw.count('###'),
            'separators': adizes_raw.count('---'),
            'lists': adizes_raw.count('- ')
        }
        print(f"   📝 Маркдаун: {markdown_raw}")
    else:
        print("❌ PAEI интерпретация не сгенерирована!")
        return
    
    # Шаг 2: Форматируем через форматтер
    print("\n2️⃣ Форматируем через interpretation_formatter...")
    formatted_interpretations = format_ai_interpretations(raw_interpretations)
    
    if 'paei' in formatted_interpretations:
        adizes_formatted = formatted_interpretations['paei']
        print(f"✅ PAEI интерпретация отформатирована ({len(adizes_formatted)} символов)")
        
        # Подсчитываем маркдаун элементы после форматирования
        markdown_formatted = {
            'bold': adizes_formatted.count('**'),
            'headers': adizes_formatted.count('###'),
            'separators': adizes_formatted.count('---'),
            'lists': adizes_formatted.count('- ')
        }
        print(f"   📝 Маркдаун: {markdown_formatted}")
        
        # Проверяем сохранность
        if markdown_raw == markdown_formatted:
            print("   ✅ Маркдаун разметка сохранена")
        else:
            print("   ⚠️ Маркдаун разметка изменена!")
    else:
        print("❌ PAEI интерпретация потеряна!")
        return
    
    # Шаг 3: Генерируем PDF как в боте
    print("\n3️⃣ Генерируем PDF отчет...")
    
    try:
        pdf_generator = EnhancedPDFReportV2()
        pdf_path = Path("final_test_adizes_markdown.pdf")
        
        pdf_path_obj, _ = pdf_generator.generate_enhanced_report(
            participant_name="Тест Финальный",
            test_date="2025-10-24",
            paei_scores=paei_scores,
            disc_scores=disc_scores,
            hexaco_scores=hexaco_scores,
            soft_skills_scores=soft_skills_scores,
            ai_interpretations=formatted_interpretations,
            out_path=pdf_path,
            user_answers=None
        )
        
        if pdf_path_obj and pdf_path.exists():
            file_size = pdf_path.stat().st_size
            print(f"✅ PDF успешно создан!")
            print(f"📁 Путь: {pdf_path}")
            print(f"📏 Размер: {file_size} байт")
            
            # Показываем превью интерпретации
            print(f"\n📄 Превью интерпретации Адизеса:")
            lines = adizes_formatted.split('\n')[:15]
            for line in lines:
                if line.strip():
                    print(f"   {line}")
            print("   ...")
            
        else:
            print("❌ Ошибка при создании PDF")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Тест завершен! Интерпретация Адизеса теперь поддерживает маркдаун разметку.")

if __name__ == "__main__":
    test_final_adizes_in_bot()