import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

# Константы для состояний разговора
CATEGORY, SEARCH, PRICE_FROM, PRICE_TO, STOP = range(5)

# Функция для обработки команды /start
def start(update, context):
    reply_keyboard = [['Транспорт', 'Электроника', 'Снять задачу']]
    update.message.reply_text(
        'Привет! Я бот для поиска объявлений на olx.uz. Выбери категорию:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return CATEGORY

# Функция для обработки выбора категории
def category(update, context):
    user_input = update.message.text.lower()
    context.user_data['category'] = user_input
    
    if user_input == 'транспорт':
        reply_keyboard = [['Название', 'Цена от', 'Цена до', 'Стоп', 'Очистить']]
        update.message.reply_text(
            'Выбери параметр для поиска в категории "Транспортные средства":',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
    elif user_input == 'электроника':
        reply_keyboard = [['Название', 'Цена от', 'Цена до', 'Стоп', 'Очистить']]
        update.message.reply_text(
            'Выбери параметр для поиска в категории "Электроника":',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
    elif user_input == 'снять задачу':
        update.message.reply_text('Поиск отключен.')
        return ConversationHandler.END

    return SEARCH

# Функция для обработки ввода параметра поиска
def search(update, context):
    context.user_data['search_param'] = update.message.text
    update.message.reply_text('Введите цену (от):')
    return PRICE_FROM

# Функция для обработки ввода цены "от"
def price_from(update, context):
    context.user_data['price_from'] = int(update.message.text)
    update.message.reply_text('Введите цену (до):')
    return PRICE_TO

# Функция для обработки ввода цены "до" и выполнения поиска
def price_to(update, context):
    context.user_data['price_to'] = int(update.message.text)
    update.message.reply_text('Идет поиск объявлений...')

    # Выполнение парсинга объявлений на olx.uz с использованием параметров фильтрации
    # Здесь нужно написать код для парсинга и получения результатов поиска объявлений соответствующих категории и параметрам фильтрации

    # Пример вывода результатов поиска
    update.message.reply_text('Название: ...')
    update.message.reply_text('Фото: ...')
    update.message.reply_text('Описание: ...')
    update.message.reply_text('Ссылка: ...')
    
    return CATEGORY

# Функция для обработки команды "Стоп"
def stop(update, context):
    update.message.reply_text('Поиск отменен.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Функция для обработки команды "Очистить"
def clear(update, context):
    context.user_data.clear()
    update.message.reply_text('Фильтр очищен.')
    return CATEGORY

def main():
    # Инициализация Telegram-бота
    updater = Updater('TOKEN', use_context=True)
    dispatcher = updater.dispatcher

    # Создание и добавление ConversationHandler для управления разговором с ботом
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CATEGORY: [MessageHandler(Filters.text, category)],
            SEARCH: [MessageHandler(Filters.text, search)],
            PRICE_FROM: [MessageHandler(Filters.text, price_from)],
            PRICE_TO: [MessageHandler(Filters.text, price_to)],
        },
        fallbacks=[CommandHandler('stop', stop), CommandHandler('clear', clear)],
    )
    dispatcher.add_handler(conv_handler)

    # Запуск Telegram-бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

