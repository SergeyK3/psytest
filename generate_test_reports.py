"""
Скрипт для генерации тестовых отчётов по всем сценариям
Создаёт полные психологические портреты с AI интерпретациями
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Добавляем путь к src для импорта
sys.path.insert(0, str(Path(__file__).parent / "src"))

from test_scenarios import TEST_SCENARIOS, convert_hexaco_scores, convert_disc_scores
from psytest.ai_interpreter import get_ai_interpreter
from psytest.portrait import combine_blocks, save_text

def load_env_vars():
    """Загружает переменные окружения из .env файла"""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def generate_scenario_report(scenario_name: str, scenario_data: dict, ai_interpreter):
    """Генерирует полный отчёт для одного сценария"""
    
    print(f"\n🔄 Генерируется отчёт для: {scenario_data['name']}")
    
    # Извлекаем только имя без типажа в скобках
    full_name = scenario_data['name']
    if '(' in full_name and ')' in full_name:
        clean_name = full_name.split('(')[0].strip()
    else:
        clean_name = full_name
    
    # Блок общих данных
    general_block = f"""Общие данные о сотруднике

Имя сотрудника: {clean_name}
Описание: {scenario_data['description']}
Дата тестирования: {datetime.now().strftime('%Y-%m-%d %H:%M')}"""

    # Блок PAEI (Адизес)
    print("  📊 Генерация интерпретации PAEI...")
    paei_interpretation = ai_interpreter.interpret_paei(
        scenario_data['paei_scores'], 
        scenario_data['dialog_context']
    )
    
    # Блок DISC
    print("  📊 Генерация интерпретации DISC...")
    disc_scores_full = convert_disc_scores(scenario_data['disc_scores'])
    disc_interpretation = ai_interpreter.interpret_disc(
        disc_scores_full,
        scenario_data['dialog_context']
    )
    
    # Блок HEXACO
    print("  📊 Генерация интерпретации HEXACO...")
    hexaco_scores_full = convert_hexaco_scores(scenario_data['hexaco_scores'])
    hexaco_interpretation = ai_interpreter.interpret_hexaco(
        hexaco_scores_full,
        scenario_data['dialog_context']
    )
    
    # Объединяем все блоки
    full_report = combine_blocks([
        general_block,
        paei_interpretation,
        disc_interpretation,
        hexaco_interpretation
    ])
    
    # Добавляем информацию об AI
    full_report += "\n\n" + "="*50
    full_report += "\n🤖 Интерпретации сгенерированы с помощью OpenAI GPT-3.5"
    full_report += "\nPowered by OpenAI (https://openai.com)"
    full_report += "\n" + "="*50
    
    return full_report

def main():
    """Основная функция генерации всех отчётов"""
    
    print("🚀 Запуск генерации тестовых отчётов...")
    
    # Загружаем переменные окружения
    load_env_vars()
    
    # Создаём AI интерпретатор
    ai_interpreter = get_ai_interpreter()
    if not ai_interpreter:
        print("❌ Не удалось создать AI интерпретатор")
        print("Проверьте настройки OPENAI_API_KEY в .env файле")
        return
    
    print(f"✅ AI интерпретатор готов. Модель: {ai_interpreter.model}")
    
    # Создаём папку для отчётов
    reports_dir = Path(__file__).parent / "test_reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Генерируем отчёты для всех сценариев
    for scenario_name, scenario_data in TEST_SCENARIOS.items():
        try:
            # Генерируем отчёт
            report_content = generate_scenario_report(scenario_name, scenario_data, ai_interpreter)
            
            # Сохраняем отчёт
            report_filename = f"report_{scenario_name}.txt"
            report_path = reports_dir / report_filename
            save_text(report_content, report_path)
            
            print(f"  ✅ Отчёт сохранён: {report_path}")
            
        except Exception as e:
            print(f"  ❌ Ошибка при генерации отчёта для {scenario_name}: {e}")
    
    print(f"\n🎉 Генерация завершена! Отчёты сохранены в папке: {reports_dir}")
    print(f"📝 Всего сгенерировано отчётов: {len(TEST_SCENARIOS)}")
    
    # Показываем список созданных файлов
    print("\n📂 Созданные файлы:")
    for report_file in sorted(reports_dir.glob("*.txt")):
        print(f"  • {report_file.name}")

if __name__ == "__main__":
    main()