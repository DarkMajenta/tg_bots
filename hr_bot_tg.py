from telegram.ext import Updater, MessageHandler, Filters
from datetime import datetime, timedelta

# Приветственные сообщения
welcome_messages = [
    "Приветственное сообщение 1",
    "Приветственное сообщение 2 ответ"
]

# Сообщения для обучения
learning_messages = [
    "Сообщение 1 обучение",
    "Сообщение 2 обучение"
]

# Сообщения для прогрева
warming_messages = [
    "Сообщение 1 прогрев",
    "Сообщение 2 прогрев",
    "Сообщение 3 прогрев",
    "Сообщение 4 прогрев",
    "Сообщение 5 прогрев"
]

# Список разрешенных ответов
positive_responses = ["+", "готов", "понял", "ок", "да"]
negative_responses = ["не интересно", "не моё", "не актуально"]

# Время ожидания молчания пользователя
silence_timeout = timedelta(minutes=5)

# Время ожидания ответа пользователя
response_timeout = timedelta(minutes=5)

# Обработчик сообщений
def handle_message(update, context):
    message = update.message.text

    # Первое сообщение - приветствие
    if message.lower().strip() == "начать":
        send_welcome_messages(update)
    else:
        # Получаем данные о последнем контакте пользователя
        last_contact = get_last_contact()
        
        if last_contact is None:
            # Пользователь не контактировал ранее
            send_welcome_messages(update)
        else:
            last_contact_time = last_contact["time"]
            last_contact_type = last_contact["type"]

            if last_contact_type == "welcome":
                # Если последний контакт - приветствие, проверяем ответ пользователя
                if message.lower() in positive_responses:
                    start_learning(update)
                elif message.lower() in negative_responses:
                    start_warming(update)
                else:
                    # Пользователь отправил некорректный ответ, отправляем уведомление / переводим в ручной режим
                    notify_manager(update)
            elif last_contact_type == "warming":
                # Если последний контакт - прогрев, проверяем ответ пользователя
                if message.strip() == "":
                    if datetime.now() - last_contact_time > silence_timeout:
                        start_learning(update)
                    else:
                        continue_warming(update)
                else:
                    # Пользователь отправил сообщение во время прогрева, начинаем обучение
                    start_learning(update)
            elif last_contact_type == "learning":
                # Если последний контакт - обучение, проверяем ответ пользователя
                if message.strip() == "":
                    if datetime.now() - last_contact_time > silence_timeout:
                        start_learning(update)
                    else:
                        continue_learning(update)
                else:
                    # Пользователь отправил сообщение во время обучения, продолжаем обучение
                    continue_learning(update)

# Отправка приветственных сообщений
def send_welcome_messages(update):
    for message in welcome_messages:
        update.message.reply_text(message)
        update_last_contact(update, "welcome")

# Начало прогрева
def start_warming(update):
    for message in warming_messages:
        update.message.reply_text(message)
        update_last_contact(update, "warming")

# Продолжение прогрева
def continue_warming(update):
    # Получаем индекс последнего сообщения прогрева
    last_warming_index = get_last_warming_index()

    if last_warming_index is not None:
        for i in range(last_warming_index + 1, len(warming_messages)):
            message = warming_messages[i]
            update.message.reply_text(message)
            update_last_contact(update, "warming")

# Начало обучения
def start_learning(update):
    for message in learning_messages:
        update.message.reply_text(message)
        update_last_contact(update, "learning")

# Продолжение обучения
def continue_learning(update):
    # Получаем индекс последнего сообщения обучения
    last_learning_index = get_last_learning_index()

    if last_learning_index is not None:
        for i in range(last_learning_index + 1, len(learning_messages)):
            message = learning_messages[i]
            update.message.reply_text(message)
            update_last_contact(update, "learning")

# Уведомление менеджера / переход в ручной режим
def notify_manager(update):
    # Отправка уведомления или выполнение действий по уведомлению менеджера
    pass

# Получение последнего контакта пользователя
def get_last_contact():
    # Получение данных о последнем контакте пользователя из базы данных или другого источника
    pass

# Обновление данных последнего контакта пользователя
def update_last_contact(update, type):
    # Обновление данных последнего контакта пользователя в базе данных или другом источнике
    pass

# Получение индекса последнего сообщения прогрева
def get_last_warming_index():
    # Ваша реализация для получения индекса последнего сообщения прогрева
    pass

# Получение индекса последнего сообщения обучения
def get_last_learning_index():
    # Ваша реализация для получения индекса последнего сообщения обучения
    pass

def main():
    updater = Updater("TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
