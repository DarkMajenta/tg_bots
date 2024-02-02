import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackContext, CallbackQueryHandler, ConversationHandler

# Определение состояний для обработчика разговора
DICE, MODIFIER = range(2)

# Обработчик команды /start
def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"Привет, {user.first_name}! Я бот для кубиков DnD. Что будем кидать? 🎲"
        )

# Обработчик команды /roll
def roll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    return DICE

# Обработчик нажатия кнопки
def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE)  -> None:
    query = update.callback_query
    roll_value = int(query.data)

    # Сохраняем выбранный кубик в контексте
    context.user_data['dice'] = query.message.text

    # Запрашиваем модификатор у пользователя
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введите модификатор:"
    )

    return MODIFIER

# Обработчик модификатора
def get_modifier(update: Update, context: ContextTypes.DEFAULT_TYPE)  -> None:
    modifier = int(update.message.text.strip())

    # Получаем выбранный кубик из контекста
    dice = context.user_data.get('dice')

    # Кидаем кубик и добавляем модификатор
    result = random.randint(1, int(dice[1:])) + modifier

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{dice} 🎲\nРезультат: {result}"
    )

    return ConversationHandler.END

# Тело программы
def main() -> None:
    # Инициализация бота
    #application = Updater("TOKEN")
    #application = application.application
    application = Application.builder().token("TOKEN").build()
    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler("roll", roll)],
        states={
            DICE: [CallbackQueryHandler(button_click)],
            MODIFIER: [MessageHandler(None, get_modifier)]
        },
        fallbacks=[]
    ))

    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    application.idle()

if __name__ == '__main__':
    main()
