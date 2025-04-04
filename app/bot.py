import os
import logging
import requests
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
)


API_URL = "http://127.0.0.1:8000"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Токен бота не найден в .env")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()


async def register_user(telegram_id: int):
    """Регистрирует пользователя в FastAPI при старте"""
    payload = {
        "telegram_id": telegram_id,
        "start_date": datetime.utcnow().isoformat(),
    }

    try:
        response = requests.post(f"{API_URL}/register/", json=payload)
        if response.status_code == 200:
            return True
        elif response.status_code == 400:
            return "Вы уже зарегистрированы."
        else:
            return f"Ошибка {response.status_code}: {response.text}"
    except requests.RequestException as e:
        return f"Ошибка подключения к API: {e}"


async def get_statistics(telegram_id: int):
    """Получает статистику пользователя по telegram_id"""
    try:
        response = requests.get(f"{API_URL}/statistics/{telegram_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return f"Ошибка {response.status_code}: {response.text}"
    except requests.RequestException as e:
        return f"Ошибка подключения к API: {e}"


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обрабатывает команду /start, регистрирует пользователя и выводит меню"""
    if message.from_user is None:
        return

    user_id = message.from_user.id
    reg_status = await register_user(user_id)

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

    if reg_status is True:
        await message.answer(
            "✅ Вы успешно зарегистрированы!\nВыберите категорию:",
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            f"⚠ {reg_status}\nВыберите категорию:", reply_markup=keyboard
        )


@dp.callback_query()
async def handle_callback(callback_query: CallbackQuery):
    """Обрабатывает callback-запросы от кнопок"""
    if callback_query.data == "get_stats":
        telegram_id = callback_query.from_user.id  # Получаем telegram_id пользователя

        stats = await get_statistics(telegram_id)

        if isinstance(stats, dict):
            # Формируем сообщение с статистикой
            stats_message = (
                f"Ваша статистика:\n"
                f"Калорий: {stats['calories']}\n"
                f"Вода: {stats['water']} литров\n"
                f"Сон: {stats['sleep']} часов\n"
                f"Шагов: {stats['steps']}"
            )
            if callback_query.message:
                await callback_query.message.answer(stats_message)
        else:
            # В случае ошибки
            if callback_query.message:
                await callback_query.message.answer(f"❌ Ошибка: {stats}")

        # Убираем клавиатуру после обработки
        if callback_query.message and isinstance(callback_query.message, types.Message):
            await callback_query.message.delete_reply_markup()


@dp.callback_query(lambda c: c.data == "category_sleep")
async def process_sleep(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(callback_query.from_user.id, "Введите количество часов сна:")

    # Здесь обработка сообщения от того же пользователя
    @dp.message(lambda message: message.from_user.id == user_id)
    async def handle_sleep_hours(message: Message):
        if message.text:  # Проверяем, что текст не пустой и не None
            try:
                hours = int(message.text)  # Преобразуем введенные данные в целое число
                payload = {"user_telegram_id": user_id, "hours": hours}

                # Отправляем запрос на сервер для обновления данных
                response = requests.post(f"{API_URL}/sleep/", json=payload)
                if response.status_code == 200:
                    await bot.send_message(
                        callback_query.from_user.id,
                        f"Часы сна обновлены! Новое значение: {hours} часов.",
                    )
                else:
                    await bot.send_message(
                        callback_query.from_user.id,
                        f"Ошибка {response.status_code}: {response.text}",
                    )
            except ValueError:
                await bot.send_message(
                    callback_query.from_user.id, "Пожалуйста, введите корректное число."
                )
        else:
            await bot.send_message(
                callback_query.from_user.id, "Текст сообщения не может быть пустым."
            )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
