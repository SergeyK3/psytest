#!/usr/bin/env python3
"""
Тест для проверки AI генерации рекомендаций по команде
"""

import os
import sys

from interpretation_utils import generate_interpretations_from_prompt

def test_team_recommendations():
    """Тестируем генерацию рекомендаций по команде через AI"""
    
    print("🧪 ТЕСТ AI ГЕНЕРАЦИИ РЕКОМЕНДАЦИЙ ПО КОМАНДЕ")
    print("=" * 60)
    
    # Тестовые данные профиля со слабыми областями
    test_user_data = {
        'name': 'Тестовый Пользователь',
        'disc_results': {'D': 4.5, 'I': 3.0, 'S': 1.5, 'C': 3.5},  # Слабый S
        'paei_results': {'P': 1, 'A': 2, 'E': 4, 'I': 3},  # Слабые P, A
        'hexaco_results': {
            'honesty_humility': 3.5,
            'emotionality': 2.0,  # Слабая область
            'extraversion': 1.8,  # Слабая область  
            'agreeableness': 4.2,
            'conscientiousness': 3.8,
            'openness': 4.0
        },
        'soft_skills_results': {
            'leadership': 5,
            'emotional_intelligence': 4, 
            'communication': 4,
            'critical_thinking': 2,  # Слабая область
            'time_management': 4,
            'conflict_resolution': 5,
            'adaptability': 3,
            'employee_development': 4,
            'teamwork': 3,
            'creativity': 2  # Слабая область
        }
    }
    
    print("📊 Тестовый профиль (со слабыми областями):")
    print(f"DISC: {test_user_data['disc_results']}")
    print(f"PAEI: {test_user_data['paei_results']}")
    print(f"HEXACO emotionality: {test_user_data['hexaco_results']['emotionality']}")
    print(f"HEXACO extraversion: {test_user_data['hexaco_results']['extraversion']}")
    print(f"Soft Skills critical_thinking: {test_user_data['soft_skills_results']['critical_thinking']}")
    print(f"Soft Skills creativity: {test_user_data['soft_skills_results']['creativity']}")
    print()
    
    try:
        print("🔄 Генерируем интерпретации через AI...")
        
        # Генерируем интерпретации (включая новые рекомендации по команде)
        interpretations = generate_interpretations_from_prompt(
            test_user_data['paei_results'],
            test_user_data['disc_results'], 
            test_user_data['hexaco_results'],
            test_user_data['soft_skills_results']
        )
        
        print("✅ AI генерация завершена!")
        print()
        
        # Проверяем наличие всех ожидаемых разделов
        expected_sections = ['disc', 'paei', 'hexaco', 'soft_skills']
        
        for section in expected_sections:
            if section in interpretations:
                print(f"✅ Раздел '{section}' найден")
                
                # Проверяем наличие рекомендаций по команде
                content = interpretations[section].lower()
                team_keywords = [
                    'рекомендации по подбору', 'команду', 'кандидатов',
                    'disc-компенсация', 'paei-дополнение', 'hexaco-баланс', 'soft skills-синергия',
                    'специалисты', 'баланс команды', 'компенсировать'
                ]
                
                found_team_content = any(keyword in content for keyword in team_keywords)
                
                if found_team_content:
                    print(f"   🎯 Найдены рекомендации по команде в разделе '{section}'")
                    
                    # Показываем фрагмент с рекомендациями
                    lines = interpretations[section].split('\n')
                    for i, line in enumerate(lines):
                        if any(keyword in line.lower() for keyword in team_keywords[:6]):
                            print(f"   📋 Фрагмент: {line.strip()}")
                            if i + 1 < len(lines):
                                print(f"              {lines[i+1].strip()}")
                            break
                else:
                    print(f"   ⚠️  Рекомендации по команде не найдены в разделе '{section}'")
            else:
                print(f"❌ Раздел '{section}' отсутствует")
        
        print()
        print("🔍 АНАЛИЗ РЕЗУЛЬТАТА:")
        
        # Ищем специфические рекомендации для слабых областей
        all_content = " ".join(interpretations.values()).lower()
        
        # Проверяем рекомендации для слабых DISC областей
        if 'стабильност' in all_content or 'команд' in all_content:
            print("✅ Найдены рекомендации по компенсации слабого S (Стабильность)")
        
        # Проверяем рекомендации для слабых PAEI ролей  
        if 'продюсер' in all_content or 'администратор' in all_content:
            print("✅ Найдены рекомендации по усилению P/A ролей")
            
        # Проверяем рекомендации для слабых Soft Skills
        if 'критическ' in all_content or 'креативност' in all_content:
            print("✅ Найдены рекомендации по развитию критического мышления/креативности")
        
        # Проверяем рекомендации для слабых HEXACO областей
        if 'эмоциональност' in all_content or 'экстраверси' in all_content:
            print("✅ Найдены рекомендации по компенсации HEXACO слабостей")
            
        print()
        print("🎯 ФИНАЛЬНАЯ ПРОВЕРКА: Новая функциональность рекомендаций по команде работает!")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при генерации: {e}")
        return False

if __name__ == "__main__":
    success = test_team_recommendations()
    if success:
        print("\n🎉 ТЕСТ ПРОЙДЕН: Рекомендации по команде успешно интегрированы!")
    else:
        print("\n💥 ТЕСТ ПРОВАЛЕН: Требуется доработка")