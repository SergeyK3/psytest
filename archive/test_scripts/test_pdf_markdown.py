#!/usr/bin/env python3
"""
Тест генерации полного PDF отчета с новой интерпретацией Адизеса
"""

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from interpretation_utils import generate_interpretations_from_prompt
import tempfile
import os

def test_pdf_with_adizes_markdown():
    """Тестируем генерацию PDF с маркдаун разметкой Адизеса"""
    print("🔍 Тестирование PDF с маркдаун разметкой Адизеса")
    print("=" * 60)
    
    # Тестовые данные пользователя
    user_data = {
        'name': 'Тест Маркдаун',
        'user_id': 'test_markdown_12345'
    }
    
    # Тестовые результаты тестирования
    test_results = {
        'paei': {'P': 1, 'A': 2, 'E': 4, 'I': 1},  # Доминирует Предприниматель
        'disc': {'D': 4.0, 'I': 3.0, 'S': 2.5, 'C': 3.0},
        'hexaco': {'H': 3.8, 'E': 4.2, 'X': 3.5, 'A': 4.0, 'C': 3.9, 'O': 4.3},
        'soft': {'leadership': 4, 'communication': 5, 'teamwork': 3, 'creativity': 4,
                'time_management': 3, 'critical_thinking': 4, 'adaptability': 5,
                'problem_solving': 4, 'emotional_intelligence': 3, 'conflict_resolution': 4}
    }
    
    # Генерируем интерпретации
    print("📝 Генерируем интерпретации...")
    interpretations = generate_interpretations_from_prompt(
        paei_scores=test_results['paei'],
        disc_scores=test_results['disc'],
        hexaco_scores=test_results['hexaco'],
        soft_skills_scores=test_results['soft']
    )
    
    print(f"✅ Интерпретации сгенерированы: {list(interpretations.keys())}")
    
    # Проверяем интерпретацию Адизеса
    if 'paei' in interpretations:
        adizes_text = interpretations['paei']
        print(f"📊 Длина интерпретации Адизеса: {len(adizes_text)} символов")
        
        # Проверяем маркдаун элементы
        markdown_count = {
            'bold': adizes_text.count('**'),
            'headers': adizes_text.count('###'),
            'separators': adizes_text.count('---'),
            'lists': adizes_text.count('- ')
        }
        print(f"📝 Маркдаун элементы: {markdown_count}")
    
    # Генерируем PDF отчет
    print("\n📄 Генерируем PDF отчет...")
    
    try:
        # Создаем временный файл для PDF
        from pathlib import Path
        pdf_path = Path(f"test_adizes_markdown_{user_data['user_id']}.pdf")
        
        # Создаем экземпляр генератора отчетов
        pdf_generator = EnhancedPDFReportV2()
        
        # Генерируем PDF с интерпретациями
        pdf_path_obj, gdrive_link = pdf_generator.generate_enhanced_report(
            participant_name=user_data['name'],
            test_date="2025-10-24",
            paei_scores=test_results['paei'],
            disc_scores=test_results['disc'],
            hexaco_scores=test_results['hexaco'],
            soft_skills_scores=test_results['soft'],
            ai_interpretations=interpretations,
            out_path=pdf_path,
            user_answers=None
        )
        
        if pdf_path_obj and os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✅ PDF успешно создан!")
            print(f"📁 Путь: {pdf_path}")
            print(f"📏 Размер: {file_size} байт")
            
            # Предлагаем открыть файл
            print(f"\n🔍 Для проверки маркдаун разметки откройте файл:")
            print(f"   {pdf_path}")
            
        else:
            print("❌ Ошибка при создании PDF")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_pdf_with_adizes_markdown()