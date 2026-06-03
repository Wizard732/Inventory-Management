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

import os
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("token_name") # create secret key

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    msg = await message.answer(f"Привет, {message.from_user.full_name}! Этот бот создан для системы инвентаря. Хотите ли вы воспользоваться функциями бота? ")

@dp.message(Command("categories"))
# return categories
async def category(message: types.Message):
    data = full_categories()

    await asyncio.sleep(3)
    msg = await message.answer(f"Данные категории успешно получены {data}!")


@dp.message(Command("add_categories"))
# add category
async def add_cat(message: types.Message):
    args = message.text.split() # add space

    if len(args) < 3:
        await message.answer("Ошибка! Правильный формат команды: `/add_categories [ID] [Имя]`\nПример: `/add_categories 5 Обувь`")
        return

    input_id = args[1]
    category_name = " ".join(args[2:]).strip()

    if not input_id.isdigit():
        await message.answer("Ошибка: ID категории должен быть числом! Пример: 5")
        return

    category_id = int(input_id)

    if category_name in full_categories():
        await message.answer(f"Ошибка: Категория с именем '{category_name}' уже существует в базе!")
        return

    try:
        # Собираем модель Data со значениями от пользователя
        new_item = Data(
            id=category_id,  # ID, который ввел пользователь
            name=category_name,  # Имя, которое ввел пользователь
            category_id=0,  # Заглушка, так как класс Data требует это поле
            price=0  # Заглушка, так как класс Data требует это поле
        )

        # Вызываем вашу оригинальную функцию, код которой вы прислали
        data = categories(item=new_item)

        await asyncio.sleep(2)
        await message.answer(f"✅ Категория успешно создана! ID: {category_id}, Название: '{category_name}'")

    except Exception as e:
        # Если в базе данных уже есть такой ID, то вылетит ошибка, и мы поймаем её здесь
        await message.answer(f"❌ Ошибка базы данных (возможно, такой ID уже занят): {e}")

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

@app.post("/post_categories")
def post_category(item: Data):
    return categories(item)
