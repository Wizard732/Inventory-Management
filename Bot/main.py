import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


API_TOKEN = "8812490005:AAGU1xoioXQaucL_Kx2VOS4HuBYSAKY-WMw" # create secret key

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    start.msg = await message.answer(f"Этот бот создан для системы инвентаря. Хотите ли вы воспользоваться функциями бота? ")


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())