
import logging
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from llm_setup import load_llm
from pdf_loader import load_data_and_index
from llama_index.core import Settings
import os

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
TELEGRAM_BOT_TOKEN = "6358530150:AAE919TQOeBLw39Jw6N23qcqDDvH2vvuGZk"
PDF_PATH = "C:\\Users\\NeliOdei\\Documents\\Alt\\data\\abc.pdf"

# Глобальная переменная для query_engine
query_engine = None

# Обработчики команд Telegram
async def start(update, context):
    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Привет! Я AI-агент основанный на Llama Index, обученный на PDF. Спроси меня что-нибудь!"
        )
        logger.info(f"Start command received from {update.effective_chat.id}")
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Произошла ошибка при обработке команды /start"
        )

async def handle_message(update, context):
    if query_engine is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Система еще не готова. Пожалуйста, подождите..."
        )
        return

    query = update.message.text
    try:
        logger.info(f"Processing query: {query}")
        response = query_engine.query(query)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=str(response)
        )
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Произошла ошибка при обработке запроса: {e}"
        )

async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "Запустить бота"),
    ])

# Основная функция
def main():
    global query_engine

    try:
        logger.info("Starting bot initialization...")

        # Загрузка LLM
        logger.info("Loading LLM...")
        llm = load_llm()
        Settings.llm = llm

        # Загрузка и индексация PDF
        logger.info(f"Loading PDF from {PDF_PATH}...")
        index = load_data_and_index(PDF_PATH)
        query_engine = index.as_query_engine()
        logger.info("PDF loaded and indexed successfully")

        # Создание и настройка приложения Telegram
        application = ApplicationBuilder() \
            .token(TELEGRAM_BOT_TOKEN) \
            .post_init(post_init) \
            .build()

        # Регистрация обработчиков
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

        logger.info("Bot is ready and starting to poll...")
        application.run_polling()

    except Exception as e:
        logger.critical(f"Failed to start bot: {e}", exc_info=True)

if __name__ == '__main__':
    main()