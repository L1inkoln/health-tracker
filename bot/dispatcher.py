from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

if not BOT_TOKEN:
    raise ValueError("Токен бота не найден в .env")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
