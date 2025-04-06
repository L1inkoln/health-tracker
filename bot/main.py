import asyncio
import logging
from dispatcher import bot, dp, set_bot_commands
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
    await set_bot_commands()

    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
