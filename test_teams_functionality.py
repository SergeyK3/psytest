#!/usr/bin/env python3
"""
Быстрый тест новой функциональности рекомендаций по команде
"""

import sys
import os

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from src.psytest.ai_interpreter import AIInterpreter

def test_team_recommendations():
    """Тестируем генерацию рекомендаций по команде"""
    
    print("🧪 ТЕСТ РЕКОМЕНДАЦИЙ ПО КОМАНДЕ")
    print("=" * 50)
    
    # Тестовые данные
    test_scores = {
        'paei': [3, 4, 2, 1],  # P=3, A=4, E=2, I=1 - Администратор
        'disc': [2, 3, 1, 4],  # D=2, I=3, S=1, C=4 - Compliance
        'hexaco': [4, 3, 2, 5, 3, 4],  # Высокая Честность
        'soft_skills': [3, 4, 3, 4, 2, 3, 4, 2]  # Смешанные навыки
    }
    
    user_data = {
        'name': 'TEST_TEAMS',
        'age': 30,
        'position': 'Менеджер',
        'scores': test_scores
    }
    
    # 1. Тестируем AI интерпретацию
    print("🤖 Тестируем AI генерацию рекомендаций...")
    
    try:
        ai_interpreter = AIInterpreter()
        
        # Генерируем общее заключение с рекомендациями по команде
        general_interpretation = ai_interpreter.interpret_general_conclusion(test_scores)
        
        if general_interpretation:
            print("✅ AI успешно сгенерировал рекомендации:")
            print(f"   📝 Длина: {len(general_interpretation)} символов")
            
            # Проверяем ключевые слова
            keywords = ['команд', 'подбор', 'специалист', 'компенс', 'дополн', 'баланс']
            found_keywords = [kw for kw in keywords if kw.lower() in general_interpretation.lower()]
            
            print(f"   🔍 Найдено ключевых слов: {found_keywords}")
            
            # Показываем отрывок
            print(f"   📄 Начало текста:")
            print(f"      {general_interpretation[:200]}...")
            
        else:
            print("❌ AI не смог сгенерировать рекомендации")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка AI: {e}")
        return False
    
    # 2. Тестируем PDF генерацию
    print(f"\n📄 Тестируем PDF генерацию...")
    
    try:
        pdf_generator = EnhancedPDFReportV2()
        
        # Создаем PDF с рекомендациями
        pdf_path = pdf_generator.generate_report(user_data, "team_test")
        
        if pdf_path and os.path.exists(pdf_path):
            print(f"✅ PDF создан: {pdf_path}")
            
            # Проверяем размер файла
            file_size = os.path.getsize(pdf_path)
            print(f"   📊 Размер файла: {file_size} байт")
            
            return True
        else:
            print("❌ PDF не был создан")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка PDF: {e}")
        return False

if __name__ == "__main__":
    success = test_team_recommendations()
    
    if success:
        print(f"\n🎊 ТЕСТ ПРОЙДЕН: Функциональность рекомендаций по команде работает!")
        print(f"   💡 Следующий шаг: протестировать через Telegram бота")
    else:
        print(f"\n❌ ТЕСТ НЕ ПРОЙДЕН: Требуется отладка")