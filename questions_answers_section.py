#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для создания раздела с вопросами, ответами и присвоенными баллами
Предназначен для контроля выводов с возможностью легкого удаления из отчета
"""

from typing import Dict, List, Optional, Tuple
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import mm
from pathlib import Path
import sys

# Добавляем путь к модулям проекта
sys.path.append(str(Path(__file__).parent))

# Реальная загрузка вопросов из промпт файлов
def get_all_questions():
    """Загружает реальные вопросы из промпт файлов"""
    
    def parse_paei_questions(prompt_text):
        """Парсинг вопросов PAEI из текста промпта"""
        lines = prompt_text.strip().split('\n')
        questions = []
        current_question = None
        current_options = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Проверяем, начинается ли строка с номера (1. 2. и т.д.)
            if line[0].isdigit() and line[1:3] == '. ':
                # Если есть текущий вопрос, сохраняем его
                if current_question:
                    questions.append({
                        'question': current_question,
                        'answers': current_options
                    })
                
                # Начинаем новый вопрос
                current_question = line[3:]  # Убираем "1. "
                current_options = {}
            
            # Проверяем варианты ответов (P. A. E. I.)
            elif line.startswith(('P. ', 'A. ', 'E. ', 'I. ')):
                option_letter = line[0]
                option_text = line[3:]  # Убираем "P. "
                current_options[option_letter] = option_text
        
        # Добавляем последний вопрос
        if current_question and current_options:
            questions.append({
                'question': current_question,
                'answers': current_options
            })
        
        return questions
    
    def parse_disc_questions(prompt_text):
        """Парсинг вопросов DISC из промпт файла"""
        lines = prompt_text.strip().split('\n')
        questions = []
        
        for line in lines:
            if not line.strip():
                continue
            
            # Ищем строки с вопросами типа "1.1", "2.2" и т.д. (с отступом в два пробела)
            if line.startswith('  ') and '.' in line.strip() and line.strip()[0].isdigit():
                # Убираем отступ
                line_clean = line.strip()
                parts = line_clean.split(' ', 1)
                if len(parts) > 1:
                    question_id = parts[0]
                    question_text = parts[1]
                    
                    # Определяем категорию по номеру
                    if question_id.startswith('1.'):
                        category = 'D'  # Доминирование
                    elif question_id.startswith('2.'):
                        category = 'I'  # Влияние
                    elif question_id.startswith('3.'):
                        category = 'S'  # Устойчивость
                    elif question_id.startswith('4.'):
                        category = 'C'  # Подчинение правилам
                    else:
                        category = 'Unknown'
                    
                    questions.append({
                        'question': question_text,
                        'category': category,
                        'question_id': question_id
                    })
        
        return questions
    
    def parse_soft_skills_questions(prompt_text):
        """Парсинг вопросов Soft Skills из промпт файла"""
        lines = prompt_text.strip().split('\n')
        questions = []
        current_question = None
        current_skill_names = [
            'Коммуникация', 'Лидерство', 'Командная работа', 'Критическое мышление',
            'Управление временем', 'Стрессоустойчивость', 'Эмоциональный интеллект',
            'Адаптивность', 'Решение проблем', 'Креативность'
        ]
        
        for line in lines:
            if not line.strip():
                continue
            
            # Ищем основные вопросы (начинаются с цифры и точки БЕЗ отступа в начале строки)
            if line.startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ', '10.')):
                question_text = line[line.find('. ') + 2:]  # Убираем "1. " или "10. "
                question_num = int(line.split('.')[0]) - 1  # Получаем номер вопроса
                
                skill_name = current_skill_names[question_num] if question_num < len(current_skill_names) else f'Навык {question_num + 1}'
                
                questions.append({
                    'question': question_text,
                    'skill': skill_name
                })
        
        return questions
    
    def parse_hexaco_questions(prompt_text):
        """Парсинг вопросов HEXACO из промпт файла"""
        lines = prompt_text.strip().split('\n')
        questions = []
        dimension_names = ['H', 'E', 'X', 'A', 'C', 'O']  # Порядок факторов HEXACO
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Ищем вопросы (начинаются с цифры и точки)
            if line[0].isdigit() and line[1:3] == '. ':
                question_text = line[3:]  # Убираем "1. "
                question_num = int(line[0]) - 1  # Получаем индекс (0-based)
                
                dimension = dimension_names[question_num] if question_num < len(dimension_names) else 'Unknown'
                
                questions.append({
                    'question': question_text,
                    'dimension': dimension
                })
        
        return questions
    
    def parse_likert_questions(prompt_text, test_type):
        """Общая функция парсинга вопросов с шкалой Ликерта"""
        if test_type == 'disc':
            return parse_disc_questions(prompt_text)
        elif test_type == 'soft_skills':
            return parse_soft_skills_questions(prompt_text)
        elif test_type == 'hexaco':
            return parse_hexaco_questions(prompt_text)
        return []
    
    try:
        # Загружаем PAEI вопросы
        prompts_path = Path(__file__).parent / "data" / "prompts"
        
        paei_questions = []
        if (prompts_path / "adizes_user.txt").exists():
            with open(prompts_path / "adizes_user.txt", 'r', encoding='utf-8') as f:
                prompt_text = f.read()
                paei_questions = parse_paei_questions(prompt_text)
        
        # Загружаем остальные вопросы из промпт-файлов
        disc_questions = []
        if (prompts_path / "disc_user.txt").exists():
            with open(prompts_path / "disc_user.txt", 'r', encoding='utf-8') as f:
                prompt_text = f.read()
                disc_questions = parse_likert_questions(prompt_text, 'disc')
        
        soft_skills_questions = []
        if (prompts_path / "soft_user.txt").exists():
            with open(prompts_path / "soft_user.txt", 'r', encoding='utf-8') as f:
                prompt_text = f.read()
                soft_skills_questions = parse_likert_questions(prompt_text, 'soft_skills')
        
        hexaco_questions = []
        if (prompts_path / "hexaco_user.txt").exists():
            with open(prompts_path / "hexaco_user.txt", 'r', encoding='utf-8') as f:
                prompt_text = f.read()
                hexaco_questions = parse_likert_questions(prompt_text, 'hexaco')
        
        return {
            'paei': paei_questions,
            'disc': disc_questions,
            'soft_skills': soft_skills_questions,
            'hexaco': hexaco_questions
        }
        
    except Exception as e:
        print(f"Ошибка загрузки вопросов: {e}")
        return {
            'paei': [],
            'disc': [],
            'soft_skills': [],
            'hexaco': []
        }


class QuestionAnswerSection:
    """Класс для создания раздела с вопросами, ответами и баллами"""
    
    def __init__(self):
        questions = get_all_questions()
        self.paei_questions = questions['paei']
        self.disc_questions = questions['disc']
        self.hexaco_questions = questions['hexaco']
        self.soft_skills_questions = questions['soft_skills']
        
    def _calculate_paei_question_scores(self, user_answers: Dict[str, str], question_index: int) -> Dict[str, int]:
        """
        Вычисляет баллы PAEI для конкретного вопроса
        
        Args:
            user_answers: Словарь с ответами пользователя {question_index: selected_option}
            question_index: Индекс вопроса (0-based)
            
        Returns:
            Dict[str, int]: Баллы по каждой категории PAEI для данного вопроса
        """
        scores = {"P": 0, "A": 0, "E": 0, "I": 0}
        
        # Получаем выбранный пользователем вариант ответа
        selected_option = user_answers.get(str(question_index))
        if selected_option and selected_option in scores:
            scores[selected_option] = 1  # PAEI использует систему +1 балл за выбор
            
        return scores
    
    def _calculate_likert_score(self, answer_value: int, reverse_scored: bool = False) -> int:
        """
        Вычисляет балл для шкалы Ликерта
        
        Args:
            answer_value: Значение ответа (1-5 или 1-10)
            reverse_scored: Нужно ли инвертировать оценку
            
        Returns:
            int: Рассчитанный балл
        """
        if reverse_scored:
            # Для некоторых вопросов может потребоваться инверсия
            if answer_value <= 5:
                return 6 - answer_value  # Инверсия для шкалы 1-5
            else:
                return 11 - answer_value  # Инверсия для шкалы 1-10
        return answer_value
    
    def generate_paei_questions_section(self, 
                                      user_answers: Dict[str, str], 
                                      final_scores: Dict[str, float],
                                      styles) -> List:
        """
        Генерирует раздел с вопросами и ответами PAEI
        
        Args:
            user_answers: Ответы пользователя {question_index: selected_option}
            final_scores: Итоговые баллы PAEI
            styles: Стили ReportLab
            
        Returns:
            List: Элементы для добавления в отчет
        """
        story_elements = []
        
        # Заголовок раздела
        story_elements.append(Paragraph("ДЕТАЛИЗАЦИЯ ОТВЕТОВ - ТЕСТ АДИЗЕСА (PAEI)", styles['SectionTitle']))
        story_elements.append(Spacer(1, 3*mm))
        
        # Описание метода подсчета
        description = """
        <b>Методика подсчета баллов PAEI:</b> За каждый выбранный ответ присваивается 1 балл соответствующей категории.
        Итоговый результат показывает распределение предпочтений по управленческим ролям.
        """
        story_elements.append(Paragraph(description, styles['Body']))
        story_elements.append(Spacer(1, 4*mm))
        
        # Итоговые баллы
        total_text = f"<b>Итоговые баллы:</b> P={final_scores.get('P', 0)}, A={final_scores.get('A', 0)}, E={final_scores.get('E', 0)}, I={final_scores.get('I', 0)}"
        story_elements.append(Paragraph(total_text, styles['SubTitle']))
        story_elements.append(Spacer(1, 4*mm))
        
        # Детализация по вопросам
        for i, question_data in enumerate(self.paei_questions):
            question_num = i + 1
            selected_option = user_answers.get(str(i), "Не отвечен")
            
            # Вопрос
            question_text = f"<b>Вопрос {question_num}:</b> {question_data['question']}"
            story_elements.append(Paragraph(question_text, styles['Body']))
            
            # Варианты ответов с выделением выбранного
            for option_key, option_text in question_data['answers'].items():
                if option_key == selected_option:
                    answer_text = f"<b>✓ {option_key}. {option_text}</b> <i>(+1 балл к {option_key})</i>"
                    story_elements.append(Paragraph(answer_text, styles['Body']))
                else:
                    answer_text = f"• {option_key}. {option_text}"
                    story_elements.append(Paragraph(answer_text, styles['ListWithIndent']))
            
            story_elements.append(Spacer(1, 3*mm))
        
        return story_elements
    
    def generate_soft_skills_questions_section(self,
                                             user_answers: Dict[str, int],
                                             final_scores: Dict[str, float],
                                             styles) -> List:
        """
        Генерирует раздел с вопросами и ответами Soft Skills
        
        Args:
            user_answers: Ответы пользователя {question_index: rating_1_to_5}
            final_scores: Итоговые баллы по навыкам
            styles: Стили ReportLab
            
        Returns:
            List: Элементы для добавления в отчет
        """
        story_elements = []
        
        # Заголовок раздела
        story_elements.append(Paragraph("ДЕТАЛИЗАЦИЯ ОТВЕТОВ - SOFT SKILLS", styles['SectionTitle']))
        story_elements.append(Spacer(1, 3*mm))
        
        # Описание метода подсчета
        description = """
        <b>Методика подсчета баллов Soft Skills:</b> Каждый вопрос оценивается по 5-балльной шкале (1 - совершенно не согласен, 5 - полностью согласен).
        Итоговый балл по навыку равен оценке соответствующего вопроса.
        """
        story_elements.append(Paragraph(description, styles['Body']))
        story_elements.append(Spacer(1, 4*mm))
        
        # Итоговые баллы
        skills_summary = ", ".join([f"{skill}={score}" for skill, score in final_scores.items()])
        total_text = f"<b>Итоговые баллы по навыкам:</b> {skills_summary}"
        story_elements.append(Paragraph(total_text, styles['SubTitle']))
        story_elements.append(Spacer(1, 4*mm))
        
        # Детализация по вопросам
        for i, question_data in enumerate(self.soft_skills_questions):
            question_num = i + 1
            user_rating = user_answers.get(str(i), 0)
            skill_name = question_data.get('skill', f'Навык {question_num}')
            
            # Вопрос с результатом
            question_text = f"<b>Вопрос {question_num} ({skill_name}):</b> {question_data['question']}"
            story_elements.append(Paragraph(question_text, styles['Body']))
            
            # Ответ пользователя
            if user_rating > 0:
                # Интерпретация балла для 5-балльной шкалы
                if user_rating >= 4:
                    interpretation = "(Выше среднего уровня)"
                elif user_rating >= 3:
                    interpretation = "(Средний уровень развития навыка)"
                elif user_rating >= 2:
                    interpretation = "(Ниже среднего уровня)"
                else:
                    interpretation = "(Требует значительного развития)"
                
                answer_text = f"<b>Ответ:</b> {user_rating}/5 баллов {interpretation}"
                story_elements.append(Paragraph(answer_text, styles['Body']))
            else:
                story_elements.append(Paragraph("<i>Вопрос не был отвечен</i>", styles['Body']))
            
            story_elements.append(Spacer(1, 3*mm))
        
        return story_elements
    
    def generate_hexaco_questions_section(self,
                                        user_answers: Dict[str, int],
                                        final_scores: Dict[str, float],
                                        styles) -> List:
        """
        Генерирует раздел с вопросами и ответами HEXACO
        
        Args:
            user_answers: Ответы пользователя {question_index: rating_1_to_5}
            final_scores: Итоговые баллы по факторам
            styles: Стили ReportLab
            
        Returns:
            List: Элементы для добавления в отчет
        """
        story_elements = []
        
        # Заголовок раздела
        story_elements.append(Paragraph("ДЕТАЛИЗАЦИЯ ОТВЕТОВ - HEXACO", styles['SectionTitle']))
        story_elements.append(Spacer(1, 3*mm))
        
        # Описание метода подсчета
        description = """
        <b>Методика подсчета баллов HEXACO:</b> Каждый вопрос оценивается по 5-балльной шкале (1 - совершенно не согласен, 5 - полностью согласен).
        Баллы по факторам рассчитываются как средние значения соответствующих вопросов.
        """
        story_elements.append(Paragraph(description, styles['Body']))
        story_elements.append(Spacer(1, 4*mm))
        
        # Итоговые баллы
        factors_summary = ", ".join([f"{factor}={score:.1f}" for factor, score in final_scores.items()])
        total_text = f"<b>Итоговые баллы по факторам:</b> {factors_summary}"
        story_elements.append(Paragraph(total_text, styles['SubTitle']))
        story_elements.append(Spacer(1, 4*mm))
        
        # Детализация по вопросам
        for i, question_data in enumerate(self.hexaco_questions):
            question_num = i + 1
            user_rating = user_answers.get(str(i), 0)
            dimension = question_data.get('dimension', 'Unknown')
            
            # Расшифровка факторов HEXACO
            dimension_names = {
                'H': 'Честность-Скромность (Honesty-Humility)',
                'E': 'Эмоциональность (Emotionality)',
                'X': 'Экстраверсия (eXtraversion)',
                'A': 'Доброжелательность (Agreeableness)',
                'C': 'Добросовестность (Conscientiousness)',
                'O': 'Открытость опыту (Openness to experience)'
            }
            
            dimension_full = dimension_names.get(dimension, dimension)
            
            # Вопрос с результатом
            question_text = f"<b>Вопрос {question_num} ({dimension_full}):</b> {question_data['question']}"
            story_elements.append(Paragraph(question_text, styles['Body']))
            
            # Ответ пользователя
            if user_rating > 0:
                # Интерпретация балла
                if user_rating >= 4:
                    interpretation = "(Высокая выраженность фактора)"
                elif user_rating >= 3:
                    interpretation = "(Средняя выраженность фактора)"
                else:
                    interpretation = "(Низкая выраженность фактора)"
                
                answer_text = f"<b>Ответ:</b> {user_rating}/5 баллов {interpretation}"
                story_elements.append(Paragraph(answer_text, styles['Body']))
            else:
                story_elements.append(Paragraph("<i>Вопрос не был отвечен</i>", styles['Body']))
            
            story_elements.append(Spacer(1, 3*mm))
        
        return story_elements
    
    def generate_disc_questions_section(self,
                                      user_answers: Dict[str, int],
                                      final_scores: Dict[str, float],
                                      styles) -> List:
        """
        Генерирует раздел с вопросами и ответами DISC
        
        Args:
            user_answers: Ответы пользователя {question_index: rating_1_to_5}
            final_scores: Итоговые баллы по типам
            styles: Стили ReportLab
            
        Returns:
            List: Элементы для добавления в отчет
        """
        story_elements = []
        
        # Заголовок раздела
        story_elements.append(Paragraph("ДЕТАЛИЗАЦИЯ ОТВЕТОВ - DISC", styles['SectionTitle']))
        story_elements.append(Spacer(1, 3*mm))
        
        # Описание метода подсчета
        description = """
        <b>Методика подсчета баллов DISC:</b> Каждый вопрос оценивается по 5-балльной шкале. 
        Баллы по типам поведения рассчитываются как средние значения соответствующих вопросов.
        """
        story_elements.append(Paragraph(description, styles['Body']))
        story_elements.append(Spacer(1, 4*mm))
        
        # Итоговые баллы
        types_summary = ", ".join([f"{disc_type}={score:.1f}" for disc_type, score in final_scores.items()])
        total_text = f"<b>Итоговые баллы по типам:</b> {types_summary}"
        story_elements.append(Paragraph(total_text, styles['SubTitle']))
        story_elements.append(Spacer(1, 4*mm))
        
        # Детализация по вопросам
        for i, question_data in enumerate(self.disc_questions):
            question_num = i + 1
            user_rating = user_answers.get(str(i), 0)
            
            # Вопрос
            question_text = f"<b>Вопрос {question_num}:</b> {question_data['question']}"
            story_elements.append(Paragraph(question_text, styles['Body']))
            
            # Ответ пользователя
            if user_rating > 0:
                answer_text = f"<b>Ответ:</b> {user_rating}/5 баллов"
                story_elements.append(Paragraph(answer_text, styles['Body']))
            else:
                story_elements.append(Paragraph("<i>Вопрос не был отвечен</i>", styles['Body']))
            
            story_elements.append(Spacer(1, 3*mm))
        
        return story_elements
    
    def generate_complete_questions_section(self,
                                          paei_answers: Optional[Dict[str, str]] = None,
                                          soft_skills_answers: Optional[Dict[str, int]] = None,
                                          hexaco_answers: Optional[Dict[str, int]] = None,
                                          disc_answers: Optional[Dict[str, int]] = None,
                                          paei_scores: Optional[Dict[str, float]] = None,
                                          soft_skills_scores: Optional[Dict[str, float]] = None,
                                          hexaco_scores: Optional[Dict[str, float]] = None,
                                          disc_scores: Optional[Dict[str, float]] = None,
                                          styles=None) -> List:
        """
        Генерирует полный раздел с вопросами и ответами для всех тестов
        
        Args:
            *_answers: Словари с ответами пользователя для каждого теста
            *_scores: Словари с итоговыми баллами для каждого теста
            styles: Стили ReportLab
            
        Returns:
            List: Все элементы раздела для добавления в отчет
        """
        all_elements = []
        
        # Общий заголовок раздела
        all_elements.append(Paragraph("ПРИЛОЖЕНИЕ: ДЕТАЛИЗАЦИЯ ВОПРОСОВ И ОТВЕТОВ", styles['MainTitle']))
        all_elements.append(Spacer(1, 8*mm))
        
        # Добавляем разделы для каждого теста (если есть данные)
        if paei_answers and paei_scores:
            all_elements.extend(self.generate_paei_questions_section(paei_answers, paei_scores, styles))
            all_elements.append(Spacer(1, 8*mm))
            
        if soft_skills_answers and soft_skills_scores:
            all_elements.extend(self.generate_soft_skills_questions_section(soft_skills_answers, soft_skills_scores, styles))
            all_elements.append(Spacer(1, 8*mm))
            
        if hexaco_answers and hexaco_scores:
            all_elements.extend(self.generate_hexaco_questions_section(hexaco_answers, hexaco_scores, styles))
            all_elements.append(Spacer(1, 8*mm))
            
        if disc_answers and disc_scores:
            all_elements.extend(self.generate_disc_questions_section(disc_answers, disc_scores, styles))
            all_elements.append(Spacer(1, 8*mm))
        
        return all_elements


def create_sample_data_for_testing():
    """
    Создает образцы данных для тестирования модуля
    """
    # Примеры ответов пользователя
    sample_paei_answers = {"0": "P", "1": "A", "2": "E", "3": "I", "4": "P"}
    sample_soft_skills_answers = {str(i): i+5 for i in range(10)}  # Ответы от 5 до 14 (но не больше 10)
    sample_hexaco_answers = {str(i): (i % 5) + 1 for i in range(6)}  # Ответы от 1 до 5
    sample_disc_answers = {str(i): (i % 5) + 1 for i in range(8)}  # Ответы от 1 до 5
    
    # Примеры итоговых баллов
    sample_paei_scores = {"P": 2, "A": 1, "E": 1, "I": 1}
    sample_soft_skills_scores = {
        "Коммуникация": 7, "Работа в команде": 8, "Лидерство": 6, 
        "Критическое мышление": 9, "Управление временем": 5,
        "Стрессоустойчивость": 8, "Эмоциональный интеллект": 7,
        "Адаптивность": 6, "Решение проблем": 9, "Креативность": 8
    }
    sample_hexaco_scores = {"H": 4.2, "E": 3.1, "X": 3.8, "A": 4.0, "C": 3.5, "O": 4.1}
    sample_disc_scores = {"D": 3.2, "I": 4.1, "S": 3.8, "C": 2.9}
    
    return {
        'paei_answers': sample_paei_answers,
        'soft_skills_answers': sample_soft_skills_answers, 
        'hexaco_answers': sample_hexaco_answers,
        'disc_answers': sample_disc_answers,
        'paei_scores': sample_paei_scores,
        'soft_skills_scores': sample_soft_skills_scores,
        'hexaco_scores': sample_hexaco_scores,
        'disc_scores': sample_disc_scores
    }


# Пример использования
if __name__ == "__main__":
    # Демонстрационный запуск
    qa_section = QuestionAnswerSection()
    sample_data = create_sample_data_for_testing()
    
    print("Модуль questions_answers_section.py создан успешно!")
    print(f"Загружено вопросов:")
    print(f"  - PAEI: {len(qa_section.paei_questions)}")
    print(f"  - Soft Skills: {len(qa_section.soft_skills_questions)}")
    print(f"  - HEXACO: {len(qa_section.hexaco_questions)}")
    print(f"  - DISC: {len(qa_section.disc_questions)}")
    print(f"\n[READY] Готов к интеграции с enhanced_pdf_report_v2.py")