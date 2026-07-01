from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from ai import get_ai_response

# ====== ПАМЯТЬ ДИАЛОГА (простая) ======

user_history = {}

def get_history(user_id: int):
    return user_history.get(user_id, [])

def add_to_history(user_id: int, role: str, text: str):
    if user_id not in user_history:
        user_history[user_id] = []

    user_history[user_id].append(f"{role}: {text}")

# ====== /START ======

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я NOVA HOME AI\n\n"
        "📚 Я помогу тебе с домашними заданиями\n"
        "✍️ Просто напиши задачу или отправь фото"
    )

# ====== /HELP ======

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Команды:\n"
        "/start - запуск\n"
        "/help - помощь\n\n"
        "💬 Просто отправь задачу текстом или фото"
    )

# ====== ОБРАБОТКА ТЕКСТА ======

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text

    await update.message.chat.send_action(ChatAction.TYPING)

    history = get_history(user_id)
    add_to_history(user_id, "user", user_text)

    response = get_ai_response(user_text, history)

    add_to_history(user_id, "bot", response)

    await update.message.reply_text(response)

# ====== ОБРАБОТКА ФОТО (заглушка пока) ======

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Фото получено!\n\n"
        "Скоро добавим распознавание задач из изображения."
    )

# ====== РЕГИСТРАЦИЯ ХЕНДЛЕРОВ ======

def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
