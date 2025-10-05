#!/usr/bin/env python3
"""
Функция для генерации AI интерпретаций согласно обновленному general_system_res.txt
Работает без API ключа, используя шаблоны из промпта
"""

from pathlib import Path
import datetime

def generate_ai_interpretations_from_prompt(paei_scores, disc_scores, hexaco_scores, soft_skills_scores):
    """
    Генерирует AI интерпретации согласно формату из general_system_res.txt
    """
    
    # Определяем доминирующие характеристики
    paei_max = max(paei_scores, key=paei_scores.get)
    paei_roles = {'P': 'Производитель', 'A': 'Администратор', 'E': 'Предприниматель', 'I': 'Интегратор'}
    dominant_paei_role = paei_roles[paei_max]
    
    disc_max = max(disc_scores, key=disc_scores.get)
    disc_styles = {'D': 'Доминирование', 'I': 'Влияние', 'S': 'Стабильность', 'C': 'Точность'}
    dominant_disc_style = disc_styles[disc_max]
    
    hexaco_max = max(hexaco_scores, key=hexaco_scores.get)
    
    soft_max = max(soft_skills_scores, key=soft_skills_scores.get)
    
    # Находим слабые стороны для развития
    weak_paei = [paei_roles[role] for role, score in paei_scores.items() if score < 6]
    weak_skills = [skill for skill, score in soft_skills_scores.items() if score < 8.0]
    
    # Формируем интерпретации согласно новому формату
    ai_interpretations = {
        'paei': f'''Преобладающий профиль {dominant_paei_role} ({paei_scores[paei_max]} баллов) указывает на ориентацию на результат и эффективность в работе.

РЕКОМЕНДАЦИИ ПО ПРОФЕССИОНАЛЬНОМУ РАЗВИТИЮ:

1. Использование сильных сторон:
    • (PAEI): Делегировать задачи, соответствующие профилю {dominant_paei_role}
    • (Soft Skills): Развивать {soft_max} через специализированные проекты
    • (DISC): Использовать {dominant_disc_style} в командном взаимодействии

2. Области для развития:
    • (PAEI): Работать над менее выраженными управленческими ролями {', '.join(weak_paei) if weak_paei else 'Администратор'}
    • (Soft Skills): Развивать дополнительные soft skills для универсальности {weak_skills} [поиск курсов в Google]
    • (DISC): Балансировать поведенческий стиль в зависимости от ситуации

3. Карьерные перспективы:
    • (PAEI): Рассмотреть позиции, требующие качеств {dominant_paei_role}
    • (HEXACO): Планировать развитие с учетом личностного профиля HEXACO
    • (DISC): Выстраивать команду с учетом комплементарных ролей по DISC''',
        
        'soft_skills': f'Наиболее развитый навык {soft_max} ({soft_skills_scores[soft_max]} баллов) является сильной стороной для профессионального развития.',
        
        'hexaco': f'Доминирующая черта личности по модели HEXACO показывает сбалансированный профиль с акцентом на определенные аспекты поведения.',
        
        'disc': f'Поведенческий стиль {dominant_disc_style} ({disc_scores[disc_max]} баллов) определяет подход к решению задач и взаимодействию в команде.',
        
        'general': '''Общий портрет личности:
Этот человек демонстрирует комплексный профиль с выраженными сильными сторонами и областями для развития. Рекомендации сформированы с учетом современных методик психологической оценки и включают конкретные направления для профессионального роста.'''
    }
    
    return ai_interpretations

def test_corrected_format_pdf():
    """Создает PDF с правильным форматом согласно general_system_res.txt"""
    
    print("🎯 ГЕНЕРАЦИЯ PDF С ПРАВИЛЬНЫМ ФОРМАТОМ")
    print("=" * 50)
    print()
    
    # Тестовые данные
    test_data = {
        'paei_scores': {'P': 8, 'A': 5, 'E': 7, 'I': 6},
        'disc_scores': {'D': 7, 'I': 5, 'S': 3, 'C': 4},
        'hexaco_scores': {'H': 4, 'E': 3, 'X': 5, 'A': 4, 'C': 5, 'O': 3},
        'soft_skills_scores': {
            'Коммуникация': 8.5,
            'Лидерство': 9.0,
            'Критическое мышление': 6.5,
            'Креативность': 7.2,
            'Работа в команде': 8.8,
            'Адаптивность': 8.1,
            'Эмоциональный интеллект': 9.2,
            'Решение проблем': 7.8,
            'Управление временем': 8.5,
            'Презентационные навыки': 7.0
        }
    }
    
    # Генерируем AI интерпретации согласно обновленному промпту
    print("🧠 Генерация AI интерпретаций согласно general_system_res.txt...")
    ai_interpretations = generate_ai_interpretations_from_prompt(
        test_data['paei_scores'],
        test_data['disc_scores'], 
        test_data['hexaco_scores'],
        test_data['soft_skills_scores']
    )
    
    print("✅ Интерпретации сформированы с новым форматом!")
    print()
    
    # Показываем ключевые элементы нового формата
    print("🔍 КЛЮЧЕВЫЕ ЭЛЕМЕНТЫ НОВОГО ФОРМАТА:")
    print("    ✅ Аббревиатуры методов: (PAEI):, (Soft Skills):, (DISC):, (HEXACO):")
    print("    ✅ Квадратные скобки: [поиск курсов в Google]")
    print("    ✅ Конкретные навыки для развития")
    print("    ✅ Структурированные рекомендации")
    print()
    
    # Создаем PDF
    from enhanced_pdf_report_v2 import EnhancedPDFReportV2
    generator = EnhancedPDFReportV2()
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = Path(f'corrected_format_{timestamp}.pdf')
    
    print(f"📄 Создание PDF: {output_path}")
    
    # Загружаем в Google Drive
    drive_url = generator.generate_enhanced_report_with_gdrive(
        'Исправленный Формат Согласно Промпту',
        '2025-10-04',
        test_data['paei_scores'],
        test_data['disc_scores'], 
        test_data['hexaco_scores'],
        test_data['soft_skills_scores'],
        ai_interpretations,
        output_path
    )
    
    print("✅ PDF создан с ИСПРАВЛЕННЫМ форматом!")
    print()
    
    if isinstance(drive_url, tuple):
        print(f"🔗 Google Drive: {drive_url[1]}")
    else:
        print(f"🔗 Google Drive: {drive_url}")
    
    print(f"📁 Локальный файл: {output_path}")
    print()
    
    # Показываем фрагмент рекомендаций
    print("📝 ФРАГМЕНТ РЕКОМЕНДАЦИЙ (новый формат):")
    recommendations = ai_interpretations['paei'].split('РЕКОМЕНДАЦИИ ПО ПРОФЕССИОНАЛЬНОМУ РАЗВИТИЮ:')[1][:400]
    print(recommendations[:400] + "...")
    print()
    print("🎉 ГОТОВО! Теперь PDF использует правильный формат из general_system_res.txt")

if __name__ == "__main__":
    test_corrected_format_pdf()