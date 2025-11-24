"""
Модуль для интерпретации результатов психологических тестов с помощью OpenAI GPT-5.1
"""
import os
from typing import Dict, Optional
from pathlib import Path
import openai
from openai import OpenAI

from .prompts import load_prompt


class AIInterpreter:
    """Класс для генерации интерпретаций с помощью OpenAI GPT-5.1"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-5.1"):
        """
        Инициализация AI интерпретатора
        
        Args:
            api_key: OpenAI API ключ (если None, берется из переменной окружения)
            model: Модель для использования (по умолчанию gpt-5.1)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API ключ не найден. Установите переменную окружения OPENAI_API_KEY "
                "или передайте ключ в конструктор."
            )
        
        self.client = OpenAI(api_key=self.api_key)
    
    def _make_request(self, system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
        """
        Выполняет запрос к OpenAI API
        
        Args:
            system_prompt: Системный промпт
            user_prompt: Пользовательский промпт
            temperature: Температура для генерации (0-1)
            
        Returns:
            Ответ от GPT
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            # В случае ошибки возвращаем базовую интерпретацию
            return f"Интерпретация недоступна (ошибка AI): {str(e)}"
    
    def interpret_paei(self, scores: Dict[str, float], dialog_context: str = "") -> str:
        """
        Интерпретация результатов теста PAEI (Адизес)
        
        Args:
            scores: Словарь баллов по шкалам {'P': score, 'A': score, ...}
            dialog_context: Контекст диалога (если есть)
            
        Returns:
            Текст интерпретации
        """
        system_prompt = load_prompt("adizes_system_res.txt")
        
        scores_text = ", ".join([f"{k}: {v}" for k, v in scores.items()])
        user_prompt = f"Проанализируй результаты теста PAEI: {scores_text}"
        
        if dialog_context:
            user_prompt += f"\n\nКонтекст диалога: {dialog_context}"
        
        return self._make_request(system_prompt, user_prompt)
    
    def interpret_adizes(self, choices: list, dialog_context: str = "") -> str:
        """
        Интерпретация результатов теста Адизеса на основе выборов
        
        Args:
            choices: Список выборов пользователя ['P', 'A', 'E', 'I']
            dialog_context: Контекст диалога (если есть)
            
        Returns:
            Текст интерпретации
        """
        system_prompt = load_prompt("adizes_system_res.txt")
        
        choices_text = ", ".join(choices)
        user_prompt = f"Проанализируй выборы в тесте Адизеса: {choices_text}"
        
        if dialog_context:
            user_prompt += f"\n\nКонтекст диалога: {dialog_context}"
        
        return self._make_request(system_prompt, user_prompt)
    
    def interpret_disc(self, scores: Dict[str, float], dialog_context: str = "") -> str:
        """
        Интерпретация результатов теста DISC
        
        Args:
            scores: Словарь баллов по шкалам {'D': score, 'I': score, ...}
            dialog_context: Контекст диалога (если есть)
            
        Returns:
            Текст интерпретации
        """
        system_prompt = load_prompt("disk_system_res.txt")
        
        scores_text = ", ".join([f"{k}: {v}" for k, v in scores.items()])
        user_prompt = f"Проанализируй результаты теста DISC: {scores_text}"
        
        if dialog_context:
            user_prompt += f"\n\nКонтекст диалога: {dialog_context}"
        
        return self._make_request(system_prompt, user_prompt)
    
    def interpret_hexaco(self, scores: Dict[str, float], dialog_context: str = "") -> str:
        """
        Интерпретация результатов теста HEXACO
        
        Args:
            scores: Словарь баллов по шкалам {'H': score, 'E': score, ...}
            dialog_context: Контекст диалога (если есть)
            
        Returns:
            Текст интерпретации
        """
        system_prompt = load_prompt("hexaco_system_res.txt")
        
        scores_text = ", ".join([f"{k}: {v}" for k, v in scores.items()])
        user_prompt = f"Проанализируй результаты теста HEXACO: {scores_text}"
        
        if dialog_context:
            user_prompt += f"\n\nКонтекст диалога: {dialog_context}"
        
        return self._make_request(system_prompt, user_prompt)
    
    def interpret_soft_skills(self, scores: Dict[str, float], dialog_context: str = "") -> str:
        """
        Интерпретация результатов по soft skills
        
        Args:
            scores: Словарь баллов по навыкам
            dialog_context: Контекст диалога (если есть)
            
        Returns:
            Текст интерпретации
        """
        system_prompt = load_prompt("soft_system_res.txt")
        
        scores_text = ", ".join([f"{k}: {v}" for k, v in scores.items()])
        user_prompt = f"Проанализируй результаты по soft skills: {scores_text}"
        
        if dialog_context:
            user_prompt += f"\n\nКонтекст диалога: {dialog_context}"
        
        return self._make_request(system_prompt, user_prompt)

    def interpret_general_conclusion(self, all_scores: Dict, dialog_context: str = "") -> str:
        """
        Создание общего заключения на основе всех тестов
        
        Args:
            all_scores: Словарь со всеми результатами тестов
                {
                    'paei': {'Производитель': 8, 'Администратор': 5, ...},
                    'disc': {'D': 7, 'I': 5, 'S': 3, 'C': 4},
                    'hexaco': {'Честность-Скромность': 4, ...},
                    'soft_skills': {'Лидерство': 8, ...}
                }
            dialog_context: Контекст диалога (если есть)
            
        Returns:
            Текст общего заключения
        """
        system_prompt = load_prompt("general_system_res.txt")
        
        # Формируем текст с результатами всех тестов
        results_text = "Результаты всех тестов:\n\n"
        
        if 'paei' in all_scores:
            paei_text = ", ".join([f"{k}: {v}" for k, v in all_scores['paei'].items()])
            results_text += f"PAEI: {paei_text}\n\n"
        
        if 'soft_skills' in all_scores:
            soft_text = ", ".join([f"{k}: {v}" for k, v in all_scores['soft_skills'].items()])
            results_text += f"Soft Skills: {soft_text}\n\n"
        
        if 'hexaco' in all_scores:
            hexaco_text = ", ".join([f"{k}: {v}" for k, v in all_scores['hexaco'].items()])
            results_text += f"HEXACO: {hexaco_text}\n\n"
        
        if 'disc' in all_scores:
            disc_text = ", ".join([f"{k}: {v}" for k, v in all_scores['disc'].items()])
            results_text += f"DISC: {disc_text}\n\n"
        
        user_prompt = f"Создай общий психологический портрет на основе:\n\n{results_text}"
        
        if dialog_context:
            user_prompt += f"\nКонтекст диалога: {dialog_context}"
        
        return self._make_request(system_prompt, user_prompt)


def get_ai_interpreter(api_key: Optional[str] = None) -> Optional[AIInterpreter]:
    """
    Фабричная функция для создания AI интерпретатора
    
    Args:
        api_key: OpenAI API ключ
        
    Returns:
        AIInterpreter или None если ключ недоступен
    """
    try:
        return AIInterpreter(api_key)
    except ValueError:
        # Если ключ недоступен, возвращаем None
        # Система будет использовать статические интерпретации
        return None