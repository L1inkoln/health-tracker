from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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


def menu_update() -> str:
    return (
        "Что хотите обновить?\n"
        "1️⃣ Калории\n"
        "2️⃣ Воду\n"
        "3️⃣ Сон\n"
        "4️⃣ Шаги\n"
        "5️⃣ Все сразу\n\n"
        "Введите номер (например: 1 или 5):"
    )


# Формирование окончаний
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


def generate_stat_message(stats, goals):
    labels = {
        "water": plural_form(stats["water"], ("литр", "литра", "литров")),
        "sleep": plural_form(stats["sleep"], ("час", "часа", "часов")),
        "steps": plural_form(stats["steps"], ("шаг", "шага", "шагов")),
        "calories": plural_form(stats["calories"], ("калория", "калории", "калорий")),
    }

    notes = {
        "water": compare(
            stats["water"], goals["water_goal"], "Воды достаточно", "Недостаток воды"
        ),
        "sleep": compare(
            stats["sleep"], goals["sleep_goal"], "Сон в норме", "Недостаток сна"
        ),
        "steps": compare(
            stats["steps"], goals["steps_goal"], "Хорошая активность", "Мало шагов"
        ),
        "calories": compare(
            stats["calories"],
            goals["calories_goal"],
            "Калорийность достаточная",
            "Недостаток калорий",
        ),
    }

    return (
        f"📊 <b>Ваша статистика:</b>\n\n"
        f"🍽 Калории: {stats['calories']} {labels['calories']}\n{notes['calories']}\n\n"
        f"💧 Вода: {stats['water']} {labels['water']}\n{notes['water']}\n\n"
        f"😴 Сон: {stats['sleep']} {labels['sleep']}\n{notes['sleep']}\n\n"
        f"🚶 Шаги: {stats['steps']} {labels['steps']}\n{notes['steps']}"
    )
