import os
import logging
from dotenv import load_dotenv
import telebot
import openai

# Загрузка переменных окружения из .env (файл должен содержать только строки вида KEY=value)
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SYSTEM_PROMPT = os.getenv("AGENT_SYSTEM_PROMPT")

if not (TELEGRAM_TOKEN and OPENAI_API_KEY and SYSTEM_PROMPT):
    raise RuntimeError("В .env должны быть определены TELEGRAM_TOKEN, OPENAI_API_KEY и AGENT_SYSTEM_PROMPT")

# Логирование
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация OpenAI и Telegram бота
openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Хранилище истории диалогов
contexts = {}

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот-копирайтер по мебели на заказ. Напиши тему (кухни, шкафы и т.д.) — и я создам текст."
    )

@bot.message_handler(commands=["clear"])
def handle_clear(message):
    contexts.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Контекст очищен!")

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_message(message):
    chat_id = message.chat.id
    user_text = message.text

    if chat_id not in contexts:
        contexts[chat_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    contexts[chat_id].append({"role": "user", "content": user_text})

    try:
        # Используем новый интерфейс openai-python>=1.0
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=contexts[chat_id],
            temperature=0.3,
            max_tokens=1000
        )
        reply = response.choices[0].message.content

        contexts[chat_id].append({"role": "assistant", "content": reply})
        bot.send_message(chat_id, reply)

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        bot.send_message(chat_id, "Произошла ошибка при обращении к OpenAI API.")

if __name__ == '__main__':
    logger.info("Запуск Telegram бота...")
    bot.infinity_polling()
