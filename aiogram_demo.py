import logging
import asyncio
from aiogram import Bot, Dispatcher, types

# Инициализация бота и диспетчера
TOKEN = 'YOUR_BOT_TOKEN'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Отправляем фото
    with open('cat.png', 'rb') as photo:
        await message.answer_photo(photo)

# Функция запуска бота
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
