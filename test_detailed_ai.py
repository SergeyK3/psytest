#!/usr/bin/env python3
"""
Подробный тест для анализа AI генерации рекомендаций по команде
"""

from interpretation_utils import generate_interpretations_from_prompt

def detailed_team_recommendations_test():
    """Подробный анализ генерации рекомендаций"""
    
    print("🔍 ПОДРОБНЫЙ АНАЛИЗ AI ГЕНЕРАЦИИ")
    print("=" * 50)
    
    # Тестовый профиль с явными слабыми областями
    test_data = {
        'paei_results': {'P': 1, 'A': 1, 'E': 5, 'I': 4},  # P и A - очень слабые
        'disc_results': {'D': 5.0, 'I': 4.0, 'S': 1.0, 'C': 2.0},  # S очень слабый
        'hexaco_results': {
            'honesty_humility': 4.0,
            'emotionality': 1.5,      # Очень слабая
            'extraversion': 1.2,      # Очень слабая  
            'agreeableness': 2.0,     # Слабая
            'conscientiousness': 4.5,
            'openness': 3.8
        },
        'soft_skills_results': {
            'leadership': 5,
            'emotional_intelligence': 5, 
            'communication': 4,
            'critical_thinking': 1,   # Очень слабый
            'time_management': 4,
            'conflict_resolution': 5,
            'adaptability': 2,        # Слабый
            'employee_development': 5,
            'teamwork': 2,            # Слабый
            'creativity': 1           # Очень слабый
        }
    }
    
    print("📊 Экстремальный профиль для тестирования:")
    print("PAEI слабые области: P=1, A=1")
    print("DISC слабые области: S=1.0, C=2.0") 
    print("HEXACO слабые области: emotionality=1.5, extraversion=1.2, agreeableness=2.0")
    print("Soft Skills слабые области: critical_thinking=1, adaptability=2, teamwork=2, creativity=1")
    print()
    
    # Генерируем интерпретации
    interpretations = generate_interpretations_from_prompt(
        test_data['paei_results'],
        test_data['disc_results'], 
        test_data['hexaco_results'],
        test_data['soft_skills_results']
    )
    
    print("📄 ПОЛНЫЕ РЕЗУЛЬТАТЫ AI ГЕНЕРАЦИИ:")
    print("=" * 50)
    
    for section_name, content in interpretations.items():
        print(f"\n🔹 РАЗДЕЛ: {section_name.upper()}")
        print("-" * 40)
        print(content)
        print("-" * 40)
        
        # Анализируем наличие ключевых слов для команд
        content_lower = content.lower()
        team_keywords = [
            'рекомендации по подбору', 'команду', 'кандидатов', 'подбор',
            'disc-компенсация', 'paei-дополнение', 'hexaco-баланс', 'soft skills-синергия',
            'специалисты', 'баланс команды', 'компенсировать', 'дополнить'
        ]
        
        found_keywords = [kw for kw in team_keywords if kw in content_lower]
        if found_keywords:
            print(f"   🎯 Найдены ключевые слова команд: {found_keywords}")
        else:
            print("   ⚠️  Ключевые слова команд не найдены")
    
    print("\n🎯 ЗАКЛЮЧЕНИЕ:")
    all_content = " ".join(interpretations.values()).lower()
    
    if 'команд' in all_content:
        print("✅ Слово 'команд' найдено в результатах")
    else:
        print("❌ Слово 'команд' НЕ найдено в результатах")
        
    if 'подбор' in all_content:
        print("✅ Слово 'подбор' найдено в результатах")
    else:
        print("❌ Слово 'подбор' НЕ найдено в результатах")
        
    if 'кандидат' in all_content:
        print("✅ Слово 'кандидат' найдено в результатах") 
    else:
        print("❌ Слово 'кандидат' НЕ найдено в результатах")

if __name__ == "__main__":
    detailed_team_recommendations_test()