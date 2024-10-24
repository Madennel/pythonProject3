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
    age = State()    # Состояние для ввода возраста
    growth = State()  # Состояние для ввода роста
    weight = State()  # Состояние для ввода веса


# Создание обычной клавиатуры с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Рассчитать"), KeyboardButton(text="Информация")]
    ],
    resize_keyboard=True
)

# Создание Inline-клавиатуры с двумя кнопками
inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")],
        [InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")]
    ]
)


# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer(
        "Привет! Я бот для расчета калорий. Выберите действие:",
        reply_markup=keyboard
    )


# Обработчик для обычной кнопки "Рассчитать", выводит Inline-клавиатуру
@dp.message(lambda message: message.text == "Рассчитать")
async def main_menu(message: Message):
    await message.answer("Выберите опцию:", reply_markup=inline_kb)


# Обработчик для кнопки "Формулы расчёта" из Inline-клавиатуры
@dp.callback_query(lambda call: call.data == "formulas")
async def get_formulas(call: CallbackQuery):
    formula_text = (
        "Формула Миффлина-Сан Жеора для женщин:\n"
        "10 * вес (кг) + 6.25 * рост (см) - 5 * возраст - 161"
    )
    await call.message.answer(formula_text)


# Обработчик для кнопки "Рассчитать норму калорий"
@dp.callback_query(lambda call: call.data == "calories")
async def set_age(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)


# Обработчик для возраста
@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    # Сохраняем возраст
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (в сантиметрах):")
    await state.set_state(UserState.growth)


# Обработчик для роста
@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    # Сохраняем рост
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес (в килограммах):")
    await state.set_state(UserState.weight)


# Обработчик для веса и отправки результата
@dp.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    # Сохраняем вес
    await state.update_data(weight=message.text)

    # Получаем все данные
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    # Формула Миффлина-Сан Жеора для женщин:
    # Для женщин: 10 * вес + 6.25 * рост - 5 * возраст - 161
    calories = 10 * weight + 6.25 * growth - 5 * age - 161

    # Отправляем результат пользователю
    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал")

    # Завершаем машину состояний
    await state.clear()


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
