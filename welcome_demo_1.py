import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Устанавливаем уровень логов
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Инициализируем бота
updater = Updater(token='YOUR_TELEGRAM_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

# Функция, которая будет вызываться при команде /start
def start(update, context):
    # Отправляем приветственное сообщение
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я твой телеграм-бот!")

    # Создаем главное меню с 4 кнопками
    keyboard = [['Кнопка 1', 'Кнопка 2'], ['Кнопка 3', 'Кнопка 4']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Выбери одну из кнопок:", reply_markup=reply_markup)

# Функция, которая будет вызываться при получении сообщений от пользователя
def echo(update, context):
    # Отправляем ответное сообщение
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ты нажал кнопку: " + update.message.text)

# Регистрируем обработчики команд и сообщений
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

# Запускаем бота
updater.start_polling()

# Функция для рассылки сообщений
def send_message_to_all_users(text):
    # Получаем список всех пользователей
    all_users = updater.bot.getUpdates()

    # Отправляем сообщение каждому пользователю
    for user in all_users:
        updater.bot.send_message(chat_id=user.message.chat.id, text=text)

# Пример использования функции рассылки
send_message_to_all_users("Привет! Это рассылка!")

# Запускаем бесконечный цикл, чтобы бот работал
updater.idle()
