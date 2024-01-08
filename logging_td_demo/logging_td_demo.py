import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client['your_database_name']

@app.route('/admin')
def admin_panel():
    # Здесь можно выполнить логику для отображения и управления данными
    return 'Admin Panel'

@app.route('/analytics')
def analytics():
    return analyze_messages()


def save_message(message):
    collection = db['messages']
    collection.insert_one({'text': message.text, 'chat_id': message.chat_id})

def analyze_messages():
    collection = db['messages']
    # Здесь можно выполнить логику анализа сообщений
    total_messages = collection.count_documents({})
    return f'Total messages: {total_messages}'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Привет, {user.first_name}!")
    save_message(update.message)

def echo(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    save_message(update.message)

def main() -> None:
    # Получение токена бота
    token = 'YOUR_BOT_TOKEN'  # Замени на свой токен

    # Создание экземпляра Updater и передача токена
    updater = Updater(token)

    # Получение диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))

    # Регистрация обработчика текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Добавление маршрутов Flask
    updater.bot.wsgi_app = app

    # Запуск бота и Flask
    updater.start_polling()
    app.run()

    # Остановка бота при нажатии Ctrl-C
    updater.idle()

    # ... остальной код ...


if __name__ == '__main__':
    main()
