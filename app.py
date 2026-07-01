import os
import logging
import asyncio

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import google.generativeai as genai

# ---------------- НАСТРОЙКА ----------------

TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- ПРОМПТ ----------------

SYSTEM_PROMPT = """
Ты NOVA HOME AI.

Ты лучший школьный помощник.

Правила:

1. Решай домашние задания.
2. Объясняй решение максимально просто.
3. Не пиши сложными словами.
4. Если пользователь просит только ответ —
сначала дай решение, потом ответ.

Структура ответа:

📚 Решение

...

✅ Ответ

...

Если задача непонятна —
попроси отправить более качественную фотографию.
"""

# ---------------- КОМАНДА START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👋 Привет!\n\n"
        "Я NOVA HOME AI.\n\n"
        "📸 Отправь фотографию домашнего задания\n"
        "или просто напиши вопрос.\n\n"
        "Я объясню решение шаг за шагом."
    )

    await update.message.reply_text(text)

# ---------------- ОБРАБОТКА ТЕКСТА ----------------

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    await update.message.chat.send_action(ChatAction.TYPING)

    try:

        response = model.generate_content(
            SYSTEM_PROMPT + "\n\n" + user_text
        )

        await update.message.reply_text(
            response.text
        )

    except Exception:

        await update.message.reply_text(
            "❌ Произошла ошибка. Попробуй ещё раз."
        )

# ---------------- ЗАПУСК ----------------

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text,
        )
    )

    print("Бот запущен!")

    app.run_polling()

if __name__ == "__main__":
    main()
