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


@dp.callback_query(lambda c: c.data == "get_stats")
async def handle_stats(callback_query: CallbackQuery):
    await callback_query.answer()

    if callback_query.from_user is None:
        return
    telegram_id = callback_query.from_user.id
    stats = await get_statistics(telegram_id)
    if isinstance(stats, dict):
        stats_message = (
            f"📊 Ваша статистика:\n"
            f"🍽 Калорий: {stats['calories']}\n"
            f"💧 Вода: {stats['water']} литров\n"
            f"😴 Сон: {stats['sleep']} часов\n"
            f"🚶 Шагов: {stats['steps']}"
        )
        await callback_query.message.answer(stats_message)
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
        "Введите количество калорий и воды через пробел (например: `2500 2`):"
    )
    await state.set_state(Form.waiting_for_nutrition)


@dp.callback_query(lambda c: c.data == "category_health")
async def process_health(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите количество шагов:")
    await state.set_state(Form.waiting_for_health)


# Ввод данных
@dp.message(Form.waiting_for_sleep)
async def handle_sleep_input(message: Message, state: FSMContext):
    if message.from_user is None:
        return
    user_id = message.from_user.id
    try:
        hours = int(message.text)
        result = await update_sleep(user_telegram_id=user_id, hours=hours)
        await message.answer(result)
    except ValueError:
        await message.answer("Введите число.")
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
        result = await update_nutrition(
            user_telegram_id=message.from_user.id, calories=calories, water=water
        )
        await message.answer(result)
    except Exception:
        await message.answer(
            "Введите данные в формате: калории вода (например: 2000 1.5)"
        )
    await state.clear()
    await message.answer("🔙 Возврат в меню", reply_markup=send_main_menu())


@dp.message(Form.waiting_for_health)
async def handle_health_input(message: Message, state: FSMContext):
    if message.from_user is None:
        return
    try:
        steps = int(message.text)
        result = await update_health(user_telegram_id=message.from_user.id, steps=steps)
        await message.answer(result)
    except ValueError:
        await message.answer("Введите корректное число.")
    await state.clear()
    await message.answer("🔙 Возврат в меню", reply_markup=send_main_menu())
