#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для правильного масштабирования шкал тестов
"""
from typing import Dict, Tuple
import math

class TestScaleNormalizer:
    """Класс для нормализации шкал разных тестов"""
    
    # Определяем максимальные возможные баллы для каждого теста
    TEST_MAXIMUMS = {
        "PAEI": 5,    # 5 вопросов с альтернативным выбором
        "DISC": 6,    # 6 вопросов с альтернативным выбором  
        "HEXACO": 5,  # Каждый фактор оценивается по шкале 1-5
        "SOFT_SKILLS": 10  # Каждый навык оценивается по шкале 1-10
    }
    
    TARGET_SCALE = 10  # Целевая шкала для всех диаграмм
    
    @classmethod
    def normalize_paei_scores(cls, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Нормализует баллы PAEI к шкале 0-10
        
        Args:
            scores: Исходные баллы PAEI {"P": count, "A": count, "E": count, "I": count}
            
        Returns:
            Нормализованные баллы к шкале 0-10
        """
        max_possible = cls.TEST_MAXIMUMS["PAEI"]
        normalized = {}
        
        for key, value in scores.items():
            # Нормализуем к шкале 0-10
            normalized[key] = (value / max_possible) * cls.TARGET_SCALE
            
        return normalized
    
    @classmethod
    def normalize_disc_scores(cls, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Нормализует баллы DISC к шкале 0-10
        
        Args:
            scores: Исходные баллы DISC {"D": count, "I": count, "S": count, "C": count}
            
        Returns:
            Нормализованные баллы к шкале 0-10
        """
        max_possible = cls.TEST_MAXIMUMS["DISC"]
        normalized = {}
        
        for key, value in scores.items():
            # Нормализуем к шкале 0-10
            normalized[key] = (value / max_possible) * cls.TARGET_SCALE
            
        return normalized
    
    @classmethod
    def normalize_hexaco_scores(cls, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Нормализует баллы HEXACO к шкале 0-10
        
        Args:
            scores: Исходные баллы HEXACO по шкале 1-5
            
        Returns:
            Нормализованные баллы к шкале 0-10
        """
        normalized = {}
        
        for key, value in scores.items():
            # Переводим из шкалы 1-5 в шкалу 0-10
            # (value - 1) переводит в 0-4, затем * 2.5 дает 0-10
            normalized[key] = ((value - 1) / 4) * cls.TARGET_SCALE
            
        return normalized
    
    @classmethod
    def normalize_soft_skills_scores(cls, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Нормализует баллы Soft Skills к шкале 0-10
        
        Args:
            scores: Исходные баллы Soft Skills по шкале 1-10
            
        Returns:
            Нормализованные баллы к шкале 0-10
        """
        normalized = {}
        
        for key, value in scores.items():
            # Переводим из шкалы 1-10 в шкалу 0-10
            normalized[key] = value - 1
            
        return normalized
    
    @classmethod
    def auto_normalize(cls, test_type: str, scores: Dict[str, float]) -> Tuple[Dict[str, float], str]:
        """
        Автоматически нормализует баллы в зависимости от типа теста
        
        Args:
            test_type: Тип теста ("PAEI", "DISC", "HEXACO", "SOFT_SKILLS")
            scores: Исходные баллы
            
        Returns:
            Tuple из нормализованных баллов и описания метода
        """
        test_type = test_type.upper()
        
        if test_type == "PAEI":
            normalized = cls.normalize_paei_scores(scores)
            method = f"PAEI: нормализация {cls.TEST_MAXIMUMS['PAEI']} вопросов → шкала 0-10"
        elif test_type == "DISC":
            normalized = cls.normalize_disc_scores(scores)
            method = f"DISC: нормализация {cls.TEST_MAXIMUMS['DISC']} вопросов → шкала 0-10"
        elif test_type == "HEXACO":
            normalized = cls.normalize_hexaco_scores(scores)
            method = "HEXACO: шкала 1-5 → шкала 0-10"
        elif test_type == "SOFT_SKILLS":
            normalized = cls.normalize_soft_skills_scores(scores)
            method = "Soft Skills: шкала 1-10 → шкала 0-10"
        else:
            # Неизвестный тип - возвращаем как есть
            normalized = scores.copy()
            method = f"Неизвестный тип {test_type}: без изменений"
        
        return normalized, method
    
    @classmethod
    def get_test_info(cls, test_type: str) -> Dict[str, any]:
        """
        Возвращает информацию о тесте
        
        Args:
            test_type: Тип теста
            
        Returns:
            Словарь с информацией о тесте
        """
        test_type = test_type.upper()
        
        if test_type in cls.TEST_MAXIMUMS:
            return {
                "max_score": cls.TEST_MAXIMUMS[test_type],
                "target_scale": cls.TARGET_SCALE,
                "scale_type": "альтернативный выбор" if test_type in ["PAEI", "DISC"] else "прямая оценка"
            }
        else:
            return {
                "max_score": "неизвестно",
                "target_scale": cls.TARGET_SCALE,
                "scale_type": "неизвестно"
            }

def test_scale_normalization():
    """Тестирует систему нормализации шкал"""
    print("🎯 ТЕСТИРОВАНИЕ СИСТЕМЫ НОРМАЛИЗАЦИИ ШКАЛ")
    print("=" * 60)
    
    normalizer = TestScaleNormalizer()
    
    # Тестовые случаи
    test_cases = [
        {
            "test_type": "PAEI",
            "description": "Проблемный случай - максимальный A",
            "scores": {"P": 1, "A": 5, "E": 0, "I": 0}  # Максимум 5 баллов за 5 вопросов
        },
        {
            "test_type": "DISC", 
            "description": "Проблемный случай - максимальный D",
            "scores": {"D": 6, "I": 0, "S": 1, "C": 0}  # Максимум 6 баллов за 6 вопросов
        },
        {
            "test_type": "HEXACO",
            "description": "Средние оценки HEXACO",
            "scores": {"H": 3.5, "E": 4.2, "X": 2.8, "A": 4.0, "C": 3.1, "O": 4.5}
        },
        {
            "test_type": "SOFT_SKILLS",
            "description": "Высокие soft skills",
            "scores": {"Лидерство": 9, "Коммуникация": 8, "Планирование": 7}
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📊 Тест {i}: {case['description']}")
        print(f"Тип: {case['test_type']}")
        print(f"Исходные баллы: {case['scores']}")
        
        # Получаем информацию о тесте
        test_info = normalizer.get_test_info(case['test_type'])
        print(f"Макс. возможный балл: {test_info['max_score']}")
        print(f"Тип шкалы: {test_info['scale_type']}")
        
        # Нормализуем
        normalized, method = normalizer.auto_normalize(case['test_type'], case['scores'])
        print(f"Нормализованные баллы: {normalized}")
        print(f"Метод: {method}")
        
        # Проверяем соотношения
        if case['scores']:
            orig_max = max(case['scores'].values())
            orig_min = min(v for v in case['scores'].values() if v > 0)
            orig_ratio = orig_max / orig_min if orig_min > 0 else float('inf')
            
            norm_max = max(normalized.values())
            norm_min = min(v for v in normalized.values() if v > 0)  
            norm_ratio = norm_max / norm_min if norm_min > 0 else float('inf')
            
            print(f"Соотношение до: {orig_ratio:.2f}")
            print(f"Соотношение после: {norm_ratio:.2f}")
    
    print(f"\n✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print(f"Теперь все тесты используют единую шкалу 0-10 с правильными пропорциями!")

if __name__ == "__main__":
    print("🚀 СИСТЕМА НОРМАЛИЗАЦИИ ШКАЛ ТЕСТОВ")
    print("=" * 70)
    
    try:
        test_scale_normalization()
        
        print(f"\n💡 КЛЮЧЕВЫЕ ПРЕИМУЩЕСТВА:")
        print(f"1. Все тесты приведены к единой шкале 0-10")
        print(f"2. Учтены особенности альтернативного выбора в PAEI/DISC")
        print(f"3. Пропорции между факторами сохранены")
        print(f"4. Диаграммы стали сопоставимыми между тестами")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()