import telebot
import sqlite3
from google.oauth2 import service_account
import gspread
from airtable import Airtable

# Здесь ты можешь настроить свои административные данные
admin_panel_credentials = 'admin_panel_credentials.json'
telegram_token = 'токен_телеграм_бота'
chat_id = 'идентификатор_группы_TG'
google_credentials = 'google_credentials.json'
airtable_api_key = 'API_ключ_Airtable'
airtable_base_key = 'идентификатор_базы_Airtable'

# Подключение к Google Таблицам
google_credentials = service_account.Credentials.from_service_account_file(google_credentials)
google_client = gspread.authorize(google_credentials)
google_sheet = google_client.open('Название_гугл_таблицы').sheet1

# Подключение к базе данных SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Подключение к Airtable
airtable = Airtable('название_таблицы', 'название_таблицы', api_key=airtable_api_key)

# Создаем экземпляр телеграм-бота
bot = telebot.TeleBot(token=telegram_token)

# Метод для проверки наличия дубликатов сообщений в базе данных
def check_duplicate_message(msg):
    query = "SELECT * FROM messages WHERE message_id = ?"
    result = cursor.execute(query, (msg.message_id,))
    return result.fetchone() is not None

# Метод для сохранения сообщения в базе данных
def save_message(msg):
    query = "INSERT INTO messages (message_id, chat_id, text) VALUES (?, ?, ?)"
    cursor.execute(query, (msg.message_id, msg.chat.id, msg.text))
    conn.commit()

# Метод для пересылки сообщений
def forward_message(msg):
    bot.forward_message(chat_id, msg.chat.id, msg.message_id)

    # Дополнительные действия:
    # Пересылка в гугл таблицу
    google_sheet.append_row([msg.text, msg.chat.id])

    # Пересылка в базу данных Airtable
    airtable.insert({'text': msg.text, 'chat_id': msg.chat.id})

@bot.message_handler(func=lambda msg: True)
def handle_message(msg):
    if not check_duplicate_message(msg):
        # Проверка на наличие ключевых слов
        keywords = ['ключевое_слово_1', 'ключевое_слово_2']
        minus_keywords = ['минус_слово_1', 'минус_слово_2']

        if any(keyword in msg.text for keyword in keywords) and not any(minus_keyword in msg.text for minus_keyword in minus_keywords):
            forward_message(msg)
            save_message(msg)

bot.polling(none_stop=True)
