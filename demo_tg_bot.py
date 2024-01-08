from telegram.ext import Updater, MessageHandler, Filters

# Обработчик входящих сообщений
def handle_message(update, context):
    message = update.message
    # Здесь можно обрабатывать текст сообщений, проверять упоминания и т.д.
    # Например, можешь использовать message.text и реализовать нужную функциональность

    # Отправка ответного сообщения
    chat_id = message.chat_id
    context.bot.send_message(chat_id=chat_id, text='Привет, я бот!')

# Создание экземпляра бота
updater = Updater(token='ВСТАВЬ_ТОКЕН_СВОЕГО_БОТА')

# Получение диспетчера для регистрации обработчиков
dispatcher = updater.dispatcher

# Регистрация обработчика входящих сообщений
message_handler = MessageHandler(Filters.text, handle_message)
dispatcher.add_handler(message_handler)

# Запуск бота
updater.start_polling()
