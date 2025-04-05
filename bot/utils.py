from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import httpx
from config import API_URL

# Client для асинхронных запросов к API
if API_URL is not None:
    client = httpx.AsyncClient(base_url=API_URL)


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
        response = await client.post(f"{API_URL}/register/", json=payload)
        if response.status_code == 200:
            return True
        elif response.status_code == 400:
            return "Вы уже зарегистрированы."
        else:
            return f"Ошибка {response.status_code}: {response.text}"
    except httpx.RequestError as e:
        return f"Ошибка подключения к API: {e}"


async def get_statistics(telegram_id: int):
    """Получает статистику пользователя по telegram_id"""
    try:
        response = await client.get(f"{API_URL}/statistics/{telegram_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return f"Ошибка {response.status_code}: {response.text}"
    except httpx.RequestError as e:
        return f"Ошибка подключения к API: {e}"


async def update_sleep(user_telegram_id: int, hours: int):
    """Обновляет количество часов сна для пользователя"""
    payload = {"user_telegram_id": user_telegram_id, "hours": hours}
    try:
        response = await client.post(f"{API_URL}/sleep/", json=payload)
        if response.status_code == 200:
            return f"✅ Часы сна обновлены: {hours} часов."
        else:
            return f"❌ Ошибка {response.status_code}: {response.text}"
    except httpx.RequestError as e:
        return f"Ошибка подключения к API: {e}"


async def update_nutrition(user_telegram_id: int, calories: int, water: float):
    """Обновляет данные питания для пользователя"""
    payload = {
        "user_telegram_id": user_telegram_id,
        "calories": calories,
        "water": water,
    }
    try:
        response = await client.post(f"{API_URL}/nutrition/", json=payload)
        if response.status_code == 200:
            return f"✅ Питание обновлено: {calories} калорий, {water} л воды."
        else:
            return f"❌ Ошибка {response.status_code}: {response.text}"
    except httpx.RequestError as e:
        return f"Ошибка подключения к API: {e}"


async def update_health(user_telegram_id: int, steps: int):
    """Обновляет количество шагов для пользователя"""
    payload = {"user_telegram_id": user_telegram_id, "steps": steps}
    try:
        response = await client.post(f"{API_URL}/health/", json=payload)
        if response.status_code == 200:
            return f"✅ Шаги обновлены: {steps}"
        else:
            return f"❌ Ошибка {response.status_code}: {response.text}"
    except httpx.RequestError as e:
        return f"Ошибка подключения к API: {e}"
