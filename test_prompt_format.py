#!/usr/bin/env python3
"""
Тест обновленного промпта general_system_res.txt с новым форматом отчета
"""

def test_prompt_format():
    """Демонстрирует новый формат результатов тестирования"""
    
    print("🔍 ТЕСТ ОБНОВЛЕННОГО ПРОМПТА")
    print("=" * 50)
    
    # Тестовые данные
    test_results = {
        'paei': {'P': 4.5, 'A': 3.2, 'E': 3.8, 'I': 3.1},
        'soft_skills': {
            'Коммуникация': 8.5,
            'Лидерство': 9.0,  # Максимальный
            'Критическое мышление': 7.8,
            'Креативность': 7.2,
            'Работа в команде': 8.1
        },
        'hexaco': {'H': 3.9, 'E': 4.1, 'X': 4.3, 'A': 3.7, 'C': 4.0, 'O': 3.8},  # X максимальный
        'disc': {'D': 7, 'I': 5, 'S': 3, 'C': 6}  # D максимальный
    }
    
    # Определяем максимальные значения
    max_paei = max(test_results['paei'], key=test_results['paei'].get)
    max_soft = max(test_results['soft_skills'], key=test_results['soft_skills'].get)
    max_hexaco = max(test_results['hexaco'], key=test_results['hexaco'].get)
    max_disc = max(test_results['disc'], key=test_results['disc'].get)
    
    # Расшифровки
    paei_names = {"P": "Производитель", "A": "Администратор", "E": "Предприниматель", "I": "Интегратор"}
    disc_names = {"D": "Доминирование", "I": "Влияние", "S": "Постоянство", "C": "Соответствие"}
    hexaco_full_names = {
        "H": "Honesty-Humility (Честность-Скромность)",
        "E": "Emotionality (Эмоциональность)", 
        "X": "eXtraversion (Экстраверсия)",
        "A": "Agreeableness (Доброжелательность)",
        "C": "Conscientiousness (Добросовестность)",
        "O": "Openness (Открытость опыту)"
    }
    
    print("📋 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ (новый формат):")
    print()
    print(f"• Тест Адизеса (PAEI) - оценка управленческих ролей и стилей руководства (5 вопросов). Преобладает роль {paei_names[max_paei]} ({test_results['paei'][max_paei]} баллов)")
    print(f"• Оценка Soft Skills - анализ надпрофессиональных компетенций (10 вопросов по 10-балльной шкале). Наиболее развитый навык: {max_soft} ({test_results['soft_skills'][max_soft]} баллов)")
    print(f"• HEXACO - современная модель личности (10 вопросов по 5-балльной шкале). {max_hexaco} – {hexaco_full_names[max_hexaco]} ({test_results['hexaco'][max_hexaco]} баллов)")
    print(f"• DISC - методика оценки поведенческих стилей (8 вопросов по 4 типам). {disc_names[max_disc]} ({test_results['disc'][max_disc]} баллов)")
    
    print()
    print("✅ ПРЕИМУЩЕСТВА НОВОГО ФОРМАТА:")
    print("  🎯 Объединение методики и результата в одной строке")
    print("  📊 Правильная последовательность: PAEI → Soft Skills → HEXACO → DISC")
    print("  🔍 Полные названия HEXACO с расшифровкой")
    print("  📝 Стандартизированный формат для ИИ-интерпретатора")
    print("  💾 Добавлено в general_system_res.txt для консистентности")

if __name__ == "__main__":
    test_prompt_format()