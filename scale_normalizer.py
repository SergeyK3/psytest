#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль нормализации шкал для психологических тестов
"""
from typing import Dict, Tuple

class ScaleNormalizer:
    """Нормализатор шкал для приведения к единому масштабу"""
    
    # Максимальные баллы для каждого типа теста
    MAX_SCORES = {
        "PAEI": 5,    # 5 вопросов с альтернативным выбором
        "DISC": 6,    # 6 вопросов с альтернативным выбором  
        "HEXACO": 5,  # Шкала 1-5
        "SOFT_SKILLS": 10  # Шкала 1-10
    }
    
    TARGET_MAX = 10  # Целевая максимальная шкала
    
    @staticmethod
    def normalize_alternative_choice(scores: Dict[str, float], max_questions: int) -> Dict[str, float]:
        """
        Нормализует баллы альтернативного выбора (PAEI, DISC) к шкале 0-10
        
        Args:
            scores: Исходные баллы (количество выборов)
            max_questions: Максимальное количество вопросов
            
        Returns:
            Нормализованные баллы к шкале 0-10 (округленные до 1 знака)
        """
        normalized = {}
        for key, count in scores.items():
            # Нормализуем: (count / max_questions) * 10
            value = (count / max_questions) * ScaleNormalizer.TARGET_MAX
            normalized[key] = round(value, 1)  # Округляем до 1 десятичного знака
        return normalized
    
    @staticmethod
    def normalize_rating_scale(scores: Dict[str, float], original_min: int, original_max: int) -> Dict[str, float]:
        """
        Нормализует баллы рейтинговой шкалы к шкале 0-10
        
        Args:
            scores: Исходные баллы
            original_min: Минимум исходной шкалы
            original_max: Максимум исходной шкалы
            
        Returns:
            Нормализованные баллы к шкале 0-10 (округленные до 1 знака)
        """
        normalized = {}
        original_range = original_max - original_min
        
        for key, value in scores.items():
            # Переводим в 0-10: ((value - min) / range) * 10
            normalized_value = ((value - original_min) / original_range) * ScaleNormalizer.TARGET_MAX
            clamped_value = max(0, min(10, normalized_value))  # Ограничиваем 0-10
            normalized[key] = round(clamped_value, 1)  # Округляем до 1 десятичного знака
            
        return normalized
    
    @staticmethod 
    def normalize_paei(scores: Dict[str, float]) -> Tuple[Dict[str, float], str]:
        """Нормализует PAEI баллы"""
        normalized = ScaleNormalizer.normalize_alternative_choice(
            scores, ScaleNormalizer.MAX_SCORES["PAEI"]
        )
        method = f"PAEI: {ScaleNormalizer.MAX_SCORES['PAEI']} вопросов → 0-10"
        return normalized, method
    
    @staticmethod
    def normalize_disc(scores: Dict[str, float]) -> Tuple[Dict[str, float], str]:
        """Нормализует DISC баллы"""
        normalized = ScaleNormalizer.normalize_alternative_choice(
            scores, ScaleNormalizer.MAX_SCORES["DISC"]
        )
        method = f"DISC: {ScaleNormalizer.MAX_SCORES['DISC']} вопросов → 0-10"
        return normalized, method
    
    @staticmethod
    def normalize_hexaco(scores: Dict[str, float]) -> Tuple[Dict[str, float], str]:
        """Возвращает HEXACO баллы без нормализации (оригинальная шкала 1-5)"""
        # Возвращаем оригинальные значения без нормализации
        original_scores = {k: round(v, 1) for k, v in scores.items()}
        method = "HEXACO: оригинальная шкала 1-5 (без нормализации)"
        return original_scores, method
    
    @staticmethod
    def normalize_soft_skills(scores: Dict[str, float]) -> Tuple[Dict[str, float], str]:
        """Возвращает Soft Skills баллы без нормализации (оригинальная шкала 1-10)"""
        # Возвращаем оригинальные значения без нормализации
        original_scores = {k: round(v, 1) for k, v in scores.items()}
        method = "Soft Skills: оригинальная шкала 1-10 (без нормализации)"
        return original_scores, method
    
    @staticmethod
    def auto_normalize(test_type: str, scores: Dict[str, float]) -> Tuple[Dict[str, float], str]:
        """
        Автоматически выбирает метод нормализации по типу теста
        
        Args:
            test_type: Тип теста (PAEI, DISC, HEXACO, SOFT_SKILLS)
            scores: Исходные баллы
            
        Returns:
            Нормализованные баллы и описание метода
        """
        test_type = test_type.upper()
        
        if test_type == "PAEI":
            return ScaleNormalizer.normalize_paei(scores)
        elif test_type == "DISC":
            return ScaleNormalizer.normalize_disc(scores)
        elif test_type == "HEXACO":
            return ScaleNormalizer.normalize_hexaco(scores)
        elif test_type == "SOFT_SKILLS":
            return ScaleNormalizer.normalize_soft_skills(scores)
        else:
            # Неизвестный тип - возвращаем без изменений
            return scores.copy(), f"Неизвестный тип {test_type}"

def test_scale_normalizer():
    """Быстрый тест нормализатора"""
    print("🧪 Тест ScaleNormalizer")
    
    # Проблемные случаи
    paei_extreme = {"P": 1, "A": 5, "E": 0, "I": 0}
    disc_extreme = {"D": 6, "I": 0, "S": 1, "C": 0}
    
    paei_norm, paei_method = ScaleNormalizer.auto_normalize("PAEI", paei_extreme)
    disc_norm, disc_method = ScaleNormalizer.auto_normalize("DISC", disc_extreme)
    
    print(f"PAEI {paei_extreme} → {paei_norm} ({paei_method})")
    print(f"DISC {disc_extreme} → {disc_norm} ({disc_method})")
    
    return True

if __name__ == "__main__":
    test_scale_normalizer()