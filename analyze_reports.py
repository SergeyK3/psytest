"""
Анализ качества сгенерированных AI отчётов
Сравнивает характеристики отчётов с ожиданиями для каждого профиля
"""

import os
import sys
from pathlib import Path

# Добавляем путь к src для импорта
sys.path.insert(0, str(Path(__file__).parent / "src"))

from test_scenarios import TEST_SCENARIOS

def analyze_report_quality():
    """Анализирует качество всех сгенерированных отчётов"""
    
    reports_dir = Path(__file__).parent / "test_reports"
    
    print("📊 Анализ качества сгенерированных отчётов")
    print("=" * 60)
    
    # Проверяем каждый сценарий
    for scenario_name, scenario_data in TEST_SCENARIOS.items():
        report_path = reports_dir / f"report_{scenario_name}.txt"
        
        if not report_path.exists():
            print(f"❌ Отчёт для {scenario_name} не найден")
            continue
            
        print(f"\n🔍 Анализ: {scenario_data['name']}")
        print(f"📝 Описание: {scenario_data['description']}")
        
        # Читаем отчёт
        with open(report_path, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        # Анализ структуры отчёта
        analyze_report_structure(report_content, scenario_data)
        
        # Анализ соответствия профилю
        analyze_profile_match(report_content, scenario_data)

def analyze_report_structure(content: str, scenario_data: dict):
    """Анализирует структуру отчёта"""
    
    required_sections = [
        "Общие данные о сотруднике",
        "Классификация по Адизесу",
        "ТЕСТ DISC",
        "ТЕСТ HEXACO",
        "Powered by OpenAI"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"  ⚠️  Отсутствующие разделы: {', '.join(missing_sections)}")
    else:
        print("  ✅ Структура отчёта полная")
    
    # Проверяем длину отчёта
    word_count = len(content.split())
    if word_count < 200:
        print(f"  ⚠️  Отчёт слишком короткий: {word_count} слов")
    elif word_count > 1000:
        print(f"  ⚠️  Отчёт слишком длинный: {word_count} слов")
    else:
        print(f"  ✅ Объём отчёта оптимальный: {word_count} слов")

def analyze_profile_match(content: str, scenario_data: dict):
    """Анализирует соответствие отчёта профилю личности"""
    
    # Ключевые слова для разных типов профилей
    profile_keywords = {
        "manager_leader": ["лидер", "руководитель", "ответственность", "результат", "контроль"],
        "creative_innovator": ["творчест", "креатив", "иннова", "идеи", "новое"],
        "stable_supporter": ["стабиль", "порядок", "правила", "системн", "надёжн"],
        "team_integrator": ["команд", "интеграц", "сотрудничест", "эмпати", "гармони"],
        "analytical_perfectionist": ["анализ", "детали", "точност", "качество", "стандарт"],
        "balanced_universal": ["сбаланс", "универсал", "адаптац", "гибкос", "разносторон"]
    }
    
    # Определяем тип профиля
    profile_type = None
    for scenario_name, _ in TEST_SCENARIOS.items():
        if scenario_name in content or any(keyword in scenario_data['name'].lower() for keyword in scenario_name.split('_')):
            profile_type = scenario_name
            break
    
    if not profile_type:
        # Пытаемся определить по имени файла/содержимому
        for scenario_name in TEST_SCENARIOS.keys():
            if scenario_name in str(content).lower():
                profile_type = scenario_name
                break
    
    if profile_type and profile_type in profile_keywords:
        keywords = profile_keywords[profile_type]
        found_keywords = []
        
        content_lower = content.lower()
        for keyword in keywords:
            if keyword in content_lower:
                found_keywords.append(keyword)
        
        keyword_score = len(found_keywords) / len(keywords) * 100
        
        if keyword_score >= 60:
            print(f"  ✅ Соответствие профилю: {keyword_score:.1f}% (найдены ключевые слова: {', '.join(found_keywords)})")
        elif keyword_score >= 30:
            print(f"  ⚠️  Частичное соответствие профилю: {keyword_score:.1f}%")
        else:
            print(f"  ❌ Слабое соответствие профилю: {keyword_score:.1f}%")
    else:
        print("  ⚠️  Не удалось определить тип профиля для анализа")

def generate_summary_report():
    """Генерирует сводный отчёт по всем профилям"""
    
    reports_dir = Path(__file__).parent / "test_reports"
    
    print("\n" + "=" * 60)
    print("📋 СВОДКА ПО ВСЕМ ПРОФИЛЯМ")
    print("=" * 60)
    
    total_reports = len(TEST_SCENARIOS)
    existing_reports = len(list(reports_dir.glob("*.txt")))
    
    print(f"📊 Статистика:")
    print(f"  • Всего профилей: {total_reports}")
    print(f"  • Сгенерировано отчётов: {existing_reports}")
    print(f"  • Процент завершения: {existing_reports/total_reports*100:.1f}%")
    
    print(f"\n🎯 Типы профилей:")
    for scenario_name, scenario_data in TEST_SCENARIOS.items():
        status = "✅" if (reports_dir / f"report_{scenario_name}.txt").exists() else "❌"
        print(f"  {status} {scenario_data['name']} - {scenario_data['description']}")
    
    print(f"\n💡 Рекомендации:")
    print("  • Проверьте соответствие интерпретаций профилям личности")
    print("  • Убедитесь в наличии всех обязательных разделов")
    print("  • Сравните с примером 'Психологический портрет КимСВ.docx'")

def main():
    """Основная функция анализа"""
    analyze_report_quality()
    generate_summary_report()

if __name__ == "__main__":
    main()