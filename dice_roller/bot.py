import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"Привет, {user.first_name}! Я бот для кубиков DnD. Что будем кидать? 🎲"
        )

# Обработчик команды /roll
def roll(update: Update, context: CallbackContext):
    # Создаем кнопки для выбора кубика
    keyboard = [
        [InlineKeyboardButton("d2", callback_data='2'),
         InlineKeyboardButton("d3", callback_data='3'),
         InlineKeyboardButton("d4", callback_data='4')],
        [InlineKeyboardButton("d6", callback_data='6'),
         InlineKeyboardButton("d8", callback_data='8'),
         InlineKeyboardButton("d10", callback_data='10')],
        [InlineKeyboardButton("d12", callback_data='12'),
         InlineKeyboardButton("d16", callback_data='16'),
         InlineKeyboardButton("d20", callback_data='20'),
         InlineKeyboardButton("d100", callback_data='100')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопками
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Выбери кубик:",
        reply_markup=reply_markup
    )

# Обработчик нажатия кнопки
def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    roll_value = int(query.data)

    # Проверяем наличие модификатора в запросе
    if "+" in query.message.text:
        dice, modifier = query.message.text.split("+")
        modifier = int(modifier)
    else:
        dice = query.message.text
        modifier = 0

    # Кидаем кубик и добавляем модификатор
    result = random.randint(1, roll_value) + modifier

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{dice} 🎲\nРезультат: {result}"
    )

# Тело программы
def main():
    # Инициализация бота
    updater = Updater("TOKEN", use_context=True)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("roll", roll))
    dispatcher.add_handler(CallbackQueryHandler(button_click))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
