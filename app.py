import logging

from telegram.ext import Application

from config import BOT_TOKEN
from handlers import register_handlers

# ====== ЛОГИ ======

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# ====== ЗАПУСК БОТА ======

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")

    app = Application.builder().token(BOT_TOKEN).build()

    # подключаем все обработчики
    register_handlers(app)

    print("🤖 NOVA HOME AI запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()
