#!/usr/bin/env python3
"""
Объяснение методологии DISC - как работает подсчет баллов
"""

def explain_disc_methodology():
    """Объясняем методологию DISC на конкретном примере"""
    print("🎯 МЕТОДОЛОГИЯ DISC - Подробное объяснение")
    print("=" * 60)
    
    print("\n📋 Структура теста:")
    print("   • 8 вопросов (по 2 на каждую категорию)")
    print("   • 4 категории: D (Доминирование), I (Влияние), S (Постоянство), C (Соответствие)")
    print("   • Шкала ответов: 1-5 баллов")
    
    print("\n📝 Пример прохождения теста:")
    print("-" * 40)
    
    # Пример структуры вопросов
    questions_example = [
        {"text": "Я берую на себя ответственность за сложные задачи", "category": "D"},
        {"text": "Я стремлюсь к быстрому достижению целей", "category": "D"},
        {"text": "Мне нравится вдохновлять людей на новые идеи", "category": "I"},
        {"text": "Я легко завожу новые знакомства", "category": "I"},
        {"text": "Я предпочитаю стабильную среду", "category": "S"},
        {"text": "Мне комфортно следовать процедурам", "category": "S"},
        {"text": "Я всегда проверяю детали", "category": "C"},
        {"text": "Я предпочитаю структурированные задачи", "category": "C"}
    ]
    
    # Пример ответов пользователя
    user_answers = [5, 4, 2, 3, 3, 4, 5, 4]  # Оценки 1-5 для каждого вопроса
    
    print("Вопрос → Ответ → Категория")
    disc_totals = {"D": 0, "I": 0, "S": 0, "C": 0}
    
    for i, (question, answer) in enumerate(zip(questions_example, user_answers)):
        category = question["category"]
        disc_totals[category] += answer
        print(f"{i+1}. {question['text'][:40]}... → {answer} → {category}")
    
    print(f"\n📊 Итоговые баллы:")
    print(f"   D (Доминирование): {disc_totals['D']}/10 (из 2 вопросов: 5+4=9)")
    print(f"   I (Влияние): {disc_totals['I']}/10 (из 2 вопросов: 2+3=5)")
    print(f"   S (Постоянство): {disc_totals['S']}/10 (из 2 вопросов: 3+4=7)")
    print(f"   C (Соответствие): {disc_totals['C']}/10 (из 2 вопросов: 5+4=9)")

def explain_key_points():
    """Ключевые моменты методологии"""
    print("\n💡 КЛЮЧЕВЫЕ МОМЕНТЫ:")
    print("=" * 40)
    
    print("\n❓ Вопрос: Влияет ли каждый ответ на все категории?")
    print("✅ Ответ: НЕТ! Каждый вопрос относится к ОДНОЙ категории")
    
    print("\n🎯 Как это работает:")
    print("   1. Каждый вопрос заранее привязан к одной категории (D/I/S/C)")
    print("   2. Ваш ответ (1-5 баллов) добавляется ТОЛЬКО к этой категории")
    print("   3. Итоговый балл = сумма ответов на вопросы этой категории")
    
    print("\n📈 Диапазоны баллов:")
    print("   • Минимум: 8 баллов (8 вопросов × 1 балл = 8)")
    print("   • Максимум: 40 баллов (8 вопросов × 5 баллов = 40)")
    print("   • Но не все 8 вопросов идут в одну категорию!")
    
    print("\n🔍 Реальные диапазоны (при 2 вопросах на категорию):")
    print("   • Минимум: 2 балла (2 вопроса × 1 балл = 2)")
    print("   • Максимум: 10 баллов (2 вопроса × 5 баллов = 10)")
    
def explain_your_results():
    """Объяснение результатов D=32, I=20, S=28, C=24"""
    print("\n🎯 АНАЛИЗ ВАШИХ РЕЗУЛЬТАТОВ:")
    print("=" * 40)
    
    your_results = {"D": 32, "I": 20, "S": 28, "C": 24}
    total = sum(your_results.values())
    
    print(f"Ваши баллы: {your_results}")
    print(f"Общая сумма: {total} баллов")
    
    # Если 8 вопросов и каждый 1-5 баллов, то максимум = 8*5 = 40 баллов на человека
    # Но баллы распределяются по категориям
    
    print(f"\n🤔 Анализ:")
    questions_per_category = total / sum(your_results.values()) * len(your_results)
    avg_per_category = total / len(your_results)
    
    print(f"   • Общая сумма: {total} баллов")
    print(f"   • Среднее на категорию: {avg_per_category:.1f} баллов")
    print(f"   • Максимальная категория: D = {your_results['D']} баллов")
    print(f"   • Минимальная категория: I = {your_results['I']} баллов")
    
    if total > 40:
        estimated_questions = total // 5  # Примерное количество вопросов если все отвечали на 5
        print(f"\n💭 Предположение: В тесте было около {estimated_questions} вопросов")
        print(f"   (если средний ответ был 5 баллов)")
    
def check_current_system():
    """Проверяем текущую систему в коде"""
    print("\n🔧 ПРОВЕРКА ТЕКУЩЕЙ СИСТЕМЫ:")
    print("=" * 40)
    
    try:
        import sys, os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        from telegram_test_bot import DISC_QUESTIONS
        
        print(f"📊 Загружено {len(DISC_QUESTIONS)} DISC вопросов")
        
        # Подсчитываем вопросы по категориям
        category_count = {"D": 0, "I": 0, "S": 0, "C": 0}
        
        for i, q in enumerate(DISC_QUESTIONS):
            if 'category' in q:
                category = q['category']
                category_count[category] += 1
                print(f"   Вопрос {i+1}: {q['category']} - {q['question'][:50]}...")
            else:
                print(f"   Вопрос {i+1}: Старый формат - {list(q.get('answers', {}).keys())}")
        
        print(f"\n📈 Распределение по категориям:")
        for category, count in category_count.items():
            print(f"   {category}: {count} вопросов")
        
        return category_count
        
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return None

if __name__ == "__main__":
    explain_disc_methodology()
    explain_key_points()
    explain_your_results()
    check_current_system()