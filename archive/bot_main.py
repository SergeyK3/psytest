import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# состояния диалога
WAITING_CONFIRMATION, WAITING_NAME = range(2)

# переменная для хранения имени
user_data_store = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Здравствуйте, я бот по тестированию командных навыков. "
        "Я буду задавать вам вопросы с вариантами ответов. "
        "Вам нужно выбрать наиболее приемлемый для вас вариант ответа. Готовы?"
    )
    return WAITING_CONFIRMATION

# обработка ответа "да"
async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.lower().strip()
    if text == "да":
        await update.message.reply_text("Пожалуйста, назовите свою фамилию и имя")
        return WAITING_NAME
    else:
        await update.message.reply_text("Хорошо, напишите 'да', когда будете готовы.")
        return WAITING_CONFIRMATION

# обработка фамилии и имени
async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    full_name = update.message.text.strip()
    user_data_store[user_id] = {"full_name": full_name}

    await update.message.reply_text(f"Спасибо, {full_name}! Ваши данные сохранены.")
    # тут можно переходить к тестированию
    return ConversationHandler.END

# отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Диалог прерван. Напишите /start, чтобы начать заново.")
    return ConversationHandler.END

def main():
    app = Application.builder().token("8250482375:AAH3ZCQ3s6XJyl5g32sY63g5HKOHnqGq1WQ").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmation)],
            WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
