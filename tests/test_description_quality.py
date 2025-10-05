#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Дополнительный тест для проверки качества детальных описаний
"""

from enhanced_pdf_report_v2 import EnhancedPDFReportV2

def test_description_quality():
    """Проверяет качество и корректность детальных описаний"""
    
    print("🔍 Тестирование качества детальных описаний...")
    
    pdf_generator = EnhancedPDFReportV2()
    
    # Тестовый случай 1: Доминирующий Производитель (PAEI)
    paei_producer = {"P": 5, "A": 2, "E": 1, "I": 2}
    desc_paei = pdf_generator._generate_detailed_test_description("PAEI", paei_producer)
    
    print("\n--- ТЕСТ PAEI (Доминирующий Производитель) ---")
    print(f"✅ Анализирует доминирующий стиль: {'Производитель' in desc_paei}")
    print(f"✅ Содержит баллы: {str(paei_producer['P']) in desc_paei}")
    print(f"✅ Дает рекомендации: {'Рекомендации' in desc_paei}")
    
    # Тестовый случай 2: Высокое доминирование (DISC)
    disc_dominant = {"D": 9, "I": 3, "S": 2, "C": 4}
    desc_disc = pdf_generator._generate_detailed_test_description("DISC", disc_dominant)
    
    print("\n--- ТЕСТ DISC (Высокое доминирование) ---")
    print(f"✅ Определяет доминирующий тип: {'Доминирование' in desc_disc}")
    print(f"✅ Анализирует уровни: {'ярко выраженный' in desc_disc or 'высокий' in desc_disc}")
    print(f"✅ Практические советы: {'Рекомендации' in desc_disc}")
    
    # Тестовый случай 3: Сбалансированный HEXACO
    hexaco_balanced = {"H": 3.5, "E": 3.2, "X": 3.8, "A": 3.3, "C": 3.6, "O": 3.4}
    desc_hexaco = pdf_generator._generate_detailed_test_description("HEXACO", hexaco_balanced)
    
    print("\n--- ТЕСТ HEXACO (Сбалансированный профиль) ---")
    print(f"✅ Анализирует все факторы: {desc_hexaco.count('средний') >= 4}")
    print(f"✅ Расшифровывает факторы: {'Честность-Скромность' in desc_hexaco}")
    print(f"✅ Дает общие рекомендации: {'рекомендации' in desc_hexaco.lower()}")
    
    # Тестовый случай 4: Высокие Soft Skills
    soft_high = {
        "Лидерство": 9,
        "Эмоциональный интеллект": 8,
        "Коммуникация": 7,
        "Критическое мышление": 6
    }
    desc_soft = pdf_generator._generate_detailed_test_description("SOFT_SKILLS", soft_high)
    
    print("\n--- ТЕСТ SOFT SKILLS (Высокие навыки) ---")
    print(f"✅ Отмечает высокие уровни: {'высокий уровень' in desc_soft}")
    print(f"✅ Анализирует каждый навык: {desc_soft.count('уровень') >= 4}")
    print(f"✅ Предлагает развитие: {'развитие' in desc_soft.lower()}")
    
    # Проверка HTML-форматирования
    print("\n--- ПРОВЕРКА ФОРМАТИРОВАНИЯ ---")
    for test_type, desc in [("PAEI", desc_paei), ("DISC", desc_disc), ("HEXACO", desc_hexaco), ("SOFT_SKILLS", desc_soft)]:
        html_elements = desc.count('<b>') + desc.count('<br/>') + desc.count('</b>')
        print(f"✅ {test_type}: HTML элементов - {html_elements}")
    
    print("\n🎯 Проверка качества завершена!")

def test_edge_cases():
    """Тестирует крайние случаи"""
    
    print("\n🔬 Тестирование крайних случаев...")
    
    pdf_generator = EnhancedPDFReportV2()
    
    # Крайний случай 1: Все низкие баллы PAEI
    paei_low = {"P": 1, "A": 1, "E": 1, "I": 1}
    desc_low = pdf_generator._generate_detailed_test_description("PAEI", paei_low)
    print(f"✅ Низкие баллы PAEI: описание сгенерировано ({len(desc_low)} символов)")
    
    # Крайний случай 2: Все максимальные баллы DISC
    disc_max = {"D": 10, "I": 10, "S": 10, "C": 10}
    desc_max = pdf_generator._generate_detailed_test_description("DISC", disc_max)
    print(f"✅ Максимальные баллы DISC: описание сгенерировано ({len(desc_max)} символов)")
    
    # Крайний случай 3: Экстремальные значения HEXACO
    hexaco_extreme = {"H": 5.0, "E": 1.0, "X": 5.0, "A": 1.0, "C": 5.0, "O": 1.0}
    desc_extreme = pdf_generator._generate_detailed_test_description("HEXACO", hexaco_extreme)
    print(f"✅ Экстремальные значения HEXACO: описание сгенерировано ({len(desc_extreme)} символов)")
    
    # Крайний случай 4: Неполный набор Soft Skills
    soft_partial = {"Лидерство": 5, "Коммуникация": 3}
    desc_partial = pdf_generator._generate_detailed_test_description("SOFT_SKILLS", soft_partial)
    print(f"✅ Частичные Soft Skills: описание сгенерировано ({len(desc_partial)} символов)")
    
    print("🎯 Тестирование крайних случаев завершено!")

if __name__ == "__main__":
    test_description_quality()
    test_edge_cases()
    print("\n🎉 Полное тестирование детальных описаний завершено!")