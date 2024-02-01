import random
import telebot

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=4)
    markup.add(
        telebot.types.KeyboardButton('d2'),
        telebot.types.KeyboardButton('d3'),
        telebot.types.KeyboardButton('d4'),
        telebot.types.KeyboardButton('d6'),
        telebot.types.KeyboardButton('d8'),
        telebot.types.KeyboardButton('d10'),
        telebot.types.KeyboardButton('d12'),
        telebot.types.KeyboardButton('d16'),
        telebot.types.KeyboardButton('d20'),
        telebot.types.KeyboardButton('d100')
    )
    bot.send_message(message.chat.id, 'Выберите кубик:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['d2', 'd3', 'd4', 'd6', 'd8', 'd10', 'd12', 'd16', 'd20', 'd100'])
def roll_dice(message):
    dice = message.text
    modifier = message.text.split('+')[-1] if '+' in message.text else 0
    result = random.randint(1, int(dice[1:]))
    response = f'Выпало {result} на {dice}{"+" + str(modifier) if modifier else ""}'
    bot.send_message(message.chat.id, response)

bot.polling()
