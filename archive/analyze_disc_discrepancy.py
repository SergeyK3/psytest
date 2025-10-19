#!/usr/bin/env python3
"""
Анализ несоответствия в результатах DISC
D=32, I=20, S=28, C=24 при 8 вопросах по 2 на категорию
"""

def analyze_disc_discrepancy():
    """Анализируем несоответствие в DISC результатах"""
    print("🔍 АНАЛИЗ НЕСООТВЕТСТВИЯ DISC РЕЗУЛЬТАТОВ")
    print("=" * 50)
    
    # Ваши результаты
    your_results = {"D": 32, "I": 20, "S": 28, "C": 24}
    total = sum(your_results.values())
    
    # Текущая система: 8 вопросов, по 2 на категорию
    current_system = {
        "questions_total": 8,
        "questions_per_category": 2,
        "scale": "1-5",
        "expected_min_per_category": 2,  # 2 вопроса × 1 балл
        "expected_max_per_category": 10  # 2 вопроса × 5 баллов
    }
    
    print("📊 Ваши результаты:")
    print(f"   D = {your_results['D']} баллов")
    print(f"   I = {your_results['I']} баллов")  
    print(f"   S = {your_results['S']} баллов")
    print(f"   C = {your_results['C']} баллов")
    print(f"   Всего: {total} баллов")
    
    print("\n📋 Текущая система:")
    print(f"   • {current_system['questions_total']} вопросов всего")
    print(f"   • {current_system['questions_per_category']} вопроса на категорию")
    print(f"   • Шкала: {current_system['scale']} баллов")
    print(f"   • Ожидаемый диапазон: {current_system['expected_min_per_category']}-{current_system['expected_max_per_category']} баллов на категорию")
    
    print("\n❗ ПРОБЛЕМА:")
    print(f"   Ваши результаты превышают максимум!")
    for category, score in your_results.items():
        if score > current_system['expected_max_per_category']:
            excess = score - current_system['expected_max_per_category']
            print(f"   • {category}: {score} > {current_system['expected_max_per_category']} (превышение на {excess})")
    
    print("\n🤔 ВОЗМОЖНЫЕ ПРИЧИНЫ:")
    
    # Гипотеза 1: Больше вопросов на категорию
    estimated_questions_per_cat = max(your_results.values()) / 5  # Если все ответы были 5
    print(f"\n1. Больше вопросов на категорию:")
    print(f"   • Если максимальные ответы (все по 5): {estimated_questions_per_cat:.1f} вопросов на категорию")
    print(f"   • D=32: нужно {32/5:.1f} = 6-7 вопросов с ответом 5")
    
    # Гипотеза 2: Другая система подсчета
    print(f"\n2. Старая система подсчета:")
    print(f"   • Возможно, использовалась накопительная система")
    print(f"   • Или каждый ответ влиял на несколько категорий")
    
    # Гипотеза 3: Данные из другого теста
    if total > 40:
        alternative_questions = total / 20  # Если средний ответ 2.5
        print(f"\n3. Альтернативная интерпретация:")
        print(f"   • При среднем ответе 2.5: {alternative_questions:.0f} вопросов на категорию")
        print(f"   • Возможно, это результаты из другой версии теста")

def compare_old_vs_new_system():
    """Сравниваем старую и новую систему"""
    print("\n🔄 СРАВНЕНИЕ СИСТЕМ:")
    print("=" * 30)
    
    print("❌ СТАРАЯ СИСТЕМА (до исправления):")
    print("   • Применялась нормализация 1-10")
    print("   • Формула: 1 + (score/total) * 9")
    print("   • Результат: D=3.7, I=2.7, S=3.0, C=3.7")
    
    print("\n✅ НОВАЯ СИСТЕМА (после исправления):")
    print("   • Сырые баллы без нормализации")
    print("   • Прямая сумма ответов по категориям")
    print("   • Результат: D=32, I=20, S=28, C=24")
    
    print("\n🎯 ВОПРОС: Откуда взялись числа 32, 20, 28, 24?")
    
    # Проверим, могли ли это быть результаты старой системы
    your_results = {"D": 32, "I": 20, "S": 28, "C": 24}
    total = sum(your_results.values())
    
    print(f"\n🧮 Обратный расчет:")
    if total > 0:
        # Если это были нормализованные результаты в шкале 1-10, 
        # то оригинальные пропорции:
        proportions = {k: v/total for k, v in your_results.items()}
        print("   Пропорции от общей суммы:")
        for category, prop in proportions.items():
            print(f"   • {category}: {prop:.3f} ({prop*100:.1f}%)")
        
        # Если применить старую формулу наоборот
        print("\n   Если это результат старой нормализации:")
        for category, score in your_results.items():
            # score = 1 + (original/total_original) * 9
            # original/total_original = (score - 1) / 9
            if score >= 1:
                old_proportion = (score - 1) / 9
                print(f"   • {category}: пропорция была {old_proportion:.3f}")

def recommendation():
    """Рекомендации по решению"""
    print("\n💡 РЕКОМЕНДАЦИИ:")
    print("=" * 20)
    
    print("1. 🔍 Проверить источник данных:")
    print("   • Откуда взяты числа D=32, I=20, S=28, C=24?")
    print("   • Это результат реального тестирования?")
    print("   • Или тестовые данные из старой системы?")
    
    print("\n2. ✅ Протестировать текущую систему:")
    print("   • Пройти тест заново с текущими 8 вопросами")
    print("   • Ожидаемый диапазон: 2-10 баллов на категорию")
    print("   • Проверить, что система работает правильно")
    
    print("\n3. 📊 Сравнить с ожидаемыми результатами:")
    print("   • Текущая система: D/I/S/C от 2 до 10")
    print("   • Если получаются другие числа - искать причину")

if __name__ == "__main__":
    analyze_disc_discrepancy()
    compare_old_vs_new_system()
    recommendation()