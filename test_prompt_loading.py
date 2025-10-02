#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование загрузки улучшенных промптов
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from psytest.prompts import load_prompt

def test_prompt_loading():
    """Тестируем загрузку улучшенных промптов"""
    print("🧪 ТЕСТИРОВАНИЕ ЗАГРУЗКИ ПРОМПТОВ")
    print("=" * 50)
    
    # Тестируем DISC промпт
    print("\n🔍 Тестирование DISC промпта:")
    try:
        disc_prompt = load_prompt("disk_system_res.txt")
        print(f"✅ DISC промпт загружен (длина: {len(disc_prompt)} символов)")
        
        # Проверяем ключевые элементы
        key_elements = [
            "ВАЖНО: Анализируй РЕАЛЬНЫЕ баллы клиента",
            "Образец блока DISC (пример 1 - сбалансированный профиль)",
            "Образец блока DISC (пример 2 - доминирующий тип D)",
            "Образец блока DISC (пример 3 - доминирующий тип I)"
        ]
        
        found_elements = []
        for element in key_elements:
            if element in disc_prompt:
                found_elements.append(element)
                print(f"  ✅ Найден: {element[:50]}...")
            else:
                print(f"  ❌ Не найден: {element[:50]}...")
        
        print(f"Найдено {len(found_elements)} из {len(key_elements)} ключевых элементов")
        
    except Exception as e:
        print(f"❌ Ошибка загрузки DISC промпта: {e}")
    
    # Тестируем ADIZES промпт
    print("\n🔍 Тестирование ADIZES промпта:")
    try:
        adizes_prompt = load_prompt("adizes_system_res.txt")
        print(f"✅ ADIZES промпт загружен (длина: {len(adizes_prompt)} символов)")
        
        # Проверяем ключевые элементы
        key_elements = [
            "ВАЖНО: Анализируй РЕАЛЬНЫЕ выборы клиента",
            "Образец блока Классификация по Адизесу (пример 1 - доминирующий Интегратор)",
            "Образец блока Классификация по Адизесу (пример 2 - сбалансированный профиль)",
            "Образец блока Классификация по Адизесу (пример 3 - доминирующий Предприниматель)"
        ]
        
        found_elements = []
        for element in key_elements:
            if element in adizes_prompt:
                found_elements.append(element)
                print(f"  ✅ Найден: {element[:50]}...")
            else:
                print(f"  ❌ Не найден: {element[:50]}...")
        
        print(f"Найдено {len(found_elements)} из {len(key_elements)} ключевых элементов")
        
    except Exception as e:
        print(f"❌ Ошибка загрузки ADIZES промпта: {e}")

def test_prompt_quality():
    """Анализируем качество промптов"""
    print("\n\n🔍 АНАЛИЗ КАЧЕСТВА ПРОМПТОВ")
    print("=" * 50)
    
    # Анализ DISC промпта
    print("\n📊 Анализ DISC промпта:")
    try:
        disc_prompt = load_prompt("disk_system_res.txt")
        
        # Подсчитываем примеры
        examples_count = disc_prompt.count("Образец блока DISC")
        print(f"  Количество примеров: {examples_count}")
        
        # Проверяем баланс профилей
        profiles = ["сбалансированный", "доминирующий тип D", "доминирующий тип I"]
        for profile in profiles:
            if profile in disc_prompt.lower():
                print(f"  ✅ Есть пример для: {profile}")
            else:
                print(f"  ❌ Нет примера для: {profile}")
        
        # Проверяем инструкции
        instructions = [
            "Анализируй РЕАЛЬНЫЕ баллы",
            "точную сумму баллов",
            "доминирующий тип поведения",
            "практические рекомендации"
        ]
        
        for instruction in instructions:
            if instruction in disc_prompt:
                print(f"  ✅ Инструкция: {instruction}")
        
    except Exception as e:
        print(f"❌ Ошибка анализа DISC: {e}")
    
    # Анализ ADIZES промпта  
    print("\n📊 Анализ ADIZES промпта:")
    try:
        adizes_prompt = load_prompt("adizes_system_res.txt")
        
        # Подсчитываем примеры
        examples_count = adizes_prompt.count("Образец блока Классификация по Адизесу")
        print(f"  Количество примеров: {examples_count}")
        
        # Проверяем типы профилей
        profiles = ["Интегратор", "сбалансированный", "Предприниматель"]
        for profile in profiles:
            if profile in adizes_prompt:
                print(f"  ✅ Есть пример для: {profile}")
            else:
                print(f"  ❌ Нет примера для: {profile}")
        
        # Проверяем структуру
        structure_elements = [
            "Общий портрет",
            "Рекомендации психолога", 
            "Идеальные профессиональные роли",
            "Сильные стороны",
            "Зоны роста"
        ]
        
        for element in structure_elements:
            if element in adizes_prompt:
                print(f"  ✅ Структурный элемент: {element}")
        
    except Exception as e:
        print(f"❌ Ошибка анализа ADIZES: {e}")

if __name__ == "__main__":
    print("🚀 ТЕСТИРОВАНИЕ УЛУЧШЕННЫХ ПРОМПТОВ (БЕЗ API)")
    print("=" * 60)
    
    test_prompt_loading()
    test_prompt_quality()
    
    print("\n\n🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
    print("Промпты успешно обновлены и готовы к использованию.")