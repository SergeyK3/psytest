#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест нормализации данных для PAEI и DISC
"""

def test_normalization():
    """Тестирует нормализацию данных"""
    
    # Тестовые данные (как в боте) 
    paei_scores = {"P": 3, "A": 2, "E": 5, "I": 1}  # Счетчики 0-5
    disc_scores = {"D": 2, "I": 4, "S": 6, "C": 3}  # Счетчики 0-8
    hexaco_scores = {"H": 4.5, "E": 3.0, "X": 5.0, "A": 2.5, "C": 4.0, "O": 3.5}  # Шкала 1-5
    soft_skills_scores = {
        "Коммуникация": 8.5,
        "Лидерство": 7.8,
        "Планирование": 8.2,
        "Адаптивность": 7.6,
        "Аналитика": 8.8,
        "Творчество": 7.2,
        "Командная работа": 9.0,
        "Стрессоустойчивость": 7.5,
        "Самоконтроль": 8.0,
        "Влияние": 7.0
    }  # Шкала 1-10
    
    print("Исходные данные:")
    print(f"PAEI (0-5): {paei_scores}")
    print(f"DISC (0-8): {disc_scores}")
    print(f"HEXACO (1-5): {hexaco_scores}")
    print(f"Soft Skills (1-10): {soft_skills_scores}")
    
    # Проверяем нормализацию (симулируем логику из _create_all_charts)
    paei_normalized = {k: round((v / 5.0) * 10.0, 1) for k, v in paei_scores.items()}
    disc_normalized = {k: round((v / 8.0) * 10.0, 1) for k, v in disc_scores.items()}
    # HEXACO и Soft Skills уже нормализованы для шкалы 0-10
    hexaco_normalized = {k: round((v / 5.0) * 10.0, 1) for k, v in hexaco_scores.items()}
    
    print("\nПосле нормализации:")
    print(f"PAEI (0-10): {paei_normalized}")
    print(f"DISC (0-10): {disc_normalized}")
    print(f"HEXACO (0-10): {hexaco_normalized}")
    print(f"Soft Skills (0-10): {soft_skills_scores}")
    
    print("\nТеперь все диаграммы будут в одной шкале 0-10!")
    
    # Проверяем корректность нормализации
    max_paei = max(paei_normalized.values())
    max_disc = max(disc_normalized.values()) 
    max_hexaco = max(hexaco_normalized.values())
    max_soft = max(soft_skills_scores.values())
    
    print(f"\nМаксимальные значения:")
    print(f"PAEI: {max_paei}")
    print(f"DISC: {max_disc}")
    print(f"HEXACO: {max_hexaco}")
    print(f"Soft Skills: {max_soft}")
    
    if max_paei <= 10 and max_disc <= 10:
        print("\nНормализация работает корректно!")
    else:
        print("\nОшибка нормализации!")

if __name__ == "__main__":
    test_normalization()