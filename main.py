import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
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
worksheet = gc.open(spreadsheet_name).sheet1

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет! Отправь мне ФИО, и я найду информацию в таблице.")

@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        full_name = message.text;

        if full_name is None:
            await message.reply("Отправьте ФИО")
            return

        cell = worksheet.find(full_name, in_column=3)

        if (cell is None):
            await message.reply("ФИО не найдено в таблице.")
            return

        data = worksheet.row_values(cell.row)
        pp = data[0]
        result = data[16]
        await message.reply(f"<b>ФИО:</b> {full_name}\n<b>№ п/п:</b> {pp}\n<b>Итог:</b> {result}")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

async def main() -> None:
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())