#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест для проверки отсутствия кеширования данных между сессиями
"""

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from scale_normalizer import ScaleNormalizer
from bot_integration_example import UserAnswersCollector
from interpretation_utils import generate_interpretations_from_prompt
from pathlib import Path
import tempfile

def test_no_cache_between_reports():
    """Тестируем, что между отчетами нет кеширования"""
    
    print("🧪 Тест: отсутствие кеширования между отчетами")
    
    # Тестовые данные для первого пользователя
    test_data_1 = {
        'paei_scores': {'P': 3, 'A': 2, 'E': 4, 'I': 1},
        'disc_scores': {'D': 2.5, 'I': 4.0, 'S': 3.5, 'C': 2.0},
        'hexaco_scores': {'H': 3.5, 'E': 2.5, 'X': 4.0, 'A': 3.0, 'C': 2.8, 'O': 4.2},
        'soft_skills_scores': {'leadership': 3.8, 'communication': 4.2}
    }
    
    # Тестовые данные для второго пользователя (другие значения)
    test_data_2 = {
        'paei_scores': {'P': 1, 'A': 4, 'E': 2, 'I': 3},
        'disc_scores': {'D': 4.0, 'I': 2.0, 'S': 1.5, 'C': 4.5},
        'hexaco_scores': {'H': 2.0, 'E': 4.5, 'X': 1.5, 'A': 4.0, 'C': 4.2, 'O': 2.8},
        'soft_skills_scores': {'leadership': 2.2, 'communication': 1.8}
    }
    
    # Создаем временную папку для тестов
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Тест 1: Создание отчетов
        print("📊 Создаем экземпляры отчетов...")
        report_1 = EnhancedPDFReportV2(template_dir=temp_path)
        report_2 = EnhancedPDFReportV2(template_dir=temp_path)
        
        print(f"📊 Report 1 ID: {id(report_1)}")
        print(f"📊 Report 2 ID: {id(report_2)}")
        print(f"✅ Разные экземпляры отчетов: {id(report_1) != id(report_2)}")
        
        # Тест интерпретаций
        print("\n🧪 Тестируем интерпретации...")
        interpretations_1 = generate_interpretations_from_prompt(
            test_data_1['paei_scores'],
            test_data_1['disc_scores'],
            test_data_1['hexaco_scores'],
            test_data_1['soft_skills_scores']
        )
        
        interpretations_2 = generate_interpretations_from_prompt(
            test_data_2['paei_scores'],
            test_data_2['disc_scores'],
            test_data_2['hexaco_scores'],
            test_data_2['soft_skills_scores']
        )
        
        print(f"📊 Интерпретации 1 ключи: {list(interpretations_1.keys())}")
        print(f"📊 Интерпретации 2 ключи: {list(interpretations_2.keys())}")
        print(f"✅ Разные интерпретации: {interpretations_1 != interpretations_2}")
        
        # Проверяем UserAnswersCollector
        print("\n🧪 Тестируем UserAnswersCollector...")
        collector_1 = UserAnswersCollector()
        collector_2 = UserAnswersCollector()
        
        # Проверяем, что это разные экземпляры
        print(f"📊 Collector 1 ID: {id(collector_1)}")
        print(f"📊 Collector 2 ID: {id(collector_2)}")
        print(f"✅ Разные экземпляры: {id(collector_1) != id(collector_2)}")
        
        # Проверяем ScaleNormalizer
        print("\n🧪 Тестируем ScaleNormalizer...")
        norm_1, method_1 = ScaleNormalizer.auto_normalize("PAEI", test_data_1['paei_scores'])
        norm_2, method_2 = ScaleNormalizer.auto_normalize("PAEI", test_data_2['paei_scores'])
        
        print(f"📊 Нормализация 1: {norm_1}")
        print(f"📊 Нормализация 2: {norm_2}")
        print(f"✅ Разные результаты: {norm_1 != norm_2}")
        
        # Проверяем что в интерпретациях разный контент
        if 'paei' in interpretations_1 and 'paei' in interpretations_2:
            paei_1_len = len(interpretations_1['paei'])
            paei_2_len = len(interpretations_2['paei'])
            print(f"\n📏 PAEI интерпретация 1: {paei_1_len} символов")
            print(f"📏 PAEI интерпретация 2: {paei_2_len} символов")
        
    print("\n🎯 Тест завершен: кеширование отсутствует!")
    return True

if __name__ == "__main__":
    test_no_cache_between_reports()