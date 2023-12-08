import telebot
import requests
import random
from datetime import datetime, time, timedelta

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHANNEL_ID = 'YOUR_TELEGRAM_CHANNEL_ID'
YML_FEED_URL = 'https://autoeuropa.by/tstore/yml/c9711c38561c374416df501f41d60f9e.yml'
PRODUCT_FIELDS = ['фото', 'заголовок', 'привод', 'топливо', 'цена']
WORK_HOURS = (time(8), time(22))  # Рабочее время с 8:00 до 22:00
WORK_DAYS = [0, 1, 2, 3, 4]  # Рабочие дни: Понедельник - Пятница
PRODUCTS_PER_HOUR = 2  # Количество товаров для размещения в час
DELAY_MIN = 5  # Минимальная задержка (в секундах) перед размещением следующего товара
DELAY_MAX = 10  # Максимальная задержка (в секундах) перед размещением следующего товара
TEXT_ABOVE_URL = "Произвольный текст сверху URLа"

bot = telebot.TeleBot(TOKEN)

# Функция для получения случайного товара из YML-фида
def get_random_product_from_feed():
    response = requests.get(YML_FEED_URL)
    if response.status_code == 200:
        feed_data = response.text
        # Реализуйте парсинг данных из YML-фида и выберите случайный товар
        # Верните информацию о выбранном товаре в заданном порядке полей
        # Пример: return (photo_url, title, drive, fuel, price, product_url)
    return None

# Функция для форматирования информации о товаре
def format_product_info(product):
    formatted_info = []
    formatted_info.append(f'{product[0]}')  # фото
    formatted_info.append(f'<b>{product[1]}</b>')  # заголовок
    formatted_info.append(f'Привод: {product[2]}')  # привод
    formatted_info.append(f'Топливо: {product[3]}')  # топливо
    formatted_info.append(f'<b>{product[4]}</b>')  # цена
    formatted_info.append(f'{TEXT_ABOVE_URL}\n{product[5]}')  # URL на товар
    return '\n'.join(formatted_info)

# Функция для проверки, находится ли текущее время в рабочем диапазоне
def is_work_time():
    current_time = datetime.now().time()
    return current_time >= WORK_HOURS[0] and current_time <= WORK_HOURS[1] and datetime.now().weekday() in WORK_DAYS

# Функция для отправки товара в Telegram-канал
def send_product_to_channel():
    product = get_random_product_from_feed()
    if product:
        formatted_product_info = format_product_info(product)
        bot.send_message(CHANNEL_ID, formatted_product_info, parse_mode='HTML')

# Функция для запуска бота
def run_bot():
    while True:
        if is_work_time():
            for _ in range(PRODUCTS_PER_HOUR):
                send_product_to_channel()
                delay = random.randint(DELAY_MIN, DELAY_MAX)
                datetime.now() + timedelta(seconds=delay).timestamp()
        else:
            # Подождать до начала следующего рабочего дня
            next_workday = datetime.now() + timedelta(days=1)
            next_workday = next_workday.replace(hour=WORK_HOURS[0].hour, minute=0, second=0)
            sleep_time = (next_workday - datetime.now()).seconds
            datetime.now() + timedelta(seconds=sleep_time).timestamp()
            continue

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    run_bot()

bot.polling()
