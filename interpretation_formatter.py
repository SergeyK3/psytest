"""
Модуль для форматирования AI интерпретаций тестов HEXACO и DISC
"""

import re
from typing import Dict, List


def format_hexaco_interpretation(text: str) -> str:
    """
    Форматирует интерпретацию HEXACO для лучшего отображения в PDF
    Разделяет по качествам, выделяет разделы
    """
    if not text or not isinstance(text, str):
        return text
    
    # Не изменяем сам текст, только подготавливаем для парсинга
    return text


def format_disc_interpretation(text: str) -> str:
    """
    Форматирует интерпретацию DISC для лучшего отображения в PDF
    Разделяет по типам поведения, выделяет разделы
    """
    if not text or not isinstance(text, str):
        return text
    
    # Не изменяем сам текст, только подготавливаем для парсинга
    return text


def format_ai_interpretations(interpretations: Dict[str, str]) -> Dict[str, str]:
    """
    Форматирует все AI интерпретации для улучшенного отображения
    """
    formatted = {}
    
    for test_type, interpretation in interpretations.items():
        if test_type == 'hexaco':
            formatted[test_type] = format_hexaco_interpretation(interpretation)
        elif test_type == 'disc':
            formatted[test_type] = format_disc_interpretation(interpretation)
        else:
            # Для остальных тестов применяем базовое форматирование
            formatted[test_type] = interpretation
    
    return formatted


def parse_hexaco_sections(text: str) -> Dict[str, str]:
    """
    Разбирает интерпретацию HEXACO на отдельные секции
    Возвращает словарь с секциями для отдельного отображения
    """
    sections = {}
    
    if not text or not isinstance(text, str):
        return sections
    
    # Качества HEXACO
    hexaco_qualities = [
        "Честность-Скромность",
        "Эмоциональность", 
        "Экстраверсия",
        "Добросовестность",
        "Доброжелательность",
        "Открытость к опыту"
    ]
    
    # Ищем каждое качество и его описание
    for i, quality in enumerate(hexaco_qualities):
        next_quality = hexaco_qualities[i+1] if i+1 < len(hexaco_qualities) else None
        
        if next_quality:
            # Ищем текст от текущего качества до следующего
            pattern = rf"{re.escape(quality)}:\s*\d+.*?(?={re.escape(next_quality)}|Общий портрет)"
        else:
            # Для последнего качества ищем до "Общий портрет"
            pattern = rf"{re.escape(quality)}:\s*\d+.*?(?=Общий портрет|$)"
            
        matches = list(re.finditer(pattern, text, re.DOTALL | re.IGNORECASE))
        if matches:
            # Берем только первое совпадение, чтобы избежать дубликатов
            first_match = matches[0].group(0).strip()
            
            # Дополнительная очистка: убираем повторные вхождения того же качества внутри секции
            lines = first_match.split('\n')
            cleaned_lines = []
            quality_header_found = False
            
            for line in lines:
                line = line.strip()
                if line.startswith(f"{quality}:") and quality_header_found:
                    # Пропускаем повторный заголовок того же качества
                    continue
                elif line.startswith(f"{quality}:"):
                    quality_header_found = True
                    cleaned_lines.append(line)
                elif line:
                    cleaned_lines.append(line)
            
            sections[quality] = '\n'.join(cleaned_lines)
    
    # Общий портрет личности
    general_match = re.search(r"Общий портрет личности:.*?(?=Рекомендации психолога|$)", text, re.DOTALL | re.IGNORECASE)
    if general_match:
        sections["Общий портрет личности"] = general_match.group(0).strip()
    
    # Рекомендации психолога
    recommendations_match = re.search(r"Рекомендации психолога:.*$", text, re.DOTALL | re.IGNORECASE)
    if recommendations_match:
        sections["Рекомендации психолога"] = recommendations_match.group(0).strip()
    
    return sections


def parse_disc_sections(text: str) -> Dict[str, str]:
    """
    Разбирает интерпретацию DISC на отдельные секции
    """
    sections = {}
    
    if not text or not isinstance(text, str):
        return sections
    
    # DISC типы
    disc_types = [
        "доминированию",
        "влиянию",
        "устойчивости",
        "подчинению правилам"
    ]
    
    # Ищем секции по типам
    for i, disc_type in enumerate(disc_types):
        pattern = rf"Сумма баллов по {disc_type}.*?(?=Сумма баллов по {disc_types[i+1] if i+1 < len(disc_types) else 'Общий вывод'}|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            sections[f"DISC_{disc_type.capitalize()}"] = match.group(0).strip()
    
    # Основные разделы
    main_sections = ["Общий вывод", "Сильные стороны", "Зоны развития", "Рекомендации психолога"]
    
    for i, section in enumerate(main_sections):
        next_section = main_sections[i+1] if i+1 < len(main_sections) else None
        if next_section:
            pattern = rf"{section}:.*?(?={next_section}|$)"
        else:
            pattern = rf"{section}:.*$"
        
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            sections[section] = match.group(0).strip()
    
    return sections