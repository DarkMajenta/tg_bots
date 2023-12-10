import json
import sqlite3
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from airtable import Airtable

# Admin Panel Configuration
with open('admin_panel_credentials.json') as file:
    admin_panel_credentials = json.load(file)

telegram_token = 'YOUR_TELEGRAM_TOKEN'
chat_id = 'YOUR_CHAT_ID'
google_credentials_json = 'google_credentials.json'
airtable_api_key = 'YOUR_AIRTABLE_API_KEY'
airtable_base_key = 'YOUR_AIRTABLE_BASE_KEY'

# Google Sheets Integration
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_credentials_json, scope)
client = gspread.authorize(credentials)
sheet = client.open('Название_гугл_таблицы').sheet1

# SQLite Database Connection
database = sqlite3.connect('database.db')
cursor = database.cursor()

# Airtable Integration
airtable = Airtable('YOUR_AIRTABLE_BASE_ID', 'название_таблицы', api_key='YOUR_AIRTABLE_API_KEY')

# Saving and Checking Duplicate Messages
def check_duplicate_message(message_id):
    cursor.execute(f"SELECT * FROM messages WHERE message_id = {message_id}")
    result = cursor.fetchone()
    return result is not None

def save_message(message_id, chat_id, text):
    cursor.execute(f"INSERT INTO messages (message_id, chat_id, text) VALUES ({message_id}, {chat_id}, '{text}')")
    database.commit()

# Forwarding Messages
def forward_message(message):
    bot.forward_message(chat_id, message.chat.id, message.message_id)

    # Append message text and chat ID to the Google Sheet
    sheet.append_row([message.text, message.chat.id])

    # Insert message text and chat ID to Airtable
    airtable.insert({'Text': message.text, 'Chat ID': message.chat.id})

# Message Handling
def handle_message(message):
    if message.text:
        message_id = message.message_id
        chat_id = message.chat.id
        text = message.text

        if not check_duplicate_message(message_id):
            keywords = ['keyword1', 'keyword2']  # Add your keywords here
            minus_keywords = ['minus', 'keyword']  # Add your minus keywords here

            if any(keyword in text for keyword in keywords) and not any(keyword in text for keyword in minus_keywords):
                forward_message(message)
                save_message(message_id, chat_id, text)

# Start the Bot
bot = telebot.TeleBot(telegram_token)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    handle_message(message)

bot.polling(none_stop=True)
