import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.types import Message

# from aiogram import F

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
    await message.answer(
        "👋 Привет! Я бот для трекинга здоровья.\n\n"
        "Доступные команды:\n"
        "/water - Добавить воду\n"
        "/sleep - Зафиксировать сон"
    )


@dp.message(Command("water"))
async def cmd_water(message: Message):
    await message.answer("💧 Зафиксировано 250 мл воды!")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
