import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Инициализация логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот для мониторинга упоминаний.")

# Обработчик входящих сообщений
def message_handler(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    # Проверка на упоминание
    if "упоминание" in text:
        context.bot.send_message(chat_id=chat_id, text="Обнаружено упоминание!")

# Функция запуска бота
def run_bot(token):
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Регистрация обработчика входящих сообщений
    message_handler = MessageHandler(Filters.text, message_handler)
    dispatcher.add_handler(message_handler)

    # Запуск бота
    updater.start_polling()

    # Ждем остановку бота (например, нажатием Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    # Вставь свой токен бота
    token = 'YOUR_BOT_TOKEN'
    run_bot(token)
