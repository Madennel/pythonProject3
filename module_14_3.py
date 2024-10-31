import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение API токена из .env файла
API_TOKEN = os.getenv("API_TOKEN")

# Проверка на наличие токена
if API_TOKEN is None:
    raise ValueError("API токен не найден в .env файле.")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера с памятью для хранения состояний
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Определение группы состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Создание главной клавиатуры
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Рассчитать"), KeyboardButton(text="Информация"), KeyboardButton(text="Купить")]
    ],
    resize_keyboard=True
)

# Inline-клавиатура для выбора продуктов
products_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Магний с витамином В6 - 863 руб.", callback_data="product_buying")],
        [InlineKeyboardButton(text="Магний В6 (NFO) - 1,020 руб.", callback_data="product_buying")],
        [InlineKeyboardButton(text="Solgar Магний цитрат - 1,404 руб.", callback_data="product_buying")],
        [InlineKeyboardButton(text="Ultrabalance Omega-3 - 1,250 руб.", callback_data="product_buying")]
    ]
)

# Загрузка изображений продуктов (можно загрузить на сервер Telegram и сохранить ID)
product_images = [
    'local_path/magniy_vitamin_v6.jpg',  # Магний с витамином В6
    'local_path/magniy_v6_nfo.jpg',  # Магний В6 (NFO)
    'local_path/solgar_magniy_citrat.jpg',  # Solgar Магний цитрат
    'local_path/ultrabalance_omega3.jpg'  # Ultrabalance Omega-3
]


# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer(
        "Привет! Я бот для расчета калорий и покупок. Выберите действие:",
        reply_markup=keyboard
    )


# Обработчик кнопки "Купить"
@dp.message(lambda message: message.text == "Купить")
async def get_buying_list(message: Message):
    products = [
        ("Магний с витамином В6", "300 мг, 60 капсул - 863 руб.", product_images[0]),
        ("Магний В6 (NFO)", "120 таблеток - 1,020 руб.", product_images[1]),
        ("Solgar Магний цитрат", "200 мг, 60 таблеток - 1,404 руб.", product_images[2]),
        ("Ultrabalance Omega-3", "1000 мг - 1,250 руб.", product_images[3])
    ]
    for name, description, image_path in products:
        with open(image_path, 'rb') as photo:
            await message.answer_photo(photo, caption=f"Название: {name} | Описание: {description}")
    await message.answer("Выберите продукт для покупки:", reply_markup=products_kb)


# Обработчик подтверждения покупки
@dp.callback_query(lambda call: call.data == "product_buying")
async def send_confirm_message(call: CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
