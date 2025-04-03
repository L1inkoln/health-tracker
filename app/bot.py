import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery

# from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.types import Message

from aiogram import F
import requests

API_URL = "http://127.0.0.1:8000"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота с проверкой токена
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Токен бота не найден в .env")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🥗 Питание", callback_data="category_nutrition"
                )
            ],
            [InlineKeyboardButton(text="😴 Сон", callback_data="category_sleep")],
            [InlineKeyboardButton(text="🚶 Здоровье", callback_data="category_health")],
            [InlineKeyboardButton(text="📊 Статистика", callback_data="get_stats")],
        ]
    )
    await message.answer("Выбери категорию:", reply_markup=keyboard)


@dp.callback_query(F.data == "category_nutrition")
async def choose_nutrition(callback: CallbackQuery):
    if callback.message:
        await callback.message.answer(
            "Введите количество калорий или количество воды (в мл)."
        )
    await callback.answer()


@dp.callback_query(F.data == "category_sleep")
async def choose_sleep(callback: CallbackQuery):
    if callback.message:
        await callback.message.answer("Введите количество часов сна.")
    await callback.answer()


@dp.callback_query(F.data == "category_health")
async def choose_health(callback: CallbackQuery):
    if callback.message:
        await callback.message.answer("Введите количество шагов за день.")
    await callback.answer()


@dp.message()
async def send_data_to_api(message: Message):
    if message:
        user_id = message.from_user.id
        text = message.text.strip()

    if text.isdigit():
        value = int(text)
        category = "unknown"

        if "калорий" in message.text.lower():
            category = "calories"
        elif "вода" in message.text.lower():
            category = "water"
        elif "часов сна" in message.text.lower():
            category = "sleep"
        elif "шагов" in message.text.lower():
            category = "steps"

        response = requests.post(
            f"{API_URL}/add_data/",
            json={"user_id": user_id, "category": category, "value": value},
        )

        if response.status_code == 200:
            await message.answer("✅ Данные отправлены в API!")
        else:
            await message.answer("❌ Ошибка отправки данных!")
    else:
        await message.answer("❌ Введите число.")


@dp.callback_query(F.data == "get_stats")
async def get_stats(callback: CallbackQuery):
    user_id = callback.from_user.id
    response = requests.get(f"{API_URL}/get_stats/{user_id}")

    if response.status_code == 200:
        data = response.json()
        stats = data["stats"]
        deviations = data["deviations"]

        report = "\n".join(
            [
                f"🥗 Калории: {stats['calories']} ({'избыток' if deviations['calories'] > 0 else 'недостаток'}) {abs(deviations['calories'])}",
                f"💧 Вода: {stats['water']} ({'избыток' if deviations['water'] > 0 else 'недостаток'}) {abs(deviations['water'])}",
                f"😴 Сон: {stats['sleep']} ({'избыток' if deviations['sleep'] > 0 else 'недостаток'}) {abs(deviations['sleep'])}",
                f"🚶 Шаги: {stats['steps']} ({'избыток' if deviations['steps'] > 0 else 'недостаток'}) {abs(deviations['steps'])}",
            ]
        )

        await callback.message.answer(f"📊 Ваша статистика:\n{report}")
    else:
        await callback.message.answer("❌ Ошибка получения статистики!")
    await callback.answer()


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
