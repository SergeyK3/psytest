#!/usr/bin/env python3
"""
Тест новой функциональности рекомендаций по подбору команды
"""

def test_team_recommendations():
    """Тестируем логику рекомендаций по подбору команды"""
    
    # Пример профиля для тестирования
    test_profile = {
        'disc': {'D': 4.5, 'I': 3.0, 'S': 2.0, 'C': 3.5},
        'paei': {'P': 1, 'A': 2, 'E': 4, 'I': 3},
        'hexaco': {
            'H': 3.5, 'E': 2.5, 'X': 4.0, 
            'A': 2.0, 'C': 3.0, 'O': 4.2
        },
        'soft_skills': {
            'leadership': 4, 'emotional_intelligence': 5,
            'communication': 4, 'critical_thinking': 3,
            'time_management': 4, 'conflict_resolution': 5,
            'adaptability': 4, 'employee_development': 5
        }
    }
    
    print("🧪 ТЕСТ РЕКОМЕНДАЦИЙ ПО ПОДБОРУ КОМАНДЫ")
    print("=" * 50)
    
    print("\n📊 Анализируемый профиль:")
    print(f"DISC: D={test_profile['disc']['D']}, I={test_profile['disc']['I']}, S={test_profile['disc']['S']}, C={test_profile['disc']['C']}")
    print(f"PAEI: P={test_profile['paei']['P']}, A={test_profile['paei']['A']}, E={test_profile['paei']['E']}, I={test_profile['paei']['I']}")
    print(f"Soft Skills (средние): {sum(test_profile['soft_skills'].values())/len(test_profile['soft_skills']):.1f}")
    
    print("\n💡 Ожидаемые рекомендации:")
    
    # DISC анализ
    disc_weak = [k for k, v in test_profile['disc'].items() if v <= 2.5]
    print(f"DISC-компенсация: Нужны специалисты с высоким {', '.join(disc_weak)} (слабые области)")
    
    # PAEI анализ  
    paei_weak = [k for k, v in test_profile['paei'].items() if v <= 2]
    print(f"PAEI-дополнение: Нужны {', '.join(paei_weak)} (недостающие роли)")
    
    # Soft Skills анализ
    soft_weak = [k for k, v in test_profile['soft_skills'].items() if v <= 3]
    print(f"Soft Skills-синергия: Нужны эксперты в {', '.join(soft_weak)}")
    
    print("\n🎯 Практические рекомендации:")
    print("- Добавить S-типы (Стабильность) для баланса высокого D")
    print("- Найти сильного P (Продюсера) для выполнения задач")
    print("- Укрепить A (Администратора) для систематизации")
    print("- Компенсировать низкую экстраверсию и покладистость")
    
    print("\n✅ Новая функциональность готова к тестированию!")

if __name__ == "__main__":
    test_team_recommendations()