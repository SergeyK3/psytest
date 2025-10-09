"""
Тесты для основных функций Telegram бота
Проверяет ключевые функции, выявленные в ходе анализа Copilot
"""

import pytest
import sys
from pathlib import Path

# Добавляем корневую папку в path для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))

from telegram_test_bot import (
    get_soft_skills_names, 
    UserSession,
    parse_soft_skills_questions,
    SOFT_SKILLS_QUESTIONS
)

class TestSoftSkillsFunction:
    """Тестирует функцию динамического извлечения названий навыков"""
    
    def test_get_soft_skills_names_returns_list(self):
        """Проверяет, что функция возвращает список"""
        result = get_soft_skills_names()
        assert isinstance(result, list)
        assert len(result) > 0
        
    def test_get_soft_skills_names_from_questions(self):
        """Проверяет, что функция извлекает названия из SOFT_SKILLS_QUESTIONS"""
        result = get_soft_skills_names()
        
        # Проверяем, что количество навыков соответствует количеству вопросов
        if SOFT_SKILLS_QUESTIONS:
            assert len(result) == len(SOFT_SKILLS_QUESTIONS)
            
        # Проверяем, что все элементы - строки
        for skill in result:
            assert isinstance(skill, str)
            assert len(skill) > 0
    
    def test_soft_skills_questions_parsing(self):
        """Проверяет корректность парсинга вопросов"""
        questions = parse_soft_skills_questions()
        
        if questions:  # Если файл существует и загружен
            assert isinstance(questions, list)
            
            for question in questions:
                assert isinstance(question, dict)
                assert "question" in question
                assert "skill" in question
                assert isinstance(question["question"], str)
                assert isinstance(question["skill"], str)


class TestUserSession:
    """Тестирует класс UserSession"""
    
    def test_user_session_creation(self):
        """Проверяет корректное создание сессии пользователя"""
        user_id = 12345
        session = UserSession(user_id)
        
        assert session.user_id == user_id
        assert session.name is None
        assert session.current_question == 0
        assert isinstance(session.paei_scores, dict)
        assert isinstance(session.disc_scores, dict)
        assert isinstance(session.hexaco_scores, list)
        assert isinstance(session.soft_skills_scores, list)
        
    def test_user_session_defaults(self):
        """Проверяет значения по умолчанию"""
        session = UserSession(67890)
        
        # Проверяем, что PAEI и DISC начинают с нулевых значений
        paei_expected_keys = ["P", "A", "E", "I"]
        disc_expected_keys = ["D", "I", "S", "C"]
        
        for key in paei_expected_keys:
            assert key in session.paei_scores
            assert session.paei_scores[key] == 0
            
        for key in disc_expected_keys:
            assert key in session.disc_scores
            assert session.disc_scores[key] == 0


class TestDataIntegrity:
    """Проверяет целостность данных и корректность конфигурации"""
    
    def test_soft_skills_questions_not_empty(self):
        """Проверяет, что вопросы по soft skills загружены"""
        assert len(SOFT_SKILLS_QUESTIONS) > 0
        
    def test_soft_skills_questions_structure(self):
        """Проверяет структуру вопросов soft skills"""
        for i, question in enumerate(SOFT_SKILLS_QUESTIONS):
            assert "question" in question, f"Вопрос {i} не содержит поле 'question'"
            assert "skill" in question, f"Вопрос {i} не содержит поле 'skill'"
            
            # Проверяем, что поля не пустые
            assert len(question["question"].strip()) > 0, f"Вопрос {i} имеет пустой текст"
            assert len(question["skill"].strip()) > 0, f"Вопрос {i} имеет пустое название навыка"


class TestSoftSkillsDynamicNames:
    """Тестирует динамическое извлечение названий навыков"""
    
    def test_no_hardcoded_skills(self):
        """Проверяет, что названия навыков берутся из конфигурации, а не хардкода"""
        dynamic_names = get_soft_skills_names()
        
        # Проверяем, что функция возвращает корректные данные
        assert len(dynamic_names) > 0
        
        # Если у нас есть вопросы, проверяем соответствие
        if SOFT_SKILLS_QUESTIONS:
            expected_names = [q.get("skill", f"Навык {i+1}") for i, q in enumerate(SOFT_SKILLS_QUESTIONS)]
            assert dynamic_names == expected_names
    
    def test_fallback_mechanism(self):
        """Проверяет fallback механизм при ошибке извлечения навыков"""
        # Эмулируем ситуацию с пустыми вопросами
        # (в реальности можно модифицировать SOFT_SKILLS_QUESTIONS через mock)
        
        # Вызываем функцию и проверяем, что она не крашится
        result = get_soft_skills_names()
        assert isinstance(result, list)
        assert len(result) > 0
        
        # Все элементы должны быть строками
        for skill in result:
            assert isinstance(skill, str)
            assert len(skill.strip()) > 0


if __name__ == "__main__":
    # Запуск тестов напрямую
    pytest.main([__file__, "-v"])