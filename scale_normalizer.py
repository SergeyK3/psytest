#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль нормализации шкал для психологических тестов
"""
from typing import Dict, Tuple

class ScaleNormalizer:
    """Нормализатор шкал с правильными максимальными значениями для каждого теста"""
    
    # Максимальные баллы для каждого типа теста (без нормализации)
    MAX_SCORES = {
        "PAEI": 5,        # 5 вопросов с альтернативным выбором
        "DISC": 8,        # максимальная шкала 8
        "HEXACO": 5,      # максимальная оценка 5
        "SOFT_SKILLS": 5  # максимальная оценка 5 (по 5-балльной шкале)
    }
    
    @staticmethod
    def get_max_scale(test_type: str) -> int:
        """Возвращает максимальное значение шкалы для типа теста"""
        return ScaleNormalizer.MAX_SCORES.get(test_type.upper(), 10)
    
    @staticmethod 
    def normalize_paei(scores: Dict[str, float]) -> Tuple[Dict[str, float], str]:
        """Возвращает PAEI баллы без нормализации (оригинальная методика Адизеса)"""
        # Возвращаем оригинальные значения - по методике Адизеса это правильно
        # 1 балл за каждый выбранный ответ, сумма = количество вопросов
        original_scores = {k: int(v) for k, v in scores.items()}  # Целые числа
        method = "PAEI: оригинальная методика Адизеса (1 балл за ответ, сумма = кол-во вопросов)"
        return original_scores, method
    
    @staticmethod
    def normalize_disc(scores: Dict[str, float]) -> Tuple[Dict[str, float], str]:
        """Возвращает DISC баллы без нормализации (шкала 1-5, среднее значение)"""
        # Возвращаем оригинальные значения, округленные до 1 знака
        original_scores = {k: round(v, 1) for k, v in scores.items()}
        method = "DISC: оригинальная шкала 1-5 (среднее значение, без нормализации)"
        return original_scores, method
    
    @staticmethod
    def normalize_hexaco(scores: Dict[str, float]) -> Tuple[Dict[str, float], str]:
        """Возвращает HEXACO баллы без нормализации (оригинальная шкала 1-5)"""
        # Возвращаем оригинальные значения без нормализации
        original_scores = {k: round(v, 1) for k, v in scores.items()}
        method = "HEXACO: оригинальная шкала 1-5 (без нормализации)"
        return original_scores, method
    
    @staticmethod
    def normalize_soft_skills(scores: Dict[str, float]) -> Tuple[Dict[str, float], str]:
        """Возвращает Soft Skills баллы без нормализации (оригинальная шкала 1-5)"""
        # Возвращаем оригинальные значения без нормализации
        original_scores = {k: round(v, 1) for k, v in scores.items()}
        method = "Soft Skills: оригинальная шкала 1-5 (без нормализации)"
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
    
    # Тестовые данные для проверки
    paei_test = {"P": 1, "A": 5, "E": 0, "I": 0}
    disc_test = {"D": 6, "I": 0, "S": 1, "C": 0}
    hexaco_test = {"H": 3.5, "E": 4.2, "X": 2.8, "A": 4.0, "C": 3.1, "O": 3.7}
    soft_skills_test = {"Лидерство": 8.5, "Коммуникация": 7.2, "Аналитика": 9.1}
    
    paei_norm, paei_method = ScaleNormalizer.auto_normalize("PAEI", paei_test)
    disc_norm, disc_method = ScaleNormalizer.auto_normalize("DISC", disc_test)
    hexaco_norm, hexaco_method = ScaleNormalizer.auto_normalize("HEXACO", hexaco_test)
    soft_norm, soft_method = ScaleNormalizer.auto_normalize("SOFT_SKILLS", soft_skills_test)
    
    print(f"PAEI {paei_test} → {paei_norm}")
    print(f"  Метод: {paei_method}")
    print(f"  Макс шкала: {ScaleNormalizer.get_max_scale('PAEI')}")
    
    print(f"DISC {disc_test} → {disc_norm}")
    print(f"  Метод: {disc_method}")
    print(f"  Макс шкала: {ScaleNormalizer.get_max_scale('DISC')}")
    
    print(f"HEXACO → {hexaco_norm}")
    print(f"  Метод: {hexaco_method}")
    print(f"  Макс шкала: {ScaleNormalizer.get_max_scale('HEXACO')}")
    
    print(f"SOFT_SKILLS → {soft_norm}")
    print(f"  Метод: {soft_method}")
    print(f"  Макс шкала: {ScaleNormalizer.get_max_scale('SOFT_SKILLS')}")
    
    return True

if __name__ == "__main__":
    test_scale_normalizer()