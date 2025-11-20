#!/usr/bin/env python3
"""
Тест генерации PDF с реальным AI интерпретатором и обновленным промптом
"""

import sys
from pathlib import Path
import datetime

# Добавляем src в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_ai_interpreter_with_new_format():
    """Тест AI интерпретатора с обновленным форматом из general_system_res.txt"""
    
    try:
        from psytest.ai_interpreter import AIInterpreter
        from enhanced_pdf_report_v2 import EnhancedPDFReportV2
        
        print("🧠 Тестирование AI интерпретатора с обновленным промптом...")
        print("=" * 60)
        
        # Инициализируем AI интерпретатор
        ai = AIInterpreter()
        
        # Тестовые данные
        test_scores = {
            'paei': {'P': 8, 'A': 5, 'E': 7, 'I': 6},
            'disc': {'D': 7, 'I': 5, 'S': 3, 'C': 4},
            'hexaco': {'H': 4, 'E': 3, 'X': 5, 'A': 4, 'C': 5, 'O': 3},
            'soft_skills': {
                'Коммуникация': 8.5,
                'Лидерство': 9.0,
                'Критическое мышление': 6.5,
                'Креативность': 7.2,
                'Работа в команде': 8.8,
                'Адаптивность': 8.1,
                'Эмоциональный интеллект': 9.2,
                'Решение проблем': 7.8,
                'Управление временем': 8.5,
                'Презентационные навыки': 7.0
            }
        }
        
        print("📊 Генерация AI интерпретаций с обновленным промптом...")
        
        # Получаем AI интерпретации
        ai_interpretations = {}
        
        # PAEI интерпретация
        print("    🔄 PAEI интерпретация...")
        ai_interpretations['paei'] = ai.interpret_paei(test_scores['paei'])
        
        # Soft Skills интерпретация
        print("    🔄 Soft Skills интерпретация...")
        ai_interpretations['soft_skills'] = ai.interpret_soft_skills(test_scores['soft_skills'])
        
        # HEXACO интерпретация
        print("    🔄 HEXACO интерпретация...")
        ai_interpretations['hexaco'] = ai.interpret_hexaco(test_scores['hexaco'])
        
        # DISC интерпретация
        print("    🔄 DISC интерпретация...")
        ai_interpretations['disc'] = ai.interpret_disc(test_scores['disc'])
        
        # Общая интерпретация
        print("    🔄 Общая интерпретация...")
        ai_interpretations['general'] = ai.interpret_general(test_scores)
        
        print("✅ AI интерпретации получены!")
        print()
        
        # Генерируем PDF с новыми интерпретациями
        print("📄 Генерация PDF с новыми AI интерпретациями...")
        generator = EnhancedPDFReportV2()
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = Path(f'ai_test_format_{timestamp}.pdf')
        
        # Создаем PDF и загружаем в Google Drive
        drive_url = generator.generate_enhanced_report_with_gdrive(
            'AI Тест Обновленный Формат',
            '2025-10-04',
            test_scores['paei'],
            test_scores['disc'], 
            test_scores['hexaco'],
            test_scores['soft_skills'],
            ai_interpretations,
            output_path
        )
        
        print("✅ PDF создан с реальными AI интерпретациями!")
        print()
        print("🔗 Google Drive URL:", drive_url[1] if isinstance(drive_url, tuple) else drive_url)
        print("📄 Локальный файл:", output_path)
        
        # Показываем фрагменты интерпретаций
        print()
        print("📝 ФРАГМЕНТЫ AI ИНТЕРПРЕТАЦИЙ:")
        for key, value in ai_interpretations.items():
            if value:
                preview = value[:150] + "..." if len(value) > 150 else value
                print(f"    {key.upper()}: {preview}")
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Убедитесь, что все зависимости установлены")
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_interpreter_with_new_format()