import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery, InputMediaPhoto
from dotenv import load_dotenv
from crud_functions import initiate_db, get_all_products

# Загрузка переменных окружения
load_dotenv()

# Получение API токена из .env файла
API_TOKEN = os.getenv("API_TOKEN")
if API_TOKEN is None:
    raise ValueError("API токен не найден в .env файле.")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация базы данных и таблицы Products
initiate_db()

# Создание клавиатуры с кнопкой "Купить"
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Купить")]
    ],
    resize_keyboard=True
)


# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer(
        "Привет! Я бот для покупки продуктов. Выберите действие:",
        reply_markup=main_keyboard
    )


# Обработчик для кнопки "Купить", формирует список товаров и Inline-клавиатуру
@dp.message(lambda message: message.text == "Купить")
async def get_buying_list(message: Message):
    # Получаем список продуктов из базы данных
    products = get_all_products()

    for product in products:
        title, description, price, file_id = product[1], product[2], product[3], product[4]

        # Создаём кнопки для продукта
        inline_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"Купить {title} за {price} руб.", callback_data=f"product_{product[0]}")]
        ])

        # Отправляем сообщение с изображением и кнопкой
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=file_id,
            caption=f"Название: {title}\nОписание: {description}\nЦена: {price} руб.",
            reply_markup=inline_kb
        )


# Обработчик нажатия на любую кнопку продукта
@dp.callback_query(lambda call: call.data.startswith("product_"))
async def send_confirm_message(call: CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
