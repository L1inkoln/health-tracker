import asyncio
import logging
from aiogram.types import BotCommand
from dispatcher import bot, dp
from utils import client, get_jwt_token
import handlers  # noqa: F401

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_shutdown():
    """Закрытие клиента при завершении работы"""
    await client.aclose()
    print("🚪 HTTP клиент закрыт")


async def main():
    print("✅ Бот запущен")
    await get_jwt_token()
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Начать работу с ботом"),
            BotCommand(command="menu", description="Показать главное меню"),
        ]
    )

    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
