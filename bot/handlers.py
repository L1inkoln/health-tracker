import logging
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils import (
    register_user,
    get_statistics,
    send_main_menu,
    update_sleep,
    update_nutrition,
    update_health,
    plural_form,
    compare,
    reset_statistics,
)
from dispatcher import dp


logger = logging.getLogger(__name__)


# Состояния для каждой категории
class Form(StatesGroup):
    waiting_for_sleep = State()
    waiting_for_nutrition = State()
    waiting_for_health = State()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    if message.from_user is None:
        return
    user_id = message.from_user.id
    reg_status = await register_user(user_id)
    if reg_status is True:
        await message.answer(
            "✅ Вы успешно зарегистрированы!\nВыберите категорию:",
            reply_markup=send_main_menu(),
        )
    else:
        await message.answer(
            f"⚠ {reg_status}\nВыберите категорию:",
            reply_markup=send_main_menu(),
        )


@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    if message.from_user is None:
        return
    await message.answer(
        "🔙 Вернулись в главное меню. Выберите категорию:",
        reply_markup=send_main_menu(),
    )


@dp.message(Command("reset"))
async def reset_stats_handler(message: Message):
    if message.from_user is None:
        return
    telegram_id = message.from_user.id
    response = await reset_statistics(telegram_id)
    if response is True:
        await message.answer(
            "🧹 Ваша статистика была успешно сброшена.",
            reply_markup=send_main_menu(),
        )
    else:
        await message.answer(
            "❌ Ошибка при сбросе статистики.",
            reply_markup=send_main_menu(),
        )


@dp.callback_query(lambda c: c.data == "get_stats")
async def handle_stats(callback_query: CallbackQuery):
    await callback_query.answer()

    if callback_query.from_user is None:
        return
    telegram_id = callback_query.from_user.id
    stats = await get_statistics(telegram_id)

    if isinstance(stats, dict):
        norm_calories = 2300
        norm_water = 2.0
        norm_sleep = 8
        norm_steps = 5000

        # Данные пользователя
        calories = stats["calories"]
        water = stats["water"]
        sleep = stats["sleep"]
        steps = stats["steps"]

        # Форматирование окончаний
        water_label = plural_form(water, ("литр", "литра", "литров"))
        sleep_label = plural_form(sleep, ("час", "часа", "часов"))
        steps_label = plural_form(steps, ("шаг", "шага", "шагов"))
        calories_label = plural_form(calories, ("калория", "калории", "калорий"))

        water_note = compare(water, norm_water, "Воды достаточно", "Недостаток воды")
        sleep_note = compare(sleep, norm_sleep, "Сон в норме", "Недостаток сна")
        steps_note = compare(steps, norm_steps, "Хорошая активность", "Мало шагов")
        calories_note = compare(
            calories, norm_calories, "Калорийность достаточная", "Недостаток калорий"
        )

        stats_message = (
            f"📊 <b>Ваша статистика:</b>\n\n"
            f"🍽 Калории: {calories} {calories_label}\n{calories_note}\n\n"
            f"💧 Вода: {water} {water_label}\n{water_note}\n\n"
            f"😴 Сон: {sleep} {sleep_label}\n{sleep_note}\n\n"
            f"🚶 Шаги: {steps} {steps_label}\n{steps_note}"
        )

        await callback_query.message.answer(stats_message, parse_mode="HTML")
        await callback_query.message.answer(
            "🔙 Возврат в меню", reply_markup=send_main_menu()
        )

    else:
        await callback_query.message.answer(f"❌ Ошибка: {stats}")


@dp.callback_query(lambda c: c.data == "category_sleep")
async def process_sleep(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # снимаем выделение кнопки
    await callback.message.answer("Введите количество часов сна:")
    await state.set_state(Form.waiting_for_sleep)


@dp.callback_query(lambda c: c.data == "category_nutrition")
async def process_nutrition(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        "Введите количество калорий и литры воды через пробел (например: `2500 0.5`):"
    )
    await state.set_state(Form.waiting_for_nutrition)


@dp.callback_query(lambda c: c.data == "category_health")
async def process_health(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите количество шагов:")
    await state.set_state(Form.waiting_for_health)


@dp.message(Form.waiting_for_sleep)
async def handle_sleep_input(message: Message, state: FSMContext):
    if message.from_user is None:
        return
    user_id = message.from_user.id
    try:
        hours = int(message.text)
        if hours < 0 or hours > 24:
            await message.answer(
                "❌ Некорректное значение. Введите количество часов сна от 0 до 24."
            )
        else:
            result = await update_sleep(user_telegram_id=user_id, hours=hours)
            await message.answer(result)
    except ValueError:
        await message.answer(" ❌ Введите целое число.")
    await state.clear()
    await message.answer("🔙 Возврат в меню", reply_markup=send_main_menu())


@dp.message(Form.waiting_for_nutrition)
async def handle_nutrition_input(message: Message, state: FSMContext):
    if message.from_user is None:
        return
    try:
        calories_str, water_str = message.text.split()
        calories = int(calories_str)
        water = float(water_str)

        if not (0 <= calories <= 10000):
            await message.answer("❌ Калорий должно быть от 0 до 10000.")
        elif not (0 <= water <= 10):
            await message.answer("❌ Воды должно быть от 0 до 10 литров.")
        else:
            result = await update_nutrition(
                user_telegram_id=message.from_user.id, calories=calories, water=water
            )
            await message.answer(result)

    except Exception:
        await message.answer(
            "❌ Ошибка введите данные в формате: калории вода (например: 2000 0.5)"
        )
    await state.clear()
    await message.answer("🔙 Возврат в меню", reply_markup=send_main_menu())


@dp.message(Form.waiting_for_health)
async def handle_health_input(message: Message, state: FSMContext):
    if message.from_user is None:
        return
    try:
        steps = int(message.text)
        if steps < 0 or steps > 50000:
            await message.answer("❌ Шагов должно быть от 0 до 50000.")
        else:
            result = await update_health(
                user_telegram_id=message.from_user.id, steps=steps
            )
            await message.answer(result)
    except ValueError:
        await message.answer("❌ Ошибка введите целое число.")
    await state.clear()
    await message.answer("🔙 Возврат в меню", reply_markup=send_main_menu())
