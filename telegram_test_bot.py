#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram бот для психологического тестирования v1.0
Готов к тестированию на телефоне
"""

# pyright: reportOptionalMemberAccess=false
# pyright: reportGeneralTypeIssues=false
# pyright: reportOptionalSubscript=false
# pylance: disable=reportOptionalMemberAccess,reportGeneralTypeIssues

import logging
import asyncio
import tempfile
import shutil
import os
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Загружаем переменные окружения
load_dotenv()

# Импорты наших модулей
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from interpretation_utils import generate_interpretations_from_prompt
from src.psytest.ai_interpreter import get_ai_interpreter
from report_archiver import save_report_copy
from scale_normalizer import ScaleNormalizer
from bot_integration_example import UserAnswersCollector

# === НАСТРОЙКИ ===
# Загружаем токен бота из переменной окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения. Проверьте файл .env")

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
        
        # Новое: коллектор ответов для детального раздела в отчете
        self.answers_collector = UserAnswersCollector()

# === ФУНКЦИИ ПАРСИНГА ВОПРОСОВ ===

def parse_adizes_questions(filepath="data/prompts/adizes_user.txt"):
    """Парсит вопросы PAEI/Adizes из файла"""
    try:
        questions = []
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Разбиваем на блоки вопросов (ищем паттерн с номером)
        question_blocks = re.split(r'\n(?=\d+\.)', content)
        
        for block in question_blocks:
            if not block.strip() or not re.match(r'^\d+\.', block.strip()):
                continue
                
            lines = block.strip().split('\n')
            question_text = lines[0].strip()
            
            # Извлекаем сам вопрос (убираем номер)
            question_text = re.sub(r'^\d+\.\s*', '', question_text)
            
            answers = {}
            for line in lines[1:]:
                line = line.strip()
                if re.match(r'^[PAEI]\.', line):
                    code = line[0]  # P, A, E, или I
                    answer_text = re.sub(r'^[PAEI]\.\s*', '', line)
                    answers[code] = answer_text
            
            if question_text and len(answers) == 4:  # Должно быть 4 ответа
                questions.append({
                    "question": question_text,
                    "answers": answers
                })
        
        logger.info(f"📊 Загружено {len(questions)} PAEI вопросов из {filepath}")
        return questions
        
    except Exception as e:
        logger.error(f"❌ Ошибка при загрузке PAEI вопросов: {e}")
        return []

def parse_disc_questions(filepath="data/prompts/disc_user.txt"):
    """Парсит вопросы DISC из файла"""
    try:
        questions = []
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Разбиваем на блоки по категориям (Доминирование, Влияние, Устойчивость, Подчинение правилам)
        category_blocks = re.split(r'\n(?=\d+\.)', content)
        
        disc_categories = {
            1: "D",  # Доминирование
            2: "I",  # Влияние  
            3: "S",  # Устойчивость (Steadiness)
            4: "C"   # Подчинение правилам (Compliance)
        }
        
        for block in category_blocks:
            if not block.strip():
                continue
                
            lines = block.strip().split('\n')
            if not lines:
                continue
                
            # Извлекаем название категории и номер
            first_line = lines[0].strip()
            category_match = re.match(r'^(\d+)\.\s*(.+?):', first_line)
            if not category_match:
                continue
                
            category_num = int(category_match.group(1))
            category_name = category_match.group(2)
            
            if category_num not in disc_categories:
                continue
                
            disc_code = disc_categories[category_num]
            
            # Извлекаем подвопросы
            for line in lines[1:]:
                line = line.strip()
                if re.match(r'^\d+\.\d+', line):  # Формат 1.1, 1.2 и т.д.
                    # Убираем номер и создаем вопрос
                    question_text = re.sub(r'^\d+\.\d+\s*', '', line)
                    
                    if question_text:
                        # Создаем вопрос в формате шкалы 1-5 вместо D/I/S/C
                        questions.append({
                            "question": question_text,
                            "category": disc_code,
                            "category_name": category_name
                        })
        
        logger.info(f"📊 Загружено {len(questions)} DISC вопросов из {filepath}")
        return questions
        
    except Exception as e:
        logger.error(f"❌ Ошибка при загрузке DISC вопросов: {e}")
        return []

def parse_soft_skills_questions(filepath="data/prompts/soft_user.txt"):
    """Парсинг вопросов Soft Skills из файла промптов"""
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as file:  # utf-8-sig убирает BOM
            content = file.read()
    except FileNotFoundError:
        logger.error(f"❌ Файл {filepath} не найден")
        return []
    
    lines = content.strip().split('\n')
    questions = []
    current_question = None
    collecting_answers = False
    answers = []
    
    # Новый mapping навыков на номера вопросов (уникальные soft skills)
    skills_mapping = {
        1: "Коммуникация",
        2: "Работа в команде",
        3: "Лидерство",
        4: "Критическое мышление",
        5: "Управление временем",
        6: "Стрессоустойчивость",
        7: "Эмоциональный интеллект",
        8: "Адаптивность",
        9: "Решение проблем",
        10: "Креативность"
    }
    
    for i, line in enumerate(lines):
        original_line = line
        line = line.strip()
        if not line:
            continue
            
        # Пропускаем инструкции в начале файла
        if (line.startswith('Вот список') or line.startswith('1 =') or line.startswith('2 =') or 
            line.startswith('3 =') or line.startswith('4 =') or line.startswith('5 =') or 
            line.startswith('Задавай') or line.startswith('где:') or line.endswith('где:')):
            continue
            
        # Ищем начало нового ОСНОВНОГО вопроса (без отступа в начале строки)
        if (not original_line.startswith('  ') and  # НЕТ отступа в 2 пробела
            line and line[0].isdigit() and '. ' in line):
            
            # Сохраняем предыдущий вопрос
            if current_question and answers:
                question_num = len(questions) + 1
                skill = skills_mapping.get(question_num, "Общие навыки")
                questions.append({
                    'question': current_question,
                    'scale': "1-5",
                    'skill': skill,
                    'answers': answers.copy()
                })
                answers = []
            
            # Начинаем новый вопрос
            parts = line.split('. ', 1)
            if len(parts) == 2:
                current_question = parts[1]
                collecting_answers = True
        
        # Собираем варианты ответов (начинаются с "  1.", "  2." и т.д.)
        elif (collecting_answers and 
              original_line.startswith('  ') and  # ЕСТЬ отступ в 2 пробела
              len(original_line) > 2):
            
            clean_line = original_line[2:]  # Убираем два пробела
            if clean_line and clean_line[0].isdigit() and '. ' in clean_line:
                answer_parts = clean_line.split('. ', 1)
                if len(answer_parts) == 2:
                    try:
                        answer_num = int(answer_parts[0])
                        answer_text = answer_parts[1]
                        answers.append({'value': answer_num, 'text': answer_text})
                    except ValueError:
                        continue
    
    # Добавляем последний вопрос
    if current_question and answers:
        question_num = len(questions) + 1
        skill = skills_mapping.get(question_num, "Общие навыки")
        questions.append({
            'question': current_question,
            'scale': "1-5",
            'skill': skill,
            'answers': answers.copy()
        })
    
    if questions:
        logger.info(f"📊 Загружено {len(questions)} Soft Skills вопросов из {filepath}")
    else:
        logger.error(f"❌ Не удалось загрузить Soft Skills вопросы из {filepath}")
    
    return questions

# === ТЕСТОВЫЕ ДАННЫЕ ===
# Загружаем PAEI вопросы из файла или используем резервные
PAEI_QUESTIONS = parse_adizes_questions()
if not PAEI_QUESTIONS:
    # Резервные вопросы на случай ошибки загрузки
    PAEI_QUESTIONS = [
        {
            "question": "В работе вы больше склонны:",
            "answers": {
                "A": "Планировать и контролировать процессы",
                "P": "Достигать конкретных результатов", 
                "E": "Искать новые возможности",
                "I": "Объединять людей для совместной работы"
            }
        }
    ]

# Загружаем DISC вопросы из файла
DISC_QUESTIONS = parse_disc_questions()
if not DISC_QUESTIONS:
    logger.error("❌ Не удалось загрузить DISC вопросы из файла!")
    # Резервные DISC вопросы на случай ошибки загрузки
    DISC_QUESTIONS = [
        {
            "question": "В сложной ситуации вы:",
            "answers": {
                "D": "Берете инициативу и действуете решительно",
                "I": "Вдохновляете других на совместные действия",
                "S": "Сохраняете спокойствие и поддерживаете команду",
                "C": "Тщательно анализируете ситуацию"
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

# Загружаем Soft Skills вопросы из файла
def get_soft_skills_names() -> list[str]:
    """Извлекает названия навыков из SOFT_SKILLS_QUESTIONS"""
    try:
        return [question.get("skill", f"Навык {i+1}") for i, question in enumerate(SOFT_SKILLS_QUESTIONS)]
    except Exception as e:
        logger.warning(f"Ошибка при извлечении названий навыков: {e}")
        # Fallback на базовые названия
        return ["Коммуникация", "Лидерство", "Работа в команде", "Критическое мышление",
                "Решение проблем", "Адаптивность", "Управление временем", "Эмоциональный интеллект",
                "Креативность", "Стрессоустойчивость"]

SOFT_SKILLS_QUESTIONS = parse_soft_skills_questions()
if not SOFT_SKILLS_QUESTIONS:
    logger.error("❌ Не удалось загрузить Soft Skills вопросы из файла!")
    # Резервные Soft Skills вопросы на случай ошибки загрузки
    SOFT_SKILLS_QUESTIONS = [
        {
            "question": "Насколько эффективно вы можете объяснить сложные идеи другим?",
            "scale": "1-5",
            "skill": "Коммуникация"
        },
        {
            "question": "Как часто вы берете на себя инициативу в групповых проектах?",
            "scale": "1-5",
            "skill": "Лидерство"
        }
    ]

# === ОБРАБОТЧИКИ БОТА ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало работы с ботом"""
    if not update.effective_user or not update.message:
        return ConversationHandler.END
        
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

    await update.message.reply_text(
        f"👋 Приветствую, <b>{name}</b>! Сейчас начнём тестирование.\n",
        parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove()
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
        return await start_soft_skills_test(update, context)
    
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
        # Обычная логика подсчета баллов
        session.paei_scores[answer_code] += 1
        
        # НОВОЕ: сохраняем детальный ответ для раздела вопросов
        session.answers_collector.add_paei_answer(
            question_index=session.current_question,
            selected_option=answer_code
        )
        
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
        logger.info(f"🎯 DISC завершен! Завершаем тестирование")
        return await complete_testing(update, context)
    
    question_data = DISC_QUESTIONS[session.current_question]
    
    # Создаем клавиатуру для шкалы 1-5
    keyboard = [
        ["1 - Совсем не согласен"],
        ["2 - Не согласен"],
        ["3 - Нейтрально"],
        ["4 - Согласен"],
        ["5 - Полностью согласен"],
        ["❌ Выйти"]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    logger.info(f"❓ Отправляем DISC вопрос {session.current_question + 1}/{len(DISC_QUESTIONS)}")
    
    # Удаляем устаревшую инструкцию для DISC
    await update.message.reply_text(
        f"💼 <b>DISC - Вопрос {session.current_question + 1}/{len(DISC_QUESTIONS)}</b>\n\n"
        f"{question_data['question']}",
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    return DISC_TESTING

async def handle_disc_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает ответ DISC (шкала 1-5)"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    answer_text = update.message.text
    
    # Проверяем на команду выхода
    if answer_text and ("❌" in answer_text or answer_text.lower() in ["/exit", "/cancel", "выйти", "отмена"]):
        return await cancel(update, context)
    
    # Добавляем подробное логирование
    logger.info(f"📝 DISC ответ от {user_id}: '{answer_text}'")
    logger.info(f"📊 Текущий вопрос: {session.current_question + 1}/{len(DISC_QUESTIONS)}")
    
    # Извлекаем число от 1 до 5 из ответа
    score = None
    if answer_text and len(answer_text) > 0:
        if answer_text[0].isdigit():
            score = int(answer_text[0])
    
    logger.info(f"� Балл: {score}")
    
    if score and 1 <= score <= 5:
        # Получаем данные текущего вопроса
        question_data = DISC_QUESTIONS[session.current_question]
        category = question_data['category']  # D, I, S, C
        
        # Обычная логика добавления баллов
        session.disc_scores[category] += score
        
        # НОВОЕ: сохраняем детальный ответ для раздела вопросов
        session.answers_collector.add_disc_answer(
            question_index=session.current_question,
            rating=score
        )
        
        session.current_question += 1
        
        logger.info(f"✅ Ответ принят. Категория: {category}, Балл: {score}")
        logger.info(f"✅ Новый current_question: {session.current_question}")
        logger.info(f"📈 Счет DISC: {session.disc_scores}")
        
        if session.current_question >= len(DISC_QUESTIONS):
            logger.info(f"🎯 DISC завершен! Переходим к HEXACO")
        
        return await ask_disc_question(update, context)
    else:
        logger.warning(f"❌ Неверный ответ DISC: '{answer_text}' -> балл: {score}")
        await update.message.reply_text("❗ Пожалуйста, выберите оценку от 1 до 5")
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
        "Выберите наиболее предпочтительный для вас ответ:",
        parse_mode='HTML'
    )
    logger.info(f"📝 Переходим к первому вопросу HEXACO")
    return await ask_hexaco_question(update, context)

async def ask_hexaco_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Задает вопрос HEXACO"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    
    if session.current_question >= len(HEXACO_QUESTIONS):
        return await start_disc_test(update, context)
    
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
    
    # Проверяем на выход
    if answer_text == "❌ Выйти":
        return await cancel(update, context)
    
    # Извлекаем числовой ответ (1-5)
    try:
        score = None
        for i in range(1, 6):  # Проверяем цифры 1-5
            if answer_text.startswith(str(i)):
                score = i
                break
                
        if score is not None:
            # Обычная логика сохранения
            session.hexaco_scores.append(score)
            
            # НОВОЕ: сохраняем детальный ответ для раздела вопросов
            session.answers_collector.add_hexaco_answer(
                question_index=session.current_question,
                rating=score
            )
            
            session.current_question += 1
            return await ask_hexaco_question(update, context)
        else:
            raise ValueError("Неверный формат ответа")
            
    except (ValueError, IndexError):
        await update.message.reply_text("❗ Пожалуйста, выберите один из предложенных вариантов (1-5)")
        return HEXACO_TESTING

async def start_soft_skills_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает тест Soft Skills"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    session.current_test = "SOFT_SKILLS"
    session.current_question = 0
    
    await update.message.reply_text(
        "💪 <b>Начинаем тест Soft Skills</b>\n\n"
        "Выберите наиболее предпочтительный для вас ответ:",
        parse_mode='HTML'
    )
    
    return await ask_soft_skills_question(update, context)

async def ask_soft_skills_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Задает вопрос Soft Skills"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    
    if session.current_question >= len(SOFT_SKILLS_QUESTIONS):
        return await start_hexaco_test(update, context)
    
    question_data = SOFT_SKILLS_QUESTIONS[session.current_question]
    
    # Создаем клавиатуру с вариантами ответов из файла или базовую шкалу 1-5
    keyboard = []
    if 'answers' in question_data and question_data['answers']:
        # Используем варианты ответов из файла
        for answer in question_data['answers']:
            keyboard.append([f"{answer['value']}. {answer['text']}"])
    else:
        # Используем базовую шкалу 1-5
        keyboard = [
            ["1", "2", "3", "4", "5"]
        ]
    
    # Добавляем кнопку выхода
    keyboard.append(["❌ Выйти"])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    skill_info = f" ({question_data['skill']})" if 'skill' in question_data else ""
    
    await update.message.reply_text(
        f"💪 <b>Soft Skills - Вопрос {session.current_question + 1}/{len(SOFT_SKILLS_QUESTIONS)}</b>{skill_info}\n\n"
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
    
    # Проверяем на выход
    if answer_text and ("❌" in answer_text or answer_text.lower() in ["/exit", "/cancel", "выйти", "отмена"]):
        return await cancel(update, context)
    
    # Извлекаем числовой ответ (1-5)
    try:
        score = None
        
        # Сначала проверяем ответы в формате "1. Текст ответа"
        if answer_text and answer_text[0].isdigit():
            score = int(answer_text[0])
        
        # Проверяем диапазон 1-5
        if score and 1 <= score <= 5:
            # Обычная логика сохранения
            session.soft_skills_scores.append(score)
            
            # НОВОЕ: сохраняем детальный ответ для раздела вопросов
            session.answers_collector.add_soft_skills_answer(
                question_index=session.current_question,
                rating=score
            )
            
            logger.info(f"📝 Soft Skills ответ от {user_id}: балл {score}")
            logger.info(f"📊 Текущий счет: {session.soft_skills_scores}")
            
            session.current_question += 1
            return await ask_soft_skills_question(update, context)
        else:
            raise ValueError("Неверный диапазон ответа")
            
    except (ValueError, IndexError):
        logger.warning(f"❌ Неверный ответ Soft Skills: '{answer_text}'")
        await update.message.reply_text("❗ Пожалуйста, выберите один из предложенных вариантов (1-5)")
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
        # Обработка результатов по методикам
        # PAEI: сохраняем оригинальные баллы согласно методике Адизеса
        # (1 балл за каждый выбранный ответ, сумма = количество вопросов)
        # session.paei_scores остается без изменений - это правильно!
        
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
        soft_skills_names = get_soft_skills_names()
        if len(session.soft_skills_scores) == len(soft_skills_names):
            soft_skills_dict = {}
            for i, skill_name in enumerate(soft_skills_names):
                soft_skills_dict[skill_name] = session.soft_skills_scores[i]  # Уже в шкале 1-10
            session.soft_skills_scores = soft_skills_dict
        else:
            # Если данных недостаточно, используем средние значения
            session.soft_skills_scores = {skill: 5.0 for skill in soft_skills_names}
        
        # Генерируем два PDF отчета в отдельном потоке
        pdf_path_user, pdf_path_gdrive = await asyncio.to_thread(generate_user_report, session)
        
        # Отправляем пользователю ТОЛЬКО его отчет (без детализации вопросов)
        with open(pdf_path_user, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename=f"Отчет_{session.name.replace(' ', '_')}.pdf",
                caption=f"📊 <b>Ваш персональный отчет готов!</b>\n\n"
                       f"👤 {session.name}\n"
                       f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                       f"📋 Отчет содержит детальный анализ по всем методикам.\n"
                       f"🔒 Полная версия с детализацией вопросов сохранена для специалиста.",
                parse_mode='HTML'
            )
        
        # Удаляем временные файлы безопасно
        import os
        for pdf_path in [pdf_path_user, pdf_path_gdrive]:
            if os.path.exists(pdf_path):
                try:
                    os.unlink(pdf_path)
                except Exception as del_err:
                    logger.warning(f"⚠️ Не удалось удалить временный PDF-файл {pdf_path}: {del_err}")
        # Отправляем уведомление о завершении
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

def generate_user_report(session: UserSession) -> tuple[str, str]:
    """Генерирует два PDF отчета: один для пользователя (без вопросов), другой для Google Drive (с вопросами)"""
    
    # Создаем временную папку для диаграмм
    temp_dir = tempfile.mkdtemp()
    temp_charts_dir = Path(temp_dir) / "charts"
    temp_charts_dir.mkdir(exist_ok=True)
    
    try:
        # Всегда собираем ответы пользователя для отчета в Google Drive
        user_answers = session.answers_collector.get_answers_dict()
        
        # Инициализируем генератор PDF БЕЗ раздела вопросов для пользователя
        pdf_generator_user = EnhancedPDFReportV2(
            template_dir=temp_charts_dir,
            include_questions_section=False  # Пользователю отчет без вопросов
        )
        
        # Инициализируем генератор PDF С разделом вопросов для Google Drive
        pdf_generator_gdrive = EnhancedPDFReportV2(
            template_dir=temp_charts_dir,
            include_questions_section=True   # В Google Drive отчет с вопросами
        )
    
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
                # Fallback на интерпретации согласно формату general_system_res.txt
                interpretations = generate_interpretations_from_prompt(
                    session.paei_scores, session.disc_scores, 
                    session.hexaco_scores, session.soft_skills_scores
                )
        else:
            # Используем базовые интерпретации в правильном формате согласно general_system_res.txt
            interpretations = generate_interpretations_from_prompt(
                session.paei_scores, session.disc_scores, 
                session.hexaco_scores, session.soft_skills_scores
            )
        
        # Создаем папки для сохранения PDF
        docs_dir = Path("docs")
        docs_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        base_filename = f"{timestamp}_{session.name.replace(' ', '_') if session.name else 'TelegramUser'}_tg_{str(session.user_id)[-4:]}"
        
        # Пути для двух отчетов
        pdf_path_user = docs_dir / f"{base_filename}_user.pdf"      # Для пользователя (без вопросов)
        pdf_path_gdrive = docs_dir / f"{base_filename}_full.pdf"    # Для Google Drive (с вопросами)
        
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
        
        test_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 1. Генерируем отчет БЕЗ вопросов для пользователя
        logger.info("📄 Генерируем отчет для пользователя (без детализации вопросов)...")
        pdf_generator_user.generate_enhanced_report(
            participant_name=session.name,
            test_date=test_date,
            paei_scores=paei_normalized,
            disc_scores=disc_normalized,
            hexaco_scores=hexaco_normalized,
            soft_skills_scores=soft_skills_normalized,
            ai_interpretations=interpretations,
            out_path=pdf_path_user,
            user_answers=None  # Не передаем ответы для пользовательского отчета
        )
        
        # 2. Генерируем отчет С вопросами для Google Drive
        logger.info("📄 Генерируем полный отчет для Google Drive (с детализацией вопросов)...")
        result = pdf_generator_gdrive.generate_enhanced_report_with_gdrive(
            participant_name=session.name,
            test_date=test_date,
            paei_scores=paei_normalized,
            disc_scores=disc_normalized,
            hexaco_scores=hexaco_normalized,
            soft_skills_scores=soft_skills_normalized,
            ai_interpretations=interpretations,
            out_path=pdf_path_gdrive,
            upload_to_gdrive=True,
            user_answers=user_answers  # 🔑 Передаем собранные ответы для полного отчета
        )
        
        # Проверяем результат Google Drive загрузки
        if result and len(result) == 2:
            local_path, gdrive_link = result
            logger.info(f"📁 Пользовательский отчет: {pdf_path_user.name}")
            logger.info(f"📁 Полный отчет сохранен: {pdf_path_gdrive.name}")
            if gdrive_link:
                logger.info(f"☁️ Google Drive: {gdrive_link}")
            else:
                logger.info("⚠️ Google Drive загрузка не удалась")
        else:
            logger.info(f"📁 Пользовательский отчет: {pdf_path_user.name}")
            logger.info(f"📁 Полный отчет сохранен: {pdf_path_gdrive.name}")
            logger.warning("⚠️ Проблема с Google Drive интеграцией")
        
        # Возвращаем пути к обоим отчетам
        return str(pdf_path_user), str(pdf_path_gdrive)
            
    except Exception as e:
        logger.error(f"Ошибка генерации отчета: {e}")
        raise e
    finally:
        # Очищаем временную папку
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.debug(f"Временная папка {temp_dir} удалена")
        except Exception as e:
            logger.warning(f"Не удалось удалить временную папку {temp_dir}: {e}")

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