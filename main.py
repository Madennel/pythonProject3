import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем значение токена из переменной окружения
API_TOKEN = os.getenv("API_TOKEN")

# Проверяем, что токен загружен корректно
if API_TOKEN is None:
    raise ValueError("API токен не найден. Проверьте .env файл.")


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

router = Router()


@router.message(Command(commands=["start"]))
async def start(message: Message):
    print('Привет! Я бот, помогающий твоему здоровью.')
    await message.answer("Привет! Я бот, помогающий твоему здоровью.")


# Функция для обработки любых других сообщений
@router.message()
async def all_messages(message: Message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer("Введите команду /start, чтобы начать общение.")

# Подключаем маршрутизатор к диспетчеру
dp.include_router(router)


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
