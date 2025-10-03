#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram бот для психологического тестирования v1.0
Готов к тестированию на телефоне
"""

import logging
import asyncio
import tempfile
import os
from pathlib import Path
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Импорты наших модулей
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from src.psytest.ai_interpreter import get_ai_interpreter
from tests.test_scenarios import TEST_SCENARIOS
from report_archiver import save_report_copy
from scale_normalizer import ScaleNormalizer

# === НАСТРОЙКИ ===
BOT_TOKEN = "8250482375:AAH3ZCQ3s6XJyl5g32sY63g5HKOHnqGq1WQ"

# Состояния диалога
(WAITING_START, WAITING_NAME, PAEI_TESTING, DISC_TESTING, HEXACO_TESTING, SOFT_SKILLS_TESTING) = range(6)

# === НАСТРОЙКА ЛОГИРОВАНИЯ ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === ХРАНИЛИЩЕ ПОЛЬЗОВАТЕЛЕЙ ===
user_sessions = {}

class UserSession:
    """Класс для хранения данных пользователя"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.name = ""
        self.phone = ""
        self.paei_scores = {"P": 0, "A": 0, "E": 0, "I": 0}
        self.disc_scores = {"D": 0, "I": 0, "S": 0, "C": 0}
        self.hexaco_scores = []  # Список для хранения ответов HEXACO (шкала 1-5)
        self.soft_skills_scores = []  # Список для хранения ответов Soft Skills (шкала 1-10)
        self.current_test = ""
        self.current_question = 0
        self.started_at = datetime.now()

# === ТЕСТОВЫЕ ДАННЫЕ ===
PAEI_QUESTIONS = [
    {
        "question": "В работе вы больше склонны:",
        "answers": {
            "A": "Планировать и контролировать процессы",
            "P": "Достигать конкретных результатов", 
            "E": "Искать новые возможности",
            "I": "Объединять людей для совместной работы"
        }
    },
    {
        "question": "При принятии решений вы:",
        "answers": {
            "A": "Анализируете все детали и риски",
            "P": "Фокусируетесь на практическом результате",
            "E": "Ищете инновационные подходы",
            "I": "Учитываете мнения всех участников"
        }
    },
    {
        "question": "В команде вы чаще:",
        "answers": {
            "A": "Организуете рабочие процессы",
            "P": "Выполняете ключевые задачи",
            "E": "Предлагаете новые идеи", 
            "I": "Поддерживаете атмосферу сотрудничества"
        }
    },
    {
        "question": "Как вы подходите к выполнению нового проекта?",
        "answers": {
            "P": "Сразу приступаю к работе, чтобы как можно быстрее увидеть результат",
            "A": "В первую очередь разрабатываю структуру и последовательность действий",
            "E": "Начинаю с поиска новых идей и возможностей",
            "I": "Убеждаюсь, что все члены команды понимают свои роли"
        }
    },
    {
        "question": "Какой формат работы вам наиболее комфортен?",
        "answers": {
            "P": "Быстрое выполнение задач с четкими целями",
            "A": "Работа в стабильной системе с заранее установленными правилами",
            "E": "Проекты, требующие творчества и гибкости",
            "I": "Работа в команде с акцентом на взаимодействие и коммуникацию"
        }
    }
]

DISC_QUESTIONS = [
    {
        "question": "В сложной ситуации вы:",
        "answers": {
            "D": "Берете инициативу и действуете решительно",
            "I": "Вдохновляете других на совместные действия",
            "S": "Сохраняете спокойствие и поддерживаете команду",
            "C": "Тщательно анализируете ситуацию"
        }
    },
    {
        "question": "Ваш стиль общения:",
        "answers": {
            "D": "Прямой и нацеленный на результат",
            "I": "Эмоциональный и вдохновляющий",
            "S": "Терпеливый и поддерживающий",
            "C": "Точный и основанный на фактах"
        }
    },
    {
        "question": "В работе вы цените:",
        "answers": {
            "D": "Быстрые результаты и достижения",
            "I": "Общение и признание",
            "S": "Стабильность и гармонию",
            "C": "Качество и точность"
        }
    },
    {
        "question": "При решении сложных задач:",
        "answers": {
            "D": "Беру на себя полную ответственность за результат",
            "I": "Мотивирую команду на достижение целей",
            "S": "Предпочитаю стабильные и проверенные методы",
            "C": "Тщательно проверяю все детали и стандарты"
        }
    },
    {
        "question": "В достижении целей:",
        "answers": {
            "D": "Стремлюсь к быстрым результатам, даже если это требует рисков",
            "I": "Вдохновляю других на новые идеи и подходы",
            "S": "Следую установленным процедурам",
            "C": "Предпочитаю четко структурированные задачи"
        }
    },
    {
        "question": "В социальном взаимодействии:",
        "answers": {
            "D": "Предпочитаю прямое и эффективное общение",
            "I": "Легко завожу новые знакомства и активно общаюсь",
            "S": "Поддерживаю гармоничные отношения в команде",
            "C": "Общаюсь основываясь на фактах и логике"
        }
    },
    {
        "question": "В рабочей среде:",
        "answers": {
            "D": "Предпочитаю динамичную среду с вызовами",
            "I": "Ценю открытое общение и признание заслуг",
            "S": "Предпочитаю стабильную среду без резких изменений",
            "C": "Работаю лучше в структурированной среде с четкими правилами"
        }
    },
    {
        "question": "При планировании проектов:",
        "answers": {
            "D": "Фокусируюсь на конечном результате и скорости выполнения",
            "I": "Уделяю внимание вовлечению команды и мотивации",
            "S": "Обеспечиваю последовательность и избегаю резких изменений",
            "C": "Детально прорабатываю все этапы и процессы"
        }
    }
]

HEXACO_QUESTIONS = [
    {
        "question": "Я предпочитаю говорить правду, даже если это неудобно",
        "scale": "1-5",
        "dimension": "H"  # Honesty-Humility
    },
    {
        "question": "Я часто чувствую беспокойство о будущем",
        "scale": "1-5", 
        "dimension": "E"  # Emotionality
    },
    {
        "question": "Я люблю быть в центре внимания",
        "scale": "1-5",
        "dimension": "X"  # eXtraversion
    },
    {
        "question": "Я стараюсь следовать своим планам, даже если они сложные",
        "scale": "1-5",
        "dimension": "A"  # Agreeableness
    },
    {
        "question": "Мне легко найти общий язык с другими людьми",
        "scale": "1-5",
        "dimension": "C"  # Conscientiousness
    },
    {
        "question": "Я наслаждаюсь изучением новых идей и концепций",
        "scale": "1-5",
        "dimension": "O"  # Openness to experience
    }
]

SOFT_SKILLS_QUESTIONS = [
    {
        "question": "Насколько эффективно вы можете объяснить сложные идеи другим?",
        "scale": "1-10",
        "skill": "Коммуникация"
    },
    {
        "question": "Как часто вы берете на себя инициативу в групповых проектах?",
        "scale": "1-10",
        "skill": "Лидерство"
    },
    {
        "question": "Насколько хорошо вы планируете свое время и ресурсы?",
        "scale": "1-10",
        "skill": "Планирование"
    },
    {
        "question": "Как легко вы адаптируетесь к изменениям в рабочих процессах?",
        "scale": "1-10",
        "skill": "Адаптивность"
    },
    {
        "question": "Насколько глубоко вы анализируете проблемы перед принятием решений?",
        "scale": "1-10",
        "skill": "Аналитика"
    },
    {
        "question": "Как часто вы предлагаете нестандартные решения задач?",
        "scale": "1-10",
        "skill": "Творчество"
    },
    {
        "question": "Насколько эффективно вы работаете в команде?",
        "scale": "1-10",
        "skill": "Командная работа"
    },
    {
        "question": "Как хорошо вы справляетесь со стрессовыми ситуациями?",
        "scale": "1-10",
        "skill": "Стрессоустойчивость"
    },
    {
        "question": "Насколько критично вы оцениваете качество своей работы?",
        "scale": "1-10",
        "skill": "Самоконтроль"
    },
    {
        "question": "Как эффективно вы можете убедить других в своей точке зрения?",
        "scale": "1-10",
        "skill": "Влияние"
    }
]

# === ОБРАБОТЧИКИ БОТА ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало работы с ботом"""
    user_id = update.effective_user.id
    
    # Добавляем логирование для диагностики
    logger.info(f"🚀 Получена команда /start от пользователя {user_id}")
    
    welcome_text = """
🎯 <b>Добро пожаловать в систему оценки командных навыков!</b>

Я проведу с вами комплексное психологическое тестирование по методикам:
• 📊 PAEI (Адизес) - управленческие роли
• 🎭 DISC - поведенческие стили  
• 🧠 HEXACO - личностные черты
• 💡 Soft Skills - надпрофессиональные навыки

📋 <b>Процесс:</b>
1. Регистрация (только ФИО)
2. Прохождение тестов (~10 минут)
3. Получение PDF отчета

Готовы начать?
    """
    
    keyboard = [["✅ Да, начать тестирование"], ["❌ Нет, не сейчас"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        welcome_text, 
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    
    return WAITING_START

async def handle_start_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка подтверждения начала"""
    text = update.message.text
    
    if "Да" in text:
        await update.message.reply_text(
            "📝 Отлично! Давайте начнем с регистрации.\n\n"
            "Пожалуйста, введите ваши <b>Фамилию и Имя</b>:",
            parse_mode='HTML',
            reply_markup=ReplyKeyboardRemove()
        )
        return WAITING_NAME
    else:
        await update.message.reply_text(
            "Хорошо! Когда будете готовы, напишите /start",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка ввода имени"""
    user_id = update.effective_user.id
    name = update.message.text.strip()
    
    # Создаем сессию пользователя
    user_sessions[user_id] = UserSession(user_id)
    user_sessions[user_id].name = name
    user_sessions[user_id].phone = ""  # Пустой телефон по умолчанию

    keyboard = [
        ["🎯 Начать тестирование"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        f"👋 Приветствую, <b>{name}</b>!\n\n"
        f"🎯 Готовы начать психологическое тестирование командных навыков?\n\n"
        f"Вас ждут три теста:\n"
        f"📊 <b>PAEI</b> - управленческие роли\n" 
        f"🎭 <b>DISC</b> - поведенческий стиль\n"
        f"🧠 <b>HEXACO & Soft Skills</b> - личностные качества\n\n"
        f"Вопрос 1 из {len(PAEI_QUESTIONS)}:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

    return await start_paei_test(update, context)

async def start_paei_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает тест PAEI"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    session.current_test = "PAEI"
    session.current_question = 0
    
    return await ask_paei_question(update, context)

async def ask_paei_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Задает вопрос PAEI"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    
    if session.current_question >= len(PAEI_QUESTIONS):
        return await start_disc_test(update, context)
    
    question_data = PAEI_QUESTIONS[session.current_question]
    
    # Формируем клавиатуру с вариантами ответов
    keyboard = []
    for key, answer in question_data["answers"].items():
        keyboard.append([f"{key}. {answer}"])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        f"📊 <b>PAEI - Вопрос {session.current_question + 1}/{len(PAEI_QUESTIONS)}</b>\n\n"
        f"{question_data['question']}",
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    
    return PAEI_TESTING

async def handle_paei_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает ответ PAEI"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    answer_text = update.message.text
    
    # Извлекаем код ответа (P, A, E, I)
    answer_code = answer_text[0] if answer_text else ""
    
    if answer_code in ["P", "A", "E", "I"]:
        session.paei_scores[answer_code] += 1
        session.current_question += 1
        return await ask_paei_question(update, context)
    else:
        await update.message.reply_text("❗ Пожалуйста, выберите один из предложенных вариантов")
        return PAEI_TESTING

async def start_disc_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает тест DISC"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    session.current_test = "DISC"
    session.current_question = 0
    
    await update.message.reply_text(
        f"✅ <b>PAEI завершен!</b>\n\n"
        f"🎭 Переходим к тесту DISC (поведенческие стили)\n"
        f"Вопрос 1 из {len(DISC_QUESTIONS)}:",
        parse_mode='HTML'
    )
    
    return await ask_disc_question(update, context)

async def ask_disc_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Задает вопрос DISC"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    
    logger.info(f"📋 ask_disc_question: current_question={session.current_question}, len={len(DISC_QUESTIONS)}")
    
    if session.current_question >= len(DISC_QUESTIONS):
        logger.info(f"🎯 DISC завершен! Запускаем HEXACO тест")
        return await start_hexaco_test(update, context)
    
    question_data = DISC_QUESTIONS[session.current_question]
    
    keyboard = []
    for key, answer in question_data["answers"].items():
        keyboard.append([f"{key}. {answer}"])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    logger.info(f"❓ Отправляем DISC вопрос {session.current_question + 1}/{len(DISC_QUESTIONS)}")
    
    await update.message.reply_text(
        f"🎭 <b>DISC - Вопрос {session.current_question + 1}/{len(DISC_QUESTIONS)}</b>\n\n"
        f"{question_data['question']}",
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    
    return DISC_TESTING

async def handle_disc_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает ответ DISC"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    answer_text = update.message.text
    
    # Добавляем подробное логирование
    logger.info(f"📝 DISC ответ от {user_id}: '{answer_text}'")
    logger.info(f"📊 Текущий вопрос: {session.current_question + 1}/{len(DISC_QUESTIONS)}")
    
    answer_code = answer_text[0] if answer_text else ""
    logger.info(f"🔤 Код ответа: '{answer_code}'")
    
    if answer_code in ["D", "I", "S", "C"]:
        session.disc_scores[answer_code] += 1
        session.current_question += 1
        logger.info(f"✅ Ответ принят. Новый current_question: {session.current_question}")
        logger.info(f"📈 Счет DISC: {session.disc_scores}")
        
        if session.current_question >= len(DISC_QUESTIONS):
            logger.info(f"🎯 DISC завершен! Переходим к HEXACO")
        
        return await ask_disc_question(update, context)
    else:
        logger.warning(f"❌ Неверный ответ DISC: '{answer_text}' -> '{answer_code}'")
        await update.message.reply_text("❗ Пожалуйста, выберите один из предложенных вариантов")
        return DISC_TESTING

async def start_hexaco_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает тест HEXACO"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    
    logger.info(f"🧠 Начинаем HEXACO тест для пользователя {user_id}")
    logger.info(f"📊 Финальные результаты DISC: {session.disc_scores}")
    
    session.current_test = "HEXACO"
    session.current_question = 0
    
    await update.message.reply_text(
        "🧠 <b>Начинаем тест HEXACO</b>\n\n"
        "Сейчас вам будут предложены утверждения.\n"
        "Оцените каждое по шкале от 1 до 5:\n"
        "1 - Совершенно не согласен\n"
        "2 - Скорее не согласен\n"
        "3 - Нейтрально\n"
        "4 - Скорее согласен\n"
        "5 - Полностью согласен",
        parse_mode='HTML'
    )
    
    logger.info(f"📝 Переходим к первому вопросу HEXACO")
    return await ask_hexaco_question(update, context)

async def ask_hexaco_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Задает вопрос HEXACO"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    
    if session.current_question >= len(HEXACO_QUESTIONS):
        return await start_soft_skills_test(update, context)
    
    question_data = HEXACO_QUESTIONS[session.current_question]
    
    keyboard = [
        ["1", "2", "3", "4", "5"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        f"🧠 <b>HEXACO - Вопрос {session.current_question + 1}/{len(HEXACO_QUESTIONS)}</b>\n\n"
        f"{question_data['question']}",
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    
    return HEXACO_TESTING

async def handle_hexaco_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает ответ HEXACO"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    answer_text = update.message.text
    
    try:
        score = int(answer_text)
        if 1 <= score <= 5:
            # Сохраняем ответ в список (позже будем делать среднее)
            session.hexaco_scores.append(score)
            
            session.current_question += 1
            return await ask_hexaco_question(update, context)
        else:
            await update.message.reply_text("❗ Пожалуйста, выберите число от 1 до 5")
            return HEXACO_TESTING
    except ValueError:
        await update.message.reply_text("❗ Пожалуйста, выберите число от 1 до 5")
        return HEXACO_TESTING

async def start_soft_skills_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает тест Soft Skills"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    session.current_test = "SOFT_SKILLS"
    session.current_question = 0
    
    await update.message.reply_text(
        "💪 <b>Начинаем тест Soft Skills</b>\n\n"
        "Оцените свои навыки по шкале от 1 до 10:\n"
        "1 - Очень слабо развит\n"
        "5 - Средне развит\n"
        "10 - Отлично развит",
        parse_mode='HTML'
    )
    
    return await ask_soft_skills_question(update, context)

async def ask_soft_skills_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Задает вопрос Soft Skills"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    
    if session.current_question >= len(SOFT_SKILLS_QUESTIONS):
        return await complete_testing(update, context)
    
    question_data = SOFT_SKILLS_QUESTIONS[session.current_question]
    
    keyboard = [
        ["1", "2", "3", "4", "5"],
        ["6", "7", "8", "9", "10"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        f"💪 <b>Soft Skills - Вопрос {session.current_question + 1}/{len(SOFT_SKILLS_QUESTIONS)}</b>\n\n"
        f"{question_data['question']}",
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    
    return SOFT_SKILLS_TESTING

async def handle_soft_skills_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает ответ Soft Skills"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    answer_text = update.message.text
    
    try:
        score = int(answer_text)
        if 1 <= score <= 10:
            # Сохраняем ответ в список
            session.soft_skills_scores.append(score)
            
            session.current_question += 1
            return await ask_soft_skills_question(update, context)
        else:
            await update.message.reply_text("❗ Пожалуйста, выберите число от 1 до 10")
            return SOFT_SKILLS_TESTING
    except ValueError:
        await update.message.reply_text("❗ Пожалуйста, выберите число от 1 до 10")
        return SOFT_SKILLS_TESTING

async def complete_testing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершает тестирование и генерирует отчет"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    
    await update.message.reply_text(
        "🎉 <b>Тестирование завершено!</b>\n\n"
        "⏳ Генерируем ваш персональный отчет...\n"
        "Это займет несколько секунд.",
        parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove()
    )
    
    try:
        # Преобразуем счетчики в осмысленные баллы 1-10
        # PAEI: конвертируем счетчики в баллы на основе доминирующих ролей
        total_paei = sum(session.paei_scores.values()) or 1
        session.paei_scores = {
            "P": round(1 + (session.paei_scores["P"] / total_paei) * 9, 1),
            "A": round(1 + (session.paei_scores["A"] / total_paei) * 9, 1), 
            "E": round(1 + (session.paei_scores["E"] / total_paei) * 9, 1),
            "I": round(1 + (session.paei_scores["I"] / total_paei) * 9, 1)
        }
        
        # DISC: конвертируем счетчики в баллы на основе доминирующих стилей
        total_disc = sum(session.disc_scores.values()) or 1
        session.disc_scores = {
            "D": round(1 + (session.disc_scores["D"] / total_disc) * 9, 1),
            "I": round(1 + (session.disc_scores["I"] / total_disc) * 9, 1),
            "S": round(1 + (session.disc_scores["S"] / total_disc) * 9, 1),
            "C": round(1 + (session.disc_scores["C"] / total_disc) * 9, 1)
        }
        
        # HEXACO: преобразуем список ответов в средние баллы по измерениям
        # У нас 6 вопросов (по одному на каждое измерение HEXACO)
        hexaco_dimensions = ["H", "E", "X", "A", "C", "O"]
        if len(session.hexaco_scores) == 6:
            hexaco_dict = {}
            for i, dimension in enumerate(hexaco_dimensions):
                score = session.hexaco_scores[i]  # Оценка 1-5
                # Конвертируем в шкалу 1-10
                hexaco_dict[dimension] = round((score / 5.0) * 10.0, 1)
            session.hexaco_scores = hexaco_dict
        else:
            # Если данных недостаточно, используем средние значения
            session.hexaco_scores = {dim: 5.0 for dim in hexaco_dimensions}
        
        # Soft Skills: преобразуем список ответов в словарь навыков
        soft_skills_names = ["Коммуникация", "Лидерство", "Работа в команде", "Критическое мышление",
                            "Решение проблем", "Адаптивность", "Управление временем", "Эмоциональный интеллект",
                            "Креативность", "Стрессоустойчивость"]
        if len(session.soft_skills_scores) == 10:
            soft_skills_dict = {}
            for i, skill_name in enumerate(soft_skills_names):
                soft_skills_dict[skill_name] = session.soft_skills_scores[i]  # Уже в шкале 1-10
            session.soft_skills_scores = soft_skills_dict
        else:
            # Если данных недостаточно, используем средние значения
            session.soft_skills_scores = {skill: 5.0 for skill in soft_skills_names}
        
        # Генерируем PDF отчет
        pdf_path = await generate_user_report(session)
        
        # Отправляем PDF пользователю
        with open(pdf_path, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename=f"Отчет_{session.name.replace(' ', '_')}.pdf",
                caption=f"📊 <b>Ваш персональный отчет готов!</b>\n\n"
                       f"👤 {session.name}\n"
                       f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                       f"📋 Отчет содержит детальный анализ по всем методикам.",
                parse_mode='HTML'
            )
        
        # Удаляем временный файл
        os.unlink(pdf_path)
        
        await update.message.reply_text(
            "✅ <b>Готово!</b>\n\n"
            "📄 Ваш отчет отправлен выше.\n"
            "💡 Сохраните его для дальнейшего использования.\n\n"
            "Спасибо за прохождение тестирования! 🎯",
            parse_mode='HTML'
        )
        
    except Exception as e:
        logger.error(f"Ошибка генерации отчета: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при генерации отчета.\n"
            "Попробуйте еще раз или обратитесь в поддержку."
        )
    
    # Очищаем сессию
    if user_id in user_sessions:
        del user_sessions[user_id]
    
    return ConversationHandler.END

async def generate_user_report(session: UserSession) -> str:
    """Генерирует PDF отчет для пользователя"""
    
    # Создаем временную папку для диаграмм
    temp_dir = tempfile.mkdtemp()
    temp_charts_dir = Path(temp_dir) / "charts"
    temp_charts_dir.mkdir(exist_ok=True)
    
    # Инициализируем генератор PDF
    pdf_generator = EnhancedPDFReportV2(template_dir=temp_charts_dir)
    
    # Инициализируем AI интерпретатор
    ai_interpreter = get_ai_interpreter()
    
    # Подготавливаем интерпретации с помощью AI или используем базовые
    interpretations = {}
    
    if ai_interpreter:
        # Используем AI для генерации интерпретаций
        try:
            interpretations["paei"] = ai_interpreter.interpret_paei(session.paei_scores)
            interpretations["disc"] = ai_interpreter.interpret_disc(session.disc_scores)
            interpretations["hexaco"] = ai_interpreter.interpret_hexaco(session.hexaco_scores)
            interpretations["soft_skills"] = ai_interpreter.interpret_soft_skills(session.soft_skills_scores)
        except Exception as e:
            print(f"⚠️ Ошибка AI интерпретации: {e}")
            # Fallback на базовые интерпретации
            interpretations = {
                "paei": f"Управленческий профиль показывает преобладание определенных ролей. "
                        f"Результаты PAEI: {session.paei_scores}",
                "disc": f"Поведенческий стиль характеризуется особенностями взаимодействия. "
                        f"Результаты DISC: {session.disc_scores}",
                "hexaco": f"Личностный профиль демонстрирует сбалансированное развитие основных черт. "
                         f"Результаты HEXACO: {session.hexaco_scores}",
                "soft_skills": f"Профессиональные навыки характеризуются определенным уровнем развития. "
                              f"Результаты Soft Skills: {session.soft_skills_scores}"
            }
    else:
        # Используем базовые интерпретации если AI недоступен
        interpretations = {
            "paei": f"Управленческий профиль показывает преобладание определенных ролей. "
                    f"Результаты PAEI: {session.paei_scores}",
            "disc": f"Поведенческий стиль характеризуется особенностями взаимодействия. "
                    f"Результаты DISC: {session.disc_scores}",
            "hexaco": f"Личностный профиль демонстрирует сбалансированное развитие основных черт. "
                     f"Результаты HEXACO: {session.hexaco_scores}",
            "soft_skills": f"Профессиональные навыки характеризуются определенным уровнем развития. "
                          f"Результаты Soft Skills: {session.soft_skills_scores}"
        }
    
    # Путь для сохранения PDF в папку docs/
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{session.name.replace(' ', '_') if session.name else 'TelegramUser'}_tg_{str(session.user_id)[-4:]}.pdf"
    pdf_path = docs_dir / filename
    
    # Нормализуем баллы к единой шкале 0-10
    paei_normalized, paei_method = ScaleNormalizer.auto_normalize("PAEI", session.paei_scores)
    disc_normalized, disc_method = ScaleNormalizer.auto_normalize("DISC", session.disc_scores)
    hexaco_normalized, hexaco_method = ScaleNormalizer.auto_normalize("HEXACO", session.hexaco_scores)
    soft_skills_normalized, soft_skills_method = ScaleNormalizer.auto_normalize("SOFT_SKILLS", session.soft_skills_scores)
    
    logger.info(f"📏 Нормализация шкал:")
    logger.info(f"  {paei_method}")
    logger.info(f"  {disc_method}")
    logger.info(f"  {hexaco_method}")
    logger.info(f"  {soft_skills_method}")
    
    # Генерируем отчет с нормализованными баллами
    pdf_generator.generate_enhanced_report(
        participant_name=session.name,
        test_date=datetime.now().strftime("%Y-%m-%d"),
        paei_scores=paei_normalized,
        disc_scores=disc_normalized,
        hexaco_scores=hexaco_normalized,
        soft_skills_scores=soft_skills_normalized,
        ai_interpretations=interpretations,
        out_path=pdf_path
    )
    
    # Отчет уже сохранен в docs/, дополнительное архивирование не требуется
    logger.info(f"📁 Отчет сохранен: {pdf_path.name}")
    
    # (Архивирование отключено, так как файл уже в правильном месте)
    # try:
    #     user_info = {
    #         "telegram_id": session.user_id,
    #         "name": session.name if session.name else "TelegramUser"
    #     }
    #     
    #     # Определяем доминирующий тест для имени файла (используем нормализованные значения)
    #     max_paei = max(paei_normalized.values()) if paei_normalized else 0
    #     max_disc = max(disc_normalized.values()) if disc_normalized else 0
    #     
    #     if max_paei >= max_disc:
    #         test_type = f"PAEI_{max(paei_normalized, key=paei_normalized.get)}"
    #     else:
    #         test_type = f"DISC_{max(disc_normalized, key=disc_normalized.get)}"
    #     
    #     archived_path = save_report_copy(pdf_path, test_type, user_info)
    #     if archived_path:
    #         logger.info(f"📁 Отчет архивирован: {archived_path.name}")
    #     
    # except Exception as e:
    #     logger.warning(f"⚠️ Не удалось архивировать отчет: {e}")
    
    return str(pdf_path)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена тестирования"""
    user_id = update.effective_user.id
    
    if user_id in user_sessions:
        del user_sessions[user_id]
    
    await update.message.reply_text(
        "❌ Тестирование отменено.\n\n"
        "Чтобы начать заново, напишите /start",
        reply_markup=ReplyKeyboardRemove()
    )
    
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Помощь"""
    help_text = """
🤖 <b>Бот для оценки командных навыков</b>

<b>Команды:</b>
/start - Начать тестирование
/cancel - Отменить текущее тестирование  
/help - Показать эту справку

<b>О тестировании:</b>
• Время прохождения: ~10 минут
• Методики: PAEI, DISC, HEXACO, Soft Skills
• Результат: Персональный PDF отчет

<b>Поддержка:</b> @your_support_contact
    """
    
    await update.message.reply_text(help_text, parse_mode='HTML')

def main():
    """Основная функция запуска бота"""
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Создаем ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_start_confirmation)],
            WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
            PAEI_TESTING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_paei_answer)],
            DISC_TESTING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_disc_answer)],
            HEXACO_TESTING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hexaco_answer)],
            SOFT_SKILLS_TESTING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_soft_skills_answer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Добавляем обработчики
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    
    # Запускаем бота
    logger.info("🤖 Бот запущен и готов к работе!")
    logger.info("📱 Telegram: @psychtestteambot")
    print("🚀 Бот запущен! Можно тестировать в Telegram: @psychtestteambot")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()