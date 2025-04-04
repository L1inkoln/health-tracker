import asyncio
import logging
from dispatcher import bot, dp
import handlers  # noqa: F401

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    print("✅ Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
