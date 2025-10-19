#!/usr/bin/env python3
"""
Анализ оптимальной шкалы для DISC - 1-5 vs 2-10 vs среднее значение
"""

def analyze_disc_scale_options():
    """Анализируем различные варианты шкалы DISC"""
    print("🎯 АНАЛИЗ ОПТИМАЛЬНОЙ ШКАЛЫ DISC")
    print("=" * 50)
    
    # Пример данных: пользователь прошел 8 вопросов, по 2 на категорию
    example_answers = {
        "D": [4, 5],  # Два вопроса по доминированию: 4 и 5 баллов
        "I": [2, 3],  # Два вопроса по влиянию: 2 и 3 балла
        "S": [3, 4],  # Два вопроса по постоянству: 3 и 4 балла
        "C": [5, 4]   # Два вопроса по соответствию: 5 и 4 балла
    }
    
    print("📝 Пример ответов пользователя:")
    for category, answers in example_answers.items():
        print(f"   {category}: {answers} (ответы на 2 вопроса)")
    
    print("\n📊 ВАРИАНТЫ ПРЕДСТАВЛЕНИЯ РЕЗУЛЬТАТОВ:")
    print("-" * 50)
    
    # Вариант 1: Сумма (текущая система)
    print("1️⃣ СУММА БАЛЛОВ (текущая система):")
    sums = {cat: sum(answers) for cat, answers in example_answers.items()}
    for category, total in sums.items():
        print(f"   {category}: {total}/10 (диапазон 2-10)")
    print("   👍 Плюсы: Показывает общую силу по категории")
    print("   👎 Минусы: Непривычная шкала, зависит от количества вопросов")
    
    # Вариант 2: Среднее значение
    print("\n2️⃣ СРЕДНЕЕ ЗНАЧЕНИЕ (рекомендуемый):")
    averages = {cat: round(sum(answers) / len(answers), 1) for cat, answers in example_answers.items()}
    for category, avg in averages.items():
        print(f"   {category}: {avg}/5.0 (диапазон 1.0-5.0)")
    print("   👍 Плюсы: Привычная шкала 1-5, легко понимать")
    print("   👍 Плюсы: Не зависит от количества вопросов")
    print("   👍 Плюсы: Соответствует исходной шкале ответов")
    
    # Вариант 3: Процентная шкала
    print("\n3️⃣ ПРОЦЕНТНАЯ ШКАЛА:")
    percentages = {cat: round((sum(answers) / (len(answers) * 5)) * 100, 1) for cat, answers in example_answers.items()}
    for category, pct in percentages.items():
        print(f"   {category}: {pct}% (диапазон 20%-100%)")
    print("   👍 Плюсы: Интуитивно понятно")
    print("   👎 Минусы: Неестественный минимум 20%")

def check_current_implementation():
    """Проверяем текущую реализацию"""
    print("\n🔧 ТЕКУЩАЯ РЕАЛИЗАЦИЯ:")
    print("=" * 30)
    
    try:
        import sys, os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        from telegram_test_bot import DISC_QUESTIONS
        
        print(f"📊 Количество DISC вопросов: {len(DISC_QUESTIONS)}")
        
        # Подсчитываем вопросы по категориям
        category_count = {"D": 0, "I": 0, "S": 0, "C": 0}
        for q in DISC_QUESTIONS:
            if 'category' in q:
                category_count[q['category']] += 1
        
        print("📈 Распределение вопросов:")
        for category, count in category_count.items():
            print(f"   {category}: {count} вопросов")
        
        if all(count == 2 for count in category_count.values()):
            print("\n✅ Система сбалансирована: по 2 вопроса на категорию")
            print("💡 Рекомендация: использовать СРЕДНЕЕ ЗНАЧЕНИЕ (1-5)")
        else:
            print("\n⚠️ Система несбалансирована!")
            print("💡 Рекомендация: либо сбалансировать, либо использовать среднее")
        
        return category_count
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def recommend_implementation():
    """Рекомендации по реализации"""
    print("\n💡 РЕКОМЕНДАЦИИ:")
    print("=" * 20)
    
    print("✅ ЛУЧШИЙ ВАРИАНТ: Среднее значение 1-5")
    print("   • Легко понимать пользователям")
    print("   • Соответствует шкале ответов")
    print("   • Не зависит от количества вопросов")
    print("   • Стандарт в психологии")
    
    print("\n🔧 ИЗМЕНЕНИЯ В КОДЕ:")
    print("1. В telegram_test_bot.py:")
    print("   • Вместо сохранения суммы сохранять среднее")
    print("   • disc_scores[category] = sum / count")
    
    print("\n2. В диаграммах:")
    print("   • Изменить max_value с 10 на 5")
    print("   • Обновить подписи осей")
    
    print("\n3. В scale_normalizer.py:")
    print("   • Обновить комментарии о диапазоне")

def simulation_average_system():
    """Симуляция системы со средними значениями"""
    print("\n🧪 СИМУЛЯЦИЯ НОВОЙ СИСТЕМЫ:")
    print("=" * 35)
    
    # Различные сценарии ответов
    scenarios = {
        "Высокое доминирование": {"D": [5, 5], "I": [2, 1], "S": [3, 2], "C": [4, 3]},
        "Сбалансированный": {"D": [3, 4], "I": [3, 3], "S": [3, 4], "C": [3, 3]},
        "Высокое влияние": {"D": [2, 1], "I": [5, 4], "S": [2, 3], "C": [2, 2]}
    }
    
    for name, answers in scenarios.items():
        print(f"\n📊 Сценарий: {name}")
        averages = {}
        for category, scores in answers.items():
            avg = sum(scores) / len(scores)
            averages[category] = round(avg, 1)
            print(f"   {category}: {scores} → среднее {avg:.1f}/5.0")
        
        # Показываем профиль
        dominant = max(averages.items(), key=lambda x: x[1])
        print(f"   🎯 Доминирующий стиль: {dominant[0]} ({dominant[1]}/5.0)")

if __name__ == "__main__":
    analyze_disc_scale_options()
    check_current_implementation()
    recommend_implementation()
    simulation_average_system()