#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пример интеграции раздела с вопросами и ответами в Telegram бот
Показывает, как собирать ответы пользователя и передавать их в отчет
"""

from pathlib import Path
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from datetime import datetime


class UserAnswersCollector:
    """
    Класс для сбора ответов пользователя в формате, 
    подходящем для раздела вопросов и ответов
    """
    
    def __init__(self):
        self.user_answers = {
            'paei': {},
            'soft_skills': {},
            'hexaco': {},
            'disc': {}
        }
        
    def add_paei_answer(self, question_index: int, selected_option: str):
        """Добавляет ответ PAEI (P, A, E, I)"""
        self.user_answers['paei'][str(question_index)] = selected_option
        
    def add_soft_skills_answer(self, question_index: int, rating: int):
        """Добавляет ответ Soft Skills (1-10)"""
        self.user_answers['soft_skills'][str(question_index)] = rating
        
    def add_hexaco_answer(self, question_index: int, rating: int):
        """Добавляет ответ HEXACO (1-5)"""
        self.user_answers['hexaco'][str(question_index)] = rating
        
    def add_disc_answer(self, question_index: int, rating: int):
        """Добавляет ответ DISC (1-5)"""
        self.user_answers['disc'][str(question_index)] = rating
        
    def get_answers_dict(self):
        """Возвращает словарь ответов для передачи в отчет"""
        return self.user_answers.copy()
        
    def clear(self):
        """Очищает все ответы"""
        for test_type in self.user_answers:
            self.user_answers[test_type].clear()


def simulate_user_session_with_questions():
    """
    Симулирует сессию пользователя с сбором ответов
    и генерацией отчета с разделом вопросов
    """
    print("🤖 СИМУЛЯЦИЯ СЕССИИ TELEGRAM БОТА С РАЗДЕЛОМ ВОПРОСОВ")
    print("=" * 65)
    
    # Создаем коллектор ответов
    answers_collector = UserAnswersCollector()
    
    # === Симулируем прохождение PAEI теста ===
    print("\n📋 Симулируем PAEI тест...")
    paei_simulation = [
        (0, "P", "Вопрос 1: Пользователь выбрал P (Производитель)"),
        (1, "A", "Вопрос 2: Пользователь выбрал A (Администратор)"),  
        (2, "E", "Вопрос 3: Пользователь выбрал E (Предприниматель)"),
        (3, "I", "Вопрос 4: Пользователь выбрал I (Интегратор)"),
        (4, "P", "Вопрос 5: Пользователь выбрал P (Производитель)")
    ]
    
    for q_idx, answer, description in paei_simulation:
        answers_collector.add_paei_answer(q_idx, answer)
        print(f"  ✅ {description}")
    
    # === Симулируем прохождение Soft Skills теста ===
    print("\n💡 Симулируем Soft Skills тест...")
    soft_skills_simulation = [
        (0, 8, "Коммуникация: 8/10"),
        (1, 7, "Работа в команде: 7/10"), 
        (2, 9, "Лидерство: 9/10"),
        (3, 6, "Критическое мышление: 6/10"),
        (4, 7, "Управление временем: 7/10"),
        (5, 8, "Стрессоустойчивость: 8/10"),
        (6, 8, "Эмоциональный интеллект: 8/10"),
        (7, 6, "Адаптивность: 6/10"),
        (8, 9, "Решение проблем: 9/10"),
        (9, 7, "Креативность: 7/10")
    ]
    
    for q_idx, rating, description in soft_skills_simulation:
        answers_collector.add_soft_skills_answer(q_idx, rating)
        print(f"  ✅ {description}")
    
    # === Симулируем прохождение HEXACO теста ===
    print("\n🧠 Симулируем HEXACO тест...")
    hexaco_simulation = [
        (0, 4, "Честность-Скромность: 4/5"),
        (1, 3, "Эмоциональность: 3/5"),
        (2, 5, "Экстраверсия: 5/5"), 
        (3, 4, "Доброжелательность: 4/5"),
        (4, 3, "Добросовестность: 3/5"),
        (5, 4, "Открытость опыту: 4/5")
    ]
    
    for q_idx, rating, description in hexaco_simulation:
        answers_collector.add_hexaco_answer(q_idx, rating)
        print(f"  ✅ {description}")
    
    # === Симулируем прохождение DISC теста ===
    print("\n🎭 Симулируем DISC тест...")
    disc_simulation = [
        (0, 4, "Доминирование: 4/5"),
        (1, 5, "Влияние: 5/5"),
        (2, 3, "Постоянство: 3/5"),
        (3, 2, "Соответствие: 2/5")
    ]
    
    for q_idx, rating, description in disc_simulation:
        answers_collector.add_disc_answer(q_idx, rating)
        print(f"  ✅ {description}")
    
    # === Подготавливаем данные для отчета ===
    print("\n📊 Подготовка данных для отчета...")
    
    # Итоговые баллы (обычно рассчитываются на основе ответов)
    paei_scores = {"P": 2, "A": 1, "E": 1, "I": 1}  # 2 раза выбрал P
    soft_skills_scores = {
        "Коммуникация": 8, "Работа в команде": 7, "Лидерство": 9,
        "Критическое мышление": 6, "Управление временем": 7,
        "Стрессоустойчивость": 8, "Эмоциональный интеллект": 8,
        "Адаптивность": 6, "Решение проблем": 9, "Креативность": 7
    }
    hexaco_scores = {"H": 4.0, "E": 3.0, "X": 5.0, "A": 4.0, "C": 3.0, "O": 4.0}
    disc_scores = {"D": 4.0, "I": 5.0, "S": 3.0, "C": 2.0}
    
    # Получаем собранные ответы
    user_answers = answers_collector.get_answers_dict()
    
    print(f"  📋 Собрано ответов:")
    print(f"    - PAEI: {len(user_answers['paei'])}")
    print(f"    - Soft Skills: {len(user_answers['soft_skills'])}")
    print(f"    - HEXACO: {len(user_answers['hexaco'])}")
    print(f"    - DISC: {len(user_answers['disc'])}")
    
    # === Генерируем отчет с разделом вопросов ===
    print("\n📄 Генерация отчета с разделом вопросов...")
    
    try:
        # Создаем генератор отчетов С разделом вопросов
        report_generator = EnhancedPDFReportV2(include_questions_section=True)
        
        # Путь к файлу отчета
        report_path = Path("bot_simulation_report_with_questions.pdf")
        
        # Генерируем отчет
        report_generator.generate_enhanced_report(
            participant_name="Симуляция Telegram Бота",
            test_date=datetime.now().strftime("%d.%m.%Y %H:%M"),
            paei_scores=paei_scores,
            disc_scores=disc_scores,
            hexaco_scores=hexaco_scores,
            soft_skills_scores=soft_skills_scores,
            ai_interpretations={
                'paei': 'Выраженная склонность к роли Производителя с элементами других стилей управления.',
                'soft_skills': 'Высокие показатели в лидерстве и решении проблем, средние в остальных областях.',
                'hexaco': 'Высокая экстраверсия, умеренные показатели по другим факторам.',
                'disc': 'Доминирует стиль Влияния (I), что характерно для общительных и мотивирующих людей.'
            },
            out_path=report_path,
            user_answers=user_answers  # 🔑 Передаем собранные ответы
        )
        
        print(f"✅ Отчет создан: {report_path}")
        
        # Показываем размер файла
        file_size = report_path.stat().st_size / 1024
        print(f"📊 Размер файла: {file_size:.1f} KB")
        
    except Exception as e:
        print(f"❌ Ошибка при создании отчета: {e}")
        import traceback
        traceback.print_exc()
    
    return user_answers


def demonstrate_bot_integration_code():
    """
    Показывает примеры кода для интеграции в Telegram бот
    """
    print("\n\n💻 ПРИМЕРЫ КОДА ДЛЯ TELEGRAM БОТА")
    print("=" * 45)
    
    print("\n1️⃣ Инициализация коллектора в UserSession:")
    print("""
class UserSession:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.name = ""
        # ... другие поля ...
        
        # Добавляем коллектор ответов для детализации
        self.answers_collector = UserAnswersCollector()
    """)
    
    print("\n2️⃣ Сохранение ответа PAEI:")
    print("""
async def handle_paei_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    
    # Получаем выбранный ответ (P, A, E, I)
    selected_answer = update.message.text.strip()[0]  # Первая буква
    
    # Обычная логика подсчета баллов
    session.paei_scores[selected_answer] += 1
    
    # НОВОЕ: сохраняем детальный ответ для раздела вопросов
    session.answers_collector.add_paei_answer(
        question_index=session.current_question,
        selected_option=selected_answer
    )
    """)
    
    print("\n3️⃣ Сохранение ответа Soft Skills:")
    print("""
async def handle_soft_skills_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    
    # Получаем оценку (1-10)
    rating = int(update.message.text.strip())
    
    # Обычная логика
    session.soft_skills_scores.append(rating)
    
    # НОВОЕ: сохраняем детальный ответ
    session.answers_collector.add_soft_skills_answer(
        question_index=session.current_question,
        rating=rating
    )
    """)
    
    print("\n4️⃣ Генерация финального отчета:")
    print("""
async def generate_final_report(user_session):
    # Выбираем, включать ли раздел вопросов
    include_questions = os.getenv('INCLUDE_QUESTIONS_SECTION', 'false').lower() == 'true'
    
    # Создаем генератор отчетов
    report_generator = EnhancedPDFReportV2(
        include_questions_section=include_questions
    )
    
    # Получаем собранные ответы (если нужны)
    user_answers = user_session.answers_collector.get_answers_dict() if include_questions else None
    
    # Генерируем отчет
    report_path, gdrive_link = report_generator.generate_enhanced_report_with_gdrive(
        participant_name=user_session.name,
        test_date=datetime.now().strftime("%d.%m.%Y %H:%M"),
        paei_scores=calculate_paei_scores(user_session),
        disc_scores=calculate_disc_scores(user_session),
        hexaco_scores=calculate_hexaco_scores(user_session),
        soft_skills_scores=calculate_soft_skills_scores(user_session),
        ai_interpretations=generate_interpretations(...),
        out_path=Path(f"report_{user_session.user_id}.pdf"),
        user_answers=user_answers  # 🔑 Передаем только если нужно
    )
    """)
    
    print("\n5️⃣ Переменная окружения для управления:")
    print("""
# В .env файле:
INCLUDE_QUESTIONS_SECTION=false  # для обычных пользователей
# INCLUDE_QUESTIONS_SECTION=true  # для исследователей/психологов
    """)


if __name__ == "__main__":
    # Запускаем симуляцию
    user_answers = simulate_user_session_with_questions()
    
    # Показываем примеры интеграции
    demonstrate_bot_integration_code()
    
    print(f"\n🎉 СИМУЛЯЦИЯ ЗАВЕРШЕНА!")
    print(f"📄 Создан файл: bot_simulation_report_with_questions.pdf")
    print(f"📋 Собрано {sum(len(answers) for answers in user_answers.values())} ответов")