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
            
            # Создаем базовый блок PAEI с результатами
            paei_results = []
            for role, score in paei_scores.items():
                role_names = {'P': 'Производитель', 'A': 'Администратор', 'E': 'Предприниматель', 'I': 'Интегратор'}
                paei_results.append(f"{role_names[role]} - {score}")
            
            # Определяем тип профиля для выбора подходящего примера
            scores_list = list(paei_scores.values())
            max_val = max(scores_list)
            min_val = min(scores_list)
            
            # Если разброс небольшой (разница <= 1) - сбалансированный профиль
            if max_val - min_val <= 1:
                pattern = r'пример 2 - сбалансированный профиль.*?"(.*?)"'
                interpretation_type = "сбалансированный"
            # Если есть явная доминирующая роль I (Интегратор)
            elif max_role == 'I' and max_score >= max_val:
                pattern = r'пример 1 - доминирующий Интегратор.*?"(.*?)"'
                interpretation_type = "доминирующий Интегратор"
            # Для остальных доминирующих ролей (P, A, E) используем пример Предпринимателя 
            # но адаптируем под конкретную роль
            else:
                pattern = r'пример 3 - доминирующий Предприниматель.*?"(.*?)"'
                interpretation_type = f"доминирующий {role_names.get(max_role, max_role)}"
            
            # Ищем интерпретацию
            match = re.search(pattern, adizes_content, re.DOTALL | re.IGNORECASE)
            if match:
                interpretation_text = match.group(1).strip()
                
                # Адаптируем текст под реальную доминирующую роль (если не Интегратор и не сбалансированный)
                if max_role != 'I' and interpretation_type != "сбалансированный":
                    role_adaptations = {
                        'P': {'old': 'Предприниматель (E)', 'new': 'Производитель (P)', 
                              'desc': 'ориентацию на результат, выполнение задач и достижение конкретных целей'},
                        'A': {'old': 'Предприниматель (E)', 'new': 'Администратор (A)', 
                              'desc': 'стремление к порядку, контролю, структурированности и соблюдению правил'},
                        'E': {'old': 'Предприниматель (E)', 'new': 'Предприниматель (E)', 
                              'desc': 'ориентацию на инновации, изменения и долгосрочное видение'}
                    }
                    
                    if max_role in role_adaptations:
                        adaptation = role_adaptations[max_role]
                        interpretation_text = interpretation_text.replace(adaptation['old'], adaptation['new'])
                        interpretation_text = interpretation_text.replace('инновации, изменения и долгосрочное видение', adaptation['desc'])
                
                # Формируем полную интерпретацию с результатами и описанием
                full_interpretation = "\n".join(paei_results) + "\n\n" + interpretation_text
                interpretations["paei"] = full_interpretation
            else:
                # Fallback - используем первый найденный пример
                fallback_match = re.search(r'Образец блока.*?"(.*?)"', adizes_content, re.DOTALL | re.IGNORECASE)
                if fallback_match:
                    interpretation_text = fallback_match.group(1).strip()
                    full_interpretation = "\n".join(paei_results) + "\n\n" + interpretation_text
                    interpretations["paei"] = full_interpretation
                else:
                    interpretations["paei"] = "\n".join(paei_results) + f"\n\nДоминирующая роль: {max_role} ({max_score} баллов)"
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
        # Ищем детальную интерпретацию DISC из CSV файла
        disc_file = Path("data/interpretations/interpretations_disc.csv")
        if disc_file.exists():
            import csv
            
            interpretations_text = []
            interpretations_text.append("**DISC Профиль:**\n")
            
            # Читаем интерпретации из CSV
            disc_interpretations = {}
            with open(disc_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    scale = row['scale']
                    range_low = int(row['range_low'])
                    range_high = int(row['range_high'])
                    level = row['level']
                    text = row['text']
                    
                    if scale not in disc_interpretations:
                        disc_interpretations[scale] = []
                    disc_interpretations[scale].append({
                        'range_low': range_low,
                        'range_high': range_high,
                        'level': level,
                        'text': text
                    })
            
            # Полные названия DISC для формата "Сумма баллов по..."
            disc_full_names = {
                'D': 'доминированию',
                'I': 'влиянию',
                'S': 'устойчивости',
                'C': 'подчинению правилам'
            }
            
            # Создаём начальную секцию с баллами
            interpretations_text.append("ТЕСТ DISC:")
            interpretations_text.append("")
            
            # Преобразуем баллы к шкале 0-60 для поиска интерпретации
            for scale_key, score in disc_scores.items():
                # Нормализуем к шкале 0-60 (если score в диапазоне 0-10)
                if score <= 10:
                    normalized_score = score * 6  # 10 баллов = 60 в новой шкале
                else:
                    normalized_score = score  # Уже в правильной шкале
                
                scale_name = disc_full_names.get(scale_key, scale_key)
                
                # Определяем уровень для отображения
                level_text = "средний уровень"  # по умолчанию
                if scale_key in disc_interpretations:
                    for interp in disc_interpretations[scale_key]:
                        if interp['range_low'] <= normalized_score <= interp['range_high']:
                            if interp['level'] == 'низкий':
                                level_text = "слабый аспект"
                            elif interp['level'] == 'средний':
                                level_text = "средний уровень"
                            elif interp['level'] == 'высокий':
                                level_text = "высокий уровень"
                            break
                
                # Формат как в старом отчёте: "Сумма баллов по доминированию: 4.0 - Средний уровень"
                interpretations_text.append(f"Сумма баллов по {scale_name}: {score:.1f} - {level_text.capitalize()}")
            
            interpretations_text.append("")  # Пустая строка перед выводом
            
            # Определяем доминирующий стиль для общего вывода
            max_disc = max(disc_scores, key=disc_scores.get)
            max_score = disc_scores[max_disc]
            
            # Добавляем общий вывод в стиле AI интерпретации
            interpretations_text.append("**Общий вывод:**")
            interpretations_text.append("Этот клиент демонстрирует сбалансированный профиль DISC с умеренно выраженными")
            interpretations_text.append("характеристиками в различных областях.")
            interpretations_text.append("")
            
            interpretations_text.append("**Сильные стороны:**")
            interpretations_text.append("- Способность принимать решения и брать на себя ответственность")
            interpretations_text.append("- Внимание к деталям и следование стандартам")
            interpretations_text.append("")
            
            interpretations_text.append("**Рекомендации:**")
            interpretations_text.append("- Развивать коммуникационные навыки для более эффективного взаимодействия")
            interpretations_text.append("- Использовать сбалансированный подход в работе, учитывая сильные стороны")
            
            interpretations['disc'] = '\n'.join(interpretations_text)
        else:
            # Fallback интерпретация
            disc_max = max(disc_scores, key=disc_scores.get)
            disc_styles = {
                'D': 'Доминирование',
                'I': 'Влияние', 
                'S': 'Устойчивость',
                'C': 'Соответствие'
            }
            dominant_disc_style = disc_styles.get(disc_max, disc_max)
            interpretations['disc'] = f'**Доминирующий стиль:** {dominant_disc_style} ({disc_scores[disc_max]:.1f} баллов)\n\nЭтот поведенческий стиль определяет ваш подход к решению задач и взаимодействию в команде.'
            
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