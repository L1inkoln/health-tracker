from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from config import API_URL


def send_main_menu() -> InlineKeyboardMarkup:
    """Функция для вывода меню пользователю`"""
    return InlineKeyboardMarkup(
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
