import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
import gspread
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Переменная окружения {name} не найдена")
    return value

credentials_file = get_env_variable('GOOGLE_CREDENTIALS_FILE')
spreadsheet_name = get_env_variable('SPREADSHEET_NAME')
BOT_TOKEN = get_env_variable('BOT_TOKEN')

gc = gspread.service_account(filename=credentials_file)
worksheet = gc.open_by_key(spreadsheet_name).sheet1

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class InputSurname(StatesGroup):
    input_surname = State()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    button1 = KeyboardButton(text="Правила получения очков")
    button2 = KeyboardButton(text="Просмотреть свои очки опыта")

    greet_kb1 = ReplyKeyboardMarkup(keyboard=[[button1], [button2]], resize_keyboard=True)

    await message.answer("Привет, дорогой друг! Выбери интересующий тебя вопрос", reply_markup=greet_kb1)

@dp.message(lambda message: message.text == "Правила получения очков")
async def process_rules(message: types.Message):
    # Обработка нажатия на кнопку "Правила получения очков"
    await message.answer_photo(photo=FSInputFile(path="./images/rules.jpg"))

@dp.message(StateFilter(None), lambda message: message.text == "Просмотреть свои очки опыта")
async def process_points(message: types.Message, state: FSMContext):
    # Обработка нажатия на кнопку "Просмотреть свои очки опыта"
    await message.answer("Пожалуйста, укажи свою фамилию (обязательно напиши её с большой буквы)")
    await state.set_state(InputSurname.input_surname)

@dp.message(InputSurname.input_surname)
async def input_surname_handler(message: types.Message, state: FSMContext):
    try:
        full_name = message.text

        if full_name is None:
            await message.reply("Отправьте ФИО")
            return

        cell = worksheet.find(full_name, in_column=3)

        if (cell is None):
            await message.reply("ФИО не найдено в таблице.")
            return

        data = worksheet.row_values(cell.row)

        pp = data[0]
        result = data[15]

        if pp is None:
            await message.reply("ФИО не найдено в таблице.")
            return

        pp = int(pp)
        if pp <= 10:
            photo_path = "./images/top_10.jpg"
        elif pp <= 20:
            photo_path = "./images/top_20.jpg"
        elif pp <= 30:
            photo_path = "./images/top_30.jpg"
        else:
            photo_path = "./images/top_50.jpg"

        await message.reply_photo(photo=FSInputFile(path=photo_path))

        await message.answer(f"Дорогой друг, поздравляю, ты идёшь в правильном направлении!\nСейчас у тебя: <b>{result}</b> очков опыта")

        await state.clear()
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

async def main() -> None:
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())