  GNU nano 7.2                                 telebot_monitor/main_2.py                                            
import telebot
import requests
import threading
from telebot import types

# Токен вашего бота
TOKEN = 'TOKEN'

bot = telebot.TeleBot(TOKEN)

def check_messages():
    bot.polling()

def process_message(message):
    if message.text == '/start':
        markup = types.InlineKeyboardMarkup()
        item = types.InlineKeyboardButton('Получить IP', callback_data='get_ip')
        markup.add(item)
        bot.reply_to(message, 'Выберите действие:', reply_markup=markup)
    else:
        bot.reply_to(message, 'Для получения внешнего IP-адреса нажмите /start')

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    message_thread = threading.Thread(target=process_message, args=(message,))
    message_thread.start()

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'get_ip':
        ip = requests.get('https://api.ipify.org').text
        bot.send_message(call.message.chat.id, f'Ваш внешний IP-адрес: {ip}')

if __name__ == '__main__':
    polling_thread = threading.Thread(target=check_messages)
    polling_thread.start()
