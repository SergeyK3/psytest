#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для форматирования интерпретаций психологических тестов
"""

import re
from typing import Dict, List, Tuple, Any


def format_ai_interpretations(interpretations: Dict[str, str]) -> Dict[str, str]:
    """
    Форматирует AI интерпретации для разных типов тестов
    
    Args:
        interpretations: Словарь с интерпретациями {test_type: interpretation_text}
    
    Returns:
        Отформатированные интерпретации
    """
    formatted = {}
    
    for test_type, interpretation in interpretations.items():
        if test_type == 'hexaco':
            formatted[test_type] = format_hexaco_interpretation(interpretation)
        elif test_type == 'disc':
            # Для DISC оставляем оригинальный формат без дополнительного форматирования
            formatted[test_type] = interpretation
        elif test_type == 'paei':
            # Для PAEI (Адизес) сохраняем маркдаун разметку как есть
            formatted[test_type] = interpretation
        else:
            # Для других типов тестов - базовое форматирование
            formatted[test_type] = _basic_format(interpretation)
    
    return formatted


def format_hexaco_interpretation(interpretation: str) -> str:
    """
    Форматирует интерпретацию HEXACO теста
    
    Args:
        interpretation: Текст интерпретации
    
    Returns:
        Отформатированный текст
    """
    if not interpretation:
        return ""
    
    # Разбиваем на секции для каждого фактора
    sections = parse_hexaco_sections(interpretation)
    
    formatted_parts = []
    
    for factor, content in sections.items():
        if content.strip():
            formatted_parts.append(f"**{factor}**")
            formatted_parts.append(content.strip())
            formatted_parts.append("")  # Пустая строка между секциями
    
    return "\n".join(formatted_parts).strip()


def format_disc_interpretation(interpretation: str) -> str:
    """
    Форматирует интерпретацию DISC теста
    
    Args:
        interpretation: Текст интерпретации
    
    Returns:
        Отформатированный текст
    """
    if not interpretation:
        return ""
    
    # Разбиваем на секции для каждого стиля
    sections = parse_disc_sections(interpretation)
    
    formatted_parts = []
    
    for style, content in sections.items():
        if content.strip():
            formatted_parts.append(f"**{style}**")
            formatted_parts.append(content.strip())
            formatted_parts.append("")  # Пустая строка между секциями
    
    return "\n".join(formatted_parts).strip()


def parse_hexaco_sections(interpretation: str) -> Dict[str, str]:
    """
    Разбирает интерпретацию HEXACO на секции по факторам
    
    Args:
        interpretation: Текст интерпретации
    
    Returns:
        Словарь {фактор: описание}
    """
    sections = {}
    
    # Список факторов HEXACO
    factors = [
        'Честность-Скромность',
        'Эмоциональность', 
        'Экстраверсия',
        'Добросовестность',
        'Доброжелательность',
        'Открытость к опыту'
    ]
    
    current_factor = None
    current_content = []
    
    lines = interpretation.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Проверяем, начинается ли строка с названия фактора
        factor_found = None
        for factor in factors:
            if line.startswith(factor):
                factor_found = factor
                break
        
        if factor_found:
            # Сохраняем предыдущую секцию
            if current_factor and current_content:
                sections[current_factor] = '\n'.join(current_content).strip()
            
            # Начинаем новую секцию
            current_factor = factor_found
            current_content = [line]
        elif current_factor:
            # Добавляем к текущей секции
            current_content.append(line)
    
    # Сохраняем последнюю секцию
    if current_factor and current_content:
        sections[current_factor] = '\n'.join(current_content).strip()
    
    return sections


def parse_disc_sections(interpretation: str) -> Dict[str, str]:
    """
    Разбирает интерпретацию DISC на секции по стилям
    
    Args:
        interpretation: Текст интерпретации
    
    Returns:
        Словарь {стиль: описание}
    """
    sections = {}
    
    # Список стилей DISC (как они генерируются в interpretation_utils.py)
    styles = ['Доминирование', 'Влияние', 'Устойчивость', 'Соответствие правилам']
    
    current_style = None
    current_content = []
    
    lines = interpretation.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Проверяем, начинается ли строка с названия стиля (с учетом **markdown**)
        style_found = None
        for style in styles:
            # Проверяем разные варианты: "**Стиль:**", "Стиль:", "**Стиль**"
            if (line.startswith(f"**{style}:**") or 
                line.startswith(f"{style}:") or 
                line.startswith(f"**{style}**") or
                line.startswith(style)):
                style_found = style
                break
        
        if style_found:
            # Сохраняем предыдущую секцию
            if current_style and current_content:
                sections[current_style] = '\n'.join(current_content).strip()
            
            # Начинаем новую секцию
            current_style = style_found
            current_content = [line]
        elif current_style:
            # Добавляем к текущей секции
            current_content.append(line)
    
    # Сохраняем последнюю секцию
    if current_style and current_content:
        sections[current_style] = '\n'.join(current_content).strip()
    
    return sections


def _basic_format(text: str) -> str:
    """
    Базовое форматирование текста
    
    Args:
        text: Исходный текст
    
    Returns:
        Отформатированный текст
    """
    if not text:
        return ""
    
    # Убираем лишние пробелы и переносы
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Разбиваем на абзацы при точках с большой буквы
    text = re.sub(r'\.\s+([А-ЯA-Z])', r'.\n\n\1', text)
    
    return text.strip()


if __name__ == "__main__":
    # Простой тест функций
    test_interpretations = {
        'hexaco': 'Честность-Скромность: 5 баллов. Высокий уровень.',
        'disc': 'Доминирование: 4 балла. Высокий уровень лидерства.',
        'other': 'Простой текст для форматирования.'
    }
    
    formatted = format_ai_interpretations(test_interpretations)
    
    print("Тест форматирования:")
    for test_type, result in formatted.items():
        print(f"\n{test_type}:")
        print(result)