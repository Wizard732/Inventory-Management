import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from fastapi import FastAPI
from contextlib import asynccontextmanager
from FastAPI.models import Data # импортируем проверку пайдантик
from SQL.db import (
    full_categories,
    categories,
    list_product,
    filter_products, # импортируем все функции бд
    add_products,
    patch_in_products,
    delete_by_id
)



API_TOKEN = "8812490005:AAGU1xoioXQaucL_Kx2VOS4HuBYSAKY-WMw" # create secret key

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    msg = await message.answer(f"Привет, {message.from_user.full_name}! Этот бот создан для системы инвентаря. Хотите ли вы воспользоваться функциями бота? ")

@dp.message(Command("categories"))
async def category(message: types.Message):
    data = full_categories()

    await asyncio.sleep(3)
    msg = await message.answer(f"Данные категории успешно получены {data}!")

@asynccontextmanager
async def fastapi_endpoint(app: FastAPI):
    # Запускаем ваш dp.start_polling, но через create_task (в фоне!)
    bot_task = asyncio.create_task(dp.start_polling(bot))
    print("Бот запущен с эндпоинтами FastAPI.")

    yield # передаем управление фастапи и эндпоинтам

    bot_task.cancel()
    await bot.session.close() # выключаем бота при выключении сервера



app = FastAPI(lifespan=fastapi_endpoint) # создаем приложение и подключаем эндпоинты

@app.get("/categories")
def get_categories():
    return full_categories()