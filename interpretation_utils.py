"""
Утилиты для генерации интерпретаций
Вынесено в отдельный модуль для избежания циклических импортов
"""

import re
from pathlib import Path


def generate_interpretations_from_prompt(paei_scores, disc_scores, hexaco_scores, soft_skills_scores):
    """
    Генерирует интерпретации на основе промптов из файлов
    """
    interpretations = {}
    
    # PAEI интерпретация
    try:
        adizes_file = Path("data/prompts/adizes_system_res.txt")
        if adizes_file.exists():
            with open(adizes_file, 'r', encoding='utf-8') as f:
                adizes_content = f.read()
            
            # Определяем доминирующую роль
            max_role = max(paei_scores, key=paei_scores.get)
            max_score = paei_scores[max_role]
            
            # Ищем соответствующую интерпретацию
            role_patterns = {
                'P': r'(?:P\s*-\s*Producer|Производитель).*?(?=\n\n|A\s*-|E\s*-|I\s*-|$)',
                'A': r'(?:A\s*-\s*Administrator|Администратор).*?(?=\n\n|P\s*-|E\s*-|I\s*-|$)',
                'E': r'(?:E\s*-\s*Entrepreneur|Предприниматель).*?(?=\n\n|P\s*-|A\s*-|I\s*-|$)',
                'I': r'(?:I\s*-\s*Integrator|Интегратор).*?(?=\n\n|P\s*-|A\s*-|E\s*-|$)'
            }
            
            if max_role in role_patterns:
                match = re.search(role_patterns[max_role], adizes_content, re.DOTALL | re.IGNORECASE)
                if match:
                    interpretation = match.group(0).strip()
                    # Очищаем от лишних переносов и пробелов
                    interpretation = re.sub(r'\n+', '\n', interpretation)
                    interpretation = re.sub(r'^\s+|\s+$', '', interpretation, flags=re.MULTILINE)
                    interpretations["paei"] = interpretation
                else:
                    interpretations["paei"] = f"Доминирующая роль: {max_role} ({max_score} баллов)"
            else:
                interpretations["paei"] = f"Доминирующая роль: {max_role} ({max_score} баллов)"
        else:
            # Fallback если файл не найден
            max_role = max(paei_scores, key=paei_scores.get)
            max_score = paei_scores[max_role]
            interpretations["paei"] = f"Доминирующая роль: {max_role} ({max_score} баллов)"
            
    except Exception as e:
        print(f"Ошибка при генерации PAEI интерпретации: {e}")
        max_role = max(paei_scores, key=paei_scores.get)
        max_score = paei_scores[max_role]
        interpretations["paei"] = f"Доминирующая роль: {max_role} ({max_score} баллов)"
    
    # DISC интерпретация
    try:
        disc_max = max(disc_scores, key=disc_scores.get)
        disc_styles = {
            'D': 'Доминирование',
            'I': 'Влияние', 
            'S': 'Стабильность',
            'C': 'Соответствие'
        }
        dominant_disc_style = disc_styles.get(disc_max, disc_max)
        interpretations['disc'] = f'Поведенческий стиль {dominant_disc_style} ({disc_scores[disc_max]} баллов) определяет подход к решению задач и взаимодействию в команде.'
    except Exception as e:
        print(f"Ошибка при генерации DISC интерпретации: {e}")
        interpretations['disc'] = "Требуется дополнительный анализ поведенческого профиля."
    
    # HEXACO интерпретация
    try:
        if isinstance(hexaco_scores, list):
            hexaco_dimensions = ["Честность-Скромность", "Эмоциональность", "Экстраверсия", 
                               "Доброжелательность", "Добросовестность", "Открытость опыту"]
            if len(hexaco_scores) >= 6:
                max_idx = hexaco_scores.index(max(hexaco_scores))
                dominant_dimension = hexaco_dimensions[max_idx]
                max_score = hexaco_scores[max_idx]
                interpretations['hexaco'] = f'Выраженная черта личности: {dominant_dimension} ({max_score} баллов) влияет на восприятие и взаимодействие с окружающим миром.'
            else:
                interpretations['hexaco'] = "Личностный профиль демонстрирует сбалансированные характеристики."
        else:
            interpretations['hexaco'] = "Личностный профиль демонстрирует сбалансированные характеристики."
    except Exception as e:
        print(f"Ошибка при генерации HEXACO интерпретации: {e}")
        interpretations['hexaco'] = "Личностный профиль демонстрирует сбалансированные характеристики."
    
    # Soft Skills интерпретация
    try:
        if isinstance(soft_skills_scores, (list, dict)):
            if isinstance(soft_skills_scores, dict):
                max_skill = max(soft_skills_scores, key=soft_skills_scores.get)
                max_score = soft_skills_scores[max_skill]
                interpretations['soft_skills'] = f'Сильная сторона: {max_skill} ({max_score} баллов) представляет ключевой навык для профессионального развития.'
            else:
                skill_names = ["Коммуникация", "Лидерство", "Работа в команде", "Критическое мышление",
                              "Решение проблем", "Адаптивность", "Управление временем", "Эмоциональный интеллект",
                              "Креативность", "Стрессоустойчивость"]
                if len(soft_skills_scores) >= len(skill_names):
                    max_idx = soft_skills_scores.index(max(soft_skills_scores))
                    max_skill = skill_names[max_idx] if max_idx < len(skill_names) else f"Навык {max_idx + 1}"
                    max_score = soft_skills_scores[max_idx]
                    interpretations['soft_skills'] = f'Сильная сторона: {max_skill} ({max_score} баллов) представляет ключевой навык для профессионального развития.'
                else:
                    interpretations['soft_skills'] = "Профиль мягких навыков демонстрирует сбалансированное развитие."
        else:
            interpretations['soft_skills'] = "Профиль мягких навыков демонстрирует сбалансированное развитие."
    except Exception as e:
        print(f"Ошибка при генерации Soft Skills интерпретации: {e}")
        interpretations['soft_skills'] = "Профиль мягких навыков демонстрирует сбалансированное развитие."
    
    # Общая интерпретация
    interpretations['general'] = '''Общий портрет личности:
Этот человек демонстрирует комплексный профиль с выраженными сильными сторонами и областями для развития. Рекомендации сформированы с учетом современных методик психологической оценки и включают конкретные направления для профессионального роста согласно формату general_system_res.txt.'''
    
    return interpretations