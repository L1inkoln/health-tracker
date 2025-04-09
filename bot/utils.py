from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import httpx
from config import API_URL, BOT_SECRET

# Client для асинхронных запросов к API
if API_URL is not None:
    client = httpx.AsyncClient(base_url=API_URL)

jwt_token = None


async def get_jwt_token():
    global jwt_token
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_URL}/auth/bot", json={"password": BOT_SECRET}
            )
            response.raise_for_status()
            jwt_token = response.json()["access_token"]
            print("✅ JWT токен успешно получен")
    except Exception as e:
        print(f"❌ Ошибка при получении токена: {e}")


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
            [
                InlineKeyboardButton(
                    text="🎯 Обновить цели", callback_data="update_goals"
                )
            ],
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
        response = await client.post(
            f"{API_URL}/register/",
            json=payload,
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
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
        response = await client.get(
            f"{API_URL}/statistics/{telegram_id}",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        if response.status_code == 200:
            return response.json()
        else:
            return f"Ошибка {response.status_code}: {response.text}"
    except httpx.RequestError as e:
        return f"Ошибка подключения к API: {e}"


async def get_goals(telegram_id: int):
    """Получает цели пользователя по telegram_id"""
    try:
        response = await client.get(
            f"{API_URL}/goals/{telegram_id}",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        if response.status_code == 200:
            return response.json()
        else:
            return f"Ошибка {response.status_code}: {response.text}"
    except httpx.RequestError as e:
        return f"Ошибка подключения к API: {e}"


async def update_goals(telegram_id: int, payload: dict):
    """Обновляет одну или несколько целей пользователя"""
    try:
        response = await client.patch(
            f"{API_URL}/goals/{telegram_id}",
            headers={"Authorization": f"Bearer {jwt_token}"},
            json=payload,
        )
        if response.status_code == 200:
            return True
        else:
            return f"Ошибка {response.status_code}: {response.text}"
    except httpx.RequestError as e:
        return f"Ошибка подключения к API: {e}"


async def reset_statistics(telegram_id: int):
    """Сбрасывает статистику пользователя"""
    try:
        response = await client.patch(
            f"{API_URL}/reset/{telegram_id}",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        if response.status_code == 200:
            return True
        else:
            return f"Ошибка {response.status_code}: {response.text}"
    except httpx.RequestError as e:
        return f"Ошибка подключения к API: {e}"


def plural_form(n: int | float, forms: tuple[str, str, str]) -> str:
    n = abs(int(n))
    if n % 10 == 1 and n % 100 != 11:
        return forms[0]
    elif 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        return forms[1]
    else:
        return forms[2]


# Подсказки
def compare(val, norm, good_msg, low_msg):
    if val >= norm:
        return f"✅ {good_msg}"
    else:
        return f"⚠️ {low_msg} (норма: {norm})"


async def update_sleep(user_telegram_id: int, hours: float):
    """Обновляет количество часов сна для пользователя"""
    payload = {"user_telegram_id": user_telegram_id, "hours": hours}
    try:
        response = await client.post(
            f"{API_URL}/sleep/",
            json=payload,
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
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
        response = await client.post(
            f"{API_URL}/nutrition/",
            json=payload,
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
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
        response = await client.post(
            f"{API_URL}/health/",
            json=payload,
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        if response.status_code == 200:
            return f"✅ Шаги обновлены: {steps}"
        else:
            return f"❌ Ошибка {response.status_code}: {response.text}"
    except httpx.RequestError as e:
        return f"Ошибка подключения к API: {e}"


async def delete_user(user_telegram_id: int):
    """Удаляет пользователя из базы"""
    try:
        response = await client.request(
            method="DELETE",
            url=f"{API_URL}/delete/{user_telegram_id}",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        if response.status_code == 200:
            return True
        else:
            return f"❌ Ошибка при удалении {response.status_code}: {response.text}"
    except httpx.RequestError as e:
        return f"Ошибка подключения к API: {e}"
