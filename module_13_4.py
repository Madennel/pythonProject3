from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
import logging

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
    growth = State() # Состояние для ввода роста
    weight = State() # Состояние для ввода веса

# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer("Привет! Я бот! Введите команду 'Calories', чтобы начать расчет нормы калорий.")

# Функция для начала запроса данных (возраст)
@dp.message(Command(commands=["Calories"]))
async def set_age(message: Message, state: FSMContext):
    await message.answer("Введите свой возраст:")
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
