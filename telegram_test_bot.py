import matplotlib
matplotlib.use('Agg')
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
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

# Загружаем переменные окружения
load_dotenv()

# Импорты наших модулей
from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from interpretation_utils import generate_interpretations_from_prompt
from src.psytest.ai_interpreter import get_ai_interpreter
from report_archiver import save_report_copy
from scale_normalizer import ScaleNormalizer

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
        
        # Простое хранение ответов для раздела с вопросами
        self.user_answers = {
            'paei': {},
            'disc': {},
            'hexaco': {},
            'soft_skills': {}
        }

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

def convert_disc_to_average(session):
    """Конвертирует DISC баллы из суммы в среднее значение (1-5)"""
    try:
        # Подсчитываем количество вопросов по каждой категории
        category_count = {"D": 0, "I": 0, "S": 0, "C": 0}
        
        for question in DISC_QUESTIONS:
            if 'category' in question:
                category = question['category']
                if category in category_count:
                    category_count[category] += 1
        
        # Конвертируем сумму в среднее значение
        for category in ["D", "I", "S", "C"]:
            if category_count[category] > 0:
                # Среднее = сумма / количество вопросов
                average = session.disc_scores[category] / category_count[category]
                session.disc_scores[category] = round(average, 1)
                logger.info(f"📊 {category}: {category_count[category]} вопросов → среднее {average:.1f}")
            else:
                logger.warning(f"⚠️ Нет вопросов для категории {category}")
        
        logger.info(f"✅ DISC конвертирован в среднее: {session.disc_scores}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка конвертации DISC: {e}")

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
        7: "Восприимчивость к критике",
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
                "Решение проблем", "Адаптивность", "Управление временем", "Восприимчивость к критике",
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
    
    keyboard = [
        [InlineKeyboardButton("✅ Да, начать тестирование", callback_data="start_yes")],
        [InlineKeyboardButton("❌ Нет, не сейчас", callback_data="start_no")],
        [InlineKeyboardButton("❌ Отменить текущую операцию", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text, 
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    
    return WAITING_START

async def handle_start_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка подтверждения начала через inline кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "start_yes":
        await query.edit_message_text(
            "📝 Отлично! Давайте начнем с регистрации.\n\n"
            "Пожалуйста, введите ваши <b>Фамилию и Имя</b>:",
            parse_mode='HTML'
        )
        return WAITING_NAME
    else:
        await query.edit_message_text(
            "Хорошо! Когда будете готовы, напишите /start"
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
        parse_mode='HTML'
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
    
    # Формируем inline клавиатуру с вариантами ответов (текст на кнопках)
    keyboard = []
    for key in ["P", "A", "E", "I"]:
        if key in question_data["answers"]:
            btn_text = f"{key}. {question_data['answers'][key]}"
            keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"paei_{key}")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Формируем текст вопроса
    question_text = f"📊 <b>PAEI - Вопрос {session.current_question + 1}/{len(PAEI_QUESTIONS)}</b>\n\n"
    question_text += f"<b>{question_data['question']}</b>"
    
    # Определяем откуда пришел запрос
    if hasattr(update, 'message') and update.message:
        # Обычное сообщение
        await update.message.reply_text(
            question_text,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    else:
        # Callback query или другой тип обновления
        await context.bot.send_message(
            chat_id=user_id,
            text=question_text,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    
    return PAEI_TESTING

async def handle_paei_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает ответ PAEI через inline кнопки"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    session = user_sessions[user_id]

    # Извлекаем код ответа из callback_data (например, "paei_P" -> "P")
    if query.data.startswith("paei_"):
        answer_code = query.data.split("_")[1]

        if answer_code in ["P", "A", "E", "I"]:
            # Обычная логика подсчета баллов
            session.paei_scores[answer_code] += 1

            # Сохраняем ответ для раздела с вопросами
            session.user_answers['paei'][str(session.current_question)] = answer_code

            # Получаем текст вопроса и ответа
            q_idx = session.current_question
            if q_idx < len(PAEI_QUESTIONS):
                question_data = PAEI_QUESTIONS[q_idx]
                answer_text = question_data["answers"].get(answer_code, answer_code)
                msg = f"Вы выбрали: {answer_code}. {answer_text}"
                await query.message.reply_text(msg, parse_mode='HTML')

            session.current_question += 1

            # Удаляем кнопки у предыдущего сообщения
            await query.edit_message_reply_markup(reply_markup=None)

            return await ask_paei_question(update, context)

    await query.edit_message_text("❗ Пожалуйста, выберите один из предложенных вариантов")
    return PAEI_TESTING

async def start_disc_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает тест DISC"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    session.current_test = "DISC"
    session.current_question = 0
    
    # Определяем откуда пришел запрос и отправляем сообщение
    if hasattr(update, 'message') and update.message:
        # Обычное сообщение
        await update.message.reply_text(
            f"✅ <b>PAEI завершен!</b>\n\n"
            f"🎭 Переходим к тесту DISC (поведенческие стили)\n"
            f"Вопрос 1 из {len(DISC_QUESTIONS)}:",
            parse_mode='HTML'
        )
    else:
        # Callback query или другой тип обновления
        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ <b>PAEI завершен!</b>\n\n"
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
        logger.info(f"🎯 DISC завершен! Конвертируем баллы в среднее значение")
        
        # Конвертируем DISC баллы из суммы в среднее значение (1-5)
        convert_disc_to_average(session)
        
        logger.info(f"🎯 DISC завершен! Завершаем тестирование")
        return await complete_testing(update, context)
    
    question_data = DISC_QUESTIONS[session.current_question]
    
    # Создаем inline клавиатуру для шкалы 1-5
    keyboard = [
        [InlineKeyboardButton("1 - Совсем не согласен", callback_data="disc_1")],
        [InlineKeyboardButton("2 - Не согласен", callback_data="disc_2")],
        [InlineKeyboardButton("3 - Нейтрально", callback_data="disc_3")],
        [InlineKeyboardButton("4 - Согласен", callback_data="disc_4")],
        [InlineKeyboardButton("5 - Полностью согласен", callback_data="disc_5")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    logger.info(f"❓ Отправляем DISC вопрос {session.current_question + 1}/{len(DISC_QUESTIONS)}")
    
    question_text = f"💼 <b>DISC - Вопрос {session.current_question + 1}/{len(DISC_QUESTIONS)}</b>\n\n{question_data['question']}"
    if hasattr(update, 'message') and update.message:
        await update.message.reply_text(
            question_text,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text=question_text,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    return DISC_TESTING

async def handle_disc_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает ответ DISC через inline кнопки"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    session = user_sessions[user_id]

    # Извлекаем балл из callback_data (например, "disc_3" -> 3)
    if query.data.startswith("disc_"):
        try:
            score = int(query.data.split("_")[1])

            if 1 <= score <= 5:
                # Получаем данные текущего вопроса
                question_data = DISC_QUESTIONS[session.current_question]
                category = question_data['category']  # D, I, S, C

                # Обычная логика добавления баллов
                session.disc_scores[category] += score

                # Сохраняем ответ для раздела с вопросами
                session.user_answers['disc'][str(session.current_question)] = score

                # Получаем текст вопроса и ответа
                q_idx = session.current_question
                if q_idx < len(DISC_QUESTIONS):
                    scale_texts = [
                        "1 - Совсем не согласен",
                        "2 - Не согласен",
                        "3 - Нейтрально",
                        "4 - Согласен",
                        "5 - Полностью согласен"
                    ]
                    answer_text = scale_texts[score-1] if 1 <= score <= 5 else str(score)
                    msg = f"Вы выбрали: {answer_text}"
                    await query.message.reply_text(msg, parse_mode='HTML')

                session.current_question += 1

                logger.info(f"✅ DISC ответ принят. Категория: {category}, Балл: {score}")
                logger.info(f"📈 Счет DISC: {session.disc_scores}")

                # Удаляем кнопки у предыдущего сообщения
                await query.edit_message_reply_markup(reply_markup=None)

                return await ask_disc_question(update, context)
        except (ValueError, IndexError):
            pass

    await query.edit_message_text("❗ Пожалуйста, выберите оценку от 1 до 5")
    return DISC_TESTING

async def start_hexaco_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает тест HEXACO"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    
    logger.info(f"🧠 Начинаем HEXACO тест для пользователя {user_id}")
    logger.info(f"📊 Финальные результаты DISC: {session.disc_scores}")
    
    session.current_test = "HEXACO"
    session.current_question = 0
    
    # Определяем откуда пришел запрос и отправляем сообщение
    if hasattr(update, 'message') and update.message:
        # Обычное сообщение
        await update.message.reply_text(
            "🧠 <b>Начинаем тест HEXACO</b>\n\n"
            "Выберите наиболее предпочтительный для вас ответ:",
            parse_mode='HTML'
        )
    else:
        # Callback query или другой тип обновления
        await context.bot.send_message(
            chat_id=user_id,
            text="🧠 <b>Начинаем тест HEXACO</b>\n\n"
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
    
    # Формируем inline клавиатуру с вариантами ответов (текст на кнопках)
    scale_texts = [
        "1 - Абсолютно не согласен",
        "2 - Не согласен",
        "3 - Нейтрально",
        "4 - Согласен",
        "5 - Полностью согласен"
    ]
    keyboard = []
    for i, text in enumerate(scale_texts, 1):
        keyboard.append([InlineKeyboardButton(text, callback_data=f"hexaco_{i}")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Формируем текст вопроса
    question_text = f"🧠 <b>HEXACO - Вопрос {session.current_question + 1}/{len(HEXACO_QUESTIONS)}</b>\n\n{question_data['question']}"

    # Определяем откуда пришел запрос
    if hasattr(update, 'message') and update.message:
        await update.message.reply_text(
            question_text,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text=question_text,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    return HEXACO_TESTING

async def handle_hexaco_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает ответ HEXACO через inline кнопки"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    session = user_sessions[user_id]

    # Извлекаем балл из callback_data (например, "hexaco_3" -> 3)
    if query.data.startswith("hexaco_"):
        try:
            score = int(query.data.split("_")[1])

            if 1 <= score <= 5:
                # Обычная логика сохранения
                session.hexaco_scores.append(score)

                # Сохраняем ответ для раздела с вопросами
                session.user_answers['hexaco'][str(session.current_question)] = score

                # Получаем текст вопроса и ответа
                q_idx = session.current_question
                if q_idx < len(HEXACO_QUESTIONS):
                    scale_texts = [
                        "1 - Абсолютно не согласен",
                        "2 - Не согласен",
                        "3 - Нейтрально",
                        "4 - Согласен",
                        "5 - Полностью согласен"
                    ]
                    answer_text = scale_texts[score-1] if 1 <= score <= 5 else str(score)
                    msg = f"Вы выбрали: {answer_text}"
                    await query.message.reply_text(msg, parse_mode='HTML')

                session.current_question += 1

                # Удаляем кнопки у предыдущего сообщения
                await query.edit_message_reply_markup(reply_markup=None)

                return await ask_hexaco_question(update, context)
        except (ValueError, IndexError):
            pass

    await query.edit_message_text("❗ Пожалуйста, выберите один из предложенных вариантов (1-5)")
    return HEXACO_TESTING

async def start_soft_skills_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает тест Soft Skills"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    session.current_test = "SOFT_SKILLS"
    session.current_question = 0
    
    # Определяем откуда пришел запрос и отправляем сообщение
    if hasattr(update, 'message') and update.message:
        # Обычное сообщение
        await update.message.reply_text(
            "💪 <b>Начинаем тест Soft Skills</b>\n\n"
            "Выберите наиболее предпочтительный для вас ответ:",
            parse_mode='HTML'
        )
    else:
        # Callback query или другой тип обновления
        await context.bot.send_message(
            chat_id=user_id,
            text="💪 <b>Начинаем тест Soft Skills</b>\n\n"
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
    
    # Формируем inline клавиатуру с вариантами ответов (текст на кнопках)
    keyboard = []
    if 'answers' in question_data and question_data['answers']:
        for answer in question_data['answers']:
            btn_text = f"{answer['value']}. {answer['text']}"
            keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"soft_{answer['value']}" )])
    else:
        scale_texts = [
            "1 - Совсем не согласен",
            "2 - Не согласен",
            "3 - Нейтрально",
            "4 - Согласен",
            "5 - Полностью согласен"
        ]
        for i, text in enumerate(scale_texts, 1):
            keyboard.append([InlineKeyboardButton(text, callback_data=f"soft_{i}")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    skill_info = f" ({question_data['skill']})" if 'skill' in question_data else ""
    question_text = f"💪 <b>Soft Skills - Вопрос {session.current_question + 1}/{len(SOFT_SKILLS_QUESTIONS)}</b>{skill_info}\n\n"
    question_text += f"<b>{question_data['question']}</b>"

    # Определяем откуда пришел запрос
    if hasattr(update, 'message') and update.message:
        await update.message.reply_text(
            question_text,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text=question_text,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    return SOFT_SKILLS_TESTING

async def handle_soft_skills_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает ответ Soft Skills через inline кнопки"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    session = user_sessions[user_id]

    # Извлекаем балл из callback_data (например, "soft_3" -> 3)
    if query.data.startswith("soft_"):
        try:
            score = int(query.data.split("_")[1])

            if 1 <= score <= 5:
                # Обычная логика сохранения
                session.soft_skills_scores.append(score)

                # Сохраняем ответ для раздела с вопросами
                session.user_answers['soft_skills'][str(session.current_question)] = score

                # Получаем текст вопроса и ответа
                q_idx = session.current_question
                if q_idx < len(SOFT_SKILLS_QUESTIONS):
                    question_data = SOFT_SKILLS_QUESTIONS[q_idx]
                    answer_text = None
                    if 'answers' in question_data and question_data['answers']:
                        for ans in question_data['answers']:
                            if ans['value'] == score:
                                answer_text = f"{ans['value']}. {ans['text']}"
                                break
                    if not answer_text:
                        scale_texts = [
                            "1 - Совсем не согласен",
                            "2 - Не согласен",
                            "3 - Нейтрально",
                            "4 - Согласен",
                            "5 - Полностью согласен"
                        ]
                        if 1 <= score <= 5:
                            answer_text = scale_texts[score-1]
                        else:
                            answer_text = str(score)
                    msg = f"Вы выбрали: {answer_text}"
                    await query.message.reply_text(msg, parse_mode='HTML')

                logger.info(f"📝 Soft Skills ответ от {user_id}: балл {score}")
                logger.info(f"📊 Текущий счет: {session.soft_skills_scores}")

                session.current_question += 1

                # Удаляем кнопки у предыдущего сообщения
                await query.edit_message_reply_markup(reply_markup=None)

                return await ask_soft_skills_question(update, context)
        except (ValueError, IndexError):
            pass

    await query.edit_message_text("❗ Пожалуйста, выберите один из предложенных вариантов (1-5)")
    return SOFT_SKILLS_TESTING

async def complete_testing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершает тестирование и генерирует отчет"""
    user_id = update.effective_user.id
    session = user_sessions[user_id]
    
    # Определяем откуда пришел запрос и отправляем сообщение
    if hasattr(update, 'message') and update.message:
        # Обычное сообщение
        await update.message.reply_text(
            "🎉 <b>Тестирование завершено!</b>\n\n"
            "⏳ Генерируем ваш персональный отчет...\n"
            "Это займет несколько минут.",
            parse_mode='HTML'
        )
    else:
        # Callback query или другой тип обновления
        await context.bot.send_message(
            chat_id=user_id,
            text="🎉 <b>Тестирование завершено!</b>\n\n"
                 "⏳ Генерируем ваш персональный отчет...\n"
                 "Это займет несколько минут.",
            parse_mode='HTML'
        )
    
    try:
        # Обработка результатов по методикам
        # PAEI: сохраняем оригинальные баллы согласно методике Адизеса
        # (1 балл за каждый выбранный ответ, сумма = количество вопросов)
        # session.paei_scores остается без изменений - это правильно!
        
        # DISC: оставляем сырые баллы (8 вопросов × шкала 1-5 = 8-40 баллов)
        # Убираем нормализацию - пусть ScaleNormalizer обработает сырые данные
        # session.disc_scores остается без изменений - это правильно!
        
        # HEXACO: преобразуем список ответов в средние баллы по измерениям
        # У нас 6 вопросов (по одному на каждое измерение HEXACO)
        hexaco_dimensions = ["H", "E", "X", "A", "C", "O"]
        if len(session.hexaco_scores) == 6:
            hexaco_dict = {}
            for i, dimension in enumerate(hexaco_dimensions):
                score = session.hexaco_scores[i]  # Оценка 1-5
                # Оставляем оригинальную шкалу 1-5 (без нормализации к 10 баллам)
                hexaco_dict[dimension] = round(score, 1)
            session.hexaco_scores = hexaco_dict
        else:
            # Если данных недостаточно, используем средние значения
            session.hexaco_scores = {dim: 3.0 for dim in hexaco_dimensions}  # Среднее для шкалы 1-5
        
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
        logger.info("🔄 Начинаем генерацию отчетов...")
        pdf_path_user, pdf_path_gdrive = await asyncio.to_thread(generate_user_report, session)
        logger.info(f"✅ Отчеты готовы: {pdf_path_user}, {pdf_path_gdrive}")
        
        # Отправляем пользователю ТОЛЬКО его отчет (без детализации вопросов)
        logger.info("📤 Отправляем отчет пользователю...")
        with open(pdf_path_user, 'rb') as pdf_file:
            # Определяем способ отправки документа
            if hasattr(update, 'message') and update.message:
                # Обычное сообщение
                await update.message.reply_document(
                    document=pdf_file,
                    filename=f"Отчет_{session.name.replace(' ', '_')}.pdf",
                    caption=f"📊 <b>Ваш персональный отчет готов!</b>\n\n"
                           f"👤 {session.name}\n"
                           f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                    parse_mode='HTML'
                )
            else:
                # Callback query или другой тип обновления
                await context.bot.send_document(
                    chat_id=user_id,
                    document=pdf_file,
                    filename=f"Отчет_{session.name.replace(' ', '_')}.pdf",
                    caption=f"📊 <b>Ваш персональный отчет готов!</b>\n\n"
                           f"👤 {session.name}\n"
                           f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                    parse_mode='HTML'
                )
        logger.info("✅ Отчет успешно отправлен пользователю!")
        
        # Удаляем временные файлы безопасно
        import os
        for pdf_path in [pdf_path_user, pdf_path_gdrive]:
            if os.path.exists(pdf_path):
                try:
                    os.unlink(pdf_path)
                except Exception as del_err:
                    logger.warning(f"⚠️ Не удалось удалить временный PDF-файл {pdf_path}: {del_err}")
        # Отправляем благодарность
        if hasattr(update, 'message') and update.message:
            # Обычное сообщение
            await update.message.reply_text(
                "Спасибо за прохождение тестирования! 🎯",
                parse_mode='HTML'
            )
        else:
            # Callback query или другой тип обновления
            await context.bot.send_message(
                chat_id=user_id,
                text="Спасибо за прохождение тестирования! 🎯",
                parse_mode='HTML'
            )
    except Exception as e:
        logger.error(f"Ошибка генерации отчета: {e}")
        import traceback
        logger.error(f"Подробная ошибка: {traceback.format_exc()}")
        
        # Отправляем сообщение об ошибке
        if hasattr(update, 'message') and update.message:
            # Обычное сообщение
            await update.message.reply_text(
                "❌ Произошла ошибка при генерации отчета.\n"
                "Попробуйте еще раз или обратитесь в поддержку."
            )
        else:
            # Callback query или другой тип обновления
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Произошла ошибка при генерации отчета.\n"
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
        # Восстанавливаем рабочий код для раздела с вопросами
        user_answers = session.user_answers
        
        # 🔍 ОТЛАДКА: Логируем собранные ответы
        logger.info(f"🔍 Собранные ответы пользователя:")
        for test_type, answers in user_answers.items():
            logger.info(f"  {test_type.upper()}: {len(answers)} ответов - {dict(list(answers.items())[:3]) if answers else 'пусто'}{'...' if len(answers) > 3 else ''}")
        
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
                
                # ✨ НОВОЕ: Генерируем общее заключение с рекомендациями по команде
                all_scores = {
                    'paei': session.paei_scores,
                    'disc': session.disc_scores,
                    'hexaco': session.hexaco_scores,
                    'soft_skills': session.soft_skills_scores
                }
                interpretations["general"] = ai_interpreter.interpret_general_conclusion(all_scores)
                
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
        user_name_part = session.name.replace(' ', '_') if session.name else 'TelegramUser'
        
        # Пути для двух отчетов
        pdf_path_user = docs_dir / f"{timestamp}_{user_name_part}.pdf"                           # Для пользователя (чистое имя)
        pdf_path_gdrive = docs_dir / f"{timestamp}_{user_name_part}_(tg_{session.user_id})_full.pdf"    # Для Google Drive (с ID)
        
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
        "Чтобы начать заново, напишите /start"
    )
    
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Помощь"""
    help_text = """🤖 <b>Бот для оценки командных навыков</b>

<b>Команды:</b>
/start - Начать тестирование
/cancel - Отменить текущее тестирование  
/help - Показать эту справку

<b>О тестировании:</b>
• Время прохождения: ~10 минут
• Методики: PAEI, DISC, HEXACO, Soft Skills
• Результат: Персональный PDF отчет

<b>Поддержка:</b> @kimsergeiv"""
    
    await update.message.reply_text(help_text, parse_mode='HTML')

def main():
    """Основная функция запуска бота"""
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Создаем ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_START: [CallbackQueryHandler(handle_start_confirmation)],
            WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
            PAEI_TESTING: [CallbackQueryHandler(handle_paei_answer)],
            DISC_TESTING: [CallbackQueryHandler(handle_disc_answer)],
            HEXACO_TESTING: [CallbackQueryHandler(handle_hexaco_answer)],
            SOFT_SKILLS_TESTING: [CallbackQueryHandler(handle_soft_skills_answer)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("help", help_command)
        ],
    )
    
    # Добавляем обработчики команд ПЕРЕД conversation handler
    application.add_handler(CommandHandler("help", help_command))
    
    # Добавляем conversation handler
    application.add_handler(conv_handler)
    
    # Запускаем бота
    logger.info("🤖 Бот запущен и готов к работе!")
    logger.info("📱 Telegram: @psytestDev2bot")
    print("🚀 Бот запущен! Можно тестировать в Telegram: @psytestDev2bot")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()