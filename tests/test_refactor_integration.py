"""
Тесты для проверки интеграции после рефакторинга Copilot
"""

import pytest
from pathlib import Path
import tempfile
import os


class TestRefactoredIntegration:
    """Тесты интеграции после рефакторинга Copilot"""
    
    def test_pdf_module_loads_after_refactor(self):
        """Проверяет, что PDF модуль загружается после рефакторинга"""
        try:
            import enhanced_pdf_report_v2
            assert hasattr(enhanced_pdf_report_v2, 'EnhancedPDFReportV2')
            assert hasattr(enhanced_pdf_report_v2.EnhancedPDFReportV2, 'generate_enhanced_report_with_gdrive')
        except ImportError as e:
            pytest.fail(f"PDF модуль не загружается: {e}")
    
    def test_telegram_bot_compatibility(self):
        """Проверяет совместимость бота с отрефакторенным PDF модулем"""
        try:
            import telegram_test_bot
            import enhanced_pdf_report_v2
            
            # Проверяем, что генератор создается
            generator = enhanced_pdf_report_v2.EnhancedPDFReportV2()
            assert generator is not None
            
            # Проверяем наличие метода, который использует бот
            assert hasattr(generator, 'generate_enhanced_report_with_gdrive')
            
        except Exception as e:
            pytest.fail(f"Ошибка совместимости: {e}")
    
    def test_pdf_generation_returns_correct_types(self):
        """Проверяет, что PDF генерация возвращает правильные типы"""
        try:
            import enhanced_pdf_report_v2
            
            generator = enhanced_pdf_report_v2.EnhancedPDFReportV2()
            
            # Создаем временный файл для тестирования
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                tmp_path = Path(tmp.name)
            
            try:
                # Тестовые данные
                test_data = {
                    'participant_name': 'Test User',
                    'test_date': '2025-10-09',
                    'paei_scores': {'P': 8.0, 'A': 6.0, 'E': 7.0, 'I': 5.0},
                    'disc_scores': {'D': 7.0, 'I': 6.0, 'S': 5.0, 'C': 4.0},
                    'hexaco_scores': {'H': 4.0, 'E': 3.0, 'X': 5.0, 'A': 4.0, 'C': 5.0, 'O': 3.0},
                    'soft_skills_scores': {
                        'Коммуникация': 8.0,
                        'Лидерство': 7.0,
                        'Работа в команде': 6.0,
                        'Критическое мышление': 7.0,
                        'Решение проблем': 6.0,
                        'Адаптивность': 8.0,
                        'Управление временем': 5.0,
                        'Эмоциональный интеллект': 7.0,
                        'Креативность': 6.0,
                        'Стрессоустойчивость': 7.0
                    },
                    'ai_interpretations': {
                        'paei': 'Тестовая интерпретация PAEI',
                        'disc': 'Тестовая интерпретация DISC', 
                        'hexaco': 'Тестовая интерпретация HEXACO',
                        'soft_skills': 'Тестовая интерпретация Soft Skills'
                    }
                }
                
                # Вызываем функцию, которую использует бот
                result = generator.generate_enhanced_report_with_gdrive(
                    **test_data,
                    out_path=tmp_path,
                    upload_to_gdrive=False  # Отключаем Google Drive для тестов
                )
                
                # Проверяем тип возвращаемого значения
                assert isinstance(result, tuple), "Функция должна возвращать tuple"
                assert len(result) == 2, "Tuple должен содержать 2 элемента"
                
                pdf_path, gdrive_link = result
                assert isinstance(pdf_path, Path), "Первый элемент должен быть Path"
                assert gdrive_link is None or isinstance(gdrive_link, str), "Второй элемент должен быть None или str"
                
            finally:
                # Очищаем временный файл
                if tmp_path.exists():
                    os.unlink(tmp_path)
                    
        except Exception as e:
            pytest.fail(f"Ошибка генерации PDF: {e}")
    
    def test_interpretation_utils_separation(self):
        """Проверяет, что функции интерпретации правильно вынесены"""
        try:
            import interpretation_utils
            
            # Проверяем, что функция доступна
            assert hasattr(interpretation_utils, 'generate_interpretations_from_prompt')
            
            # Проверяем, что она работает
            test_scores = {
                'P': 8, 'A': 6, 'E': 7, 'I': 5
            }
            
            result = interpretation_utils.generate_interpretations_from_prompt(
                test_scores, test_scores, test_scores, test_scores
            )
            
            assert isinstance(result, dict), "Функция должна возвращать словарь"
            assert 'paei' in result, "Результат должен содержать PAEI интерпретацию"
            
        except Exception as e:
            pytest.fail(f"Ошибка с interpretation_utils: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])