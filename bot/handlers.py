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
    update_goals,
    update_sleep,
    update_nutrition,
    update_health,
    reset_statistics,
    delete_user,
    get_goals,
)
from helpers import menu_update, send_main_menu, generate_stat_message

from dispatcher import dp


logger = logging.getLogger(__name__)


# Состояния для каждой категории
class Form(StatesGroup):
    waiting_for_sleep = State()
    waiting_for_nutrition = State()
    waiting_for_health = State()


class GoalForm(StatesGroup):
    choosing_goal = State()
    updating_goal = State()


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


@dp.message(Command("delete"))
async def delete_user_handler(message: Message):
    if message.from_user is None:
        return
    telegram_id = message.from_user.id
    response = await delete_user(telegram_id)
    if response is True:
        await message.answer(
            "Все данные были удалены.",
            reply_markup=send_main_menu(),
        )
    else:
        await message.answer(
            "❌ Ошибка при удалении попробуйте ещё раз.",
            reply_markup=send_main_menu(),
        )


@dp.callback_query(lambda c: c.data == "get_stats")
async def handle_stats(callback_query: CallbackQuery):
    await callback_query.answer()
    if not callback_query.from_user or not callback_query.message:
        return

    telegram_id = callback_query.from_user.id
    # Получаем статистику и цели
    stats = await get_statistics(telegram_id)
    goals = await get_goals(telegram_id)

    if isinstance(stats, dict) and isinstance(goals, dict):
        stats_message = generate_stat_message(stats, goals)
        await callback_query.message.answer(stats_message, parse_mode="HTML")
        await callback_query.message.answer(
            "🔙 Возврат в меню", reply_markup=send_main_menu()
        )
    else:
        await callback_query.message.answer("❌ Ошибка получения данных.")


@dp.callback_query(lambda c: c.data == "category_sleep")
async def process_sleep(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # снимаем выделение кнопки
    if callback.message is None:
        return
    await callback.message.answer("Введите количество часов сна:")
    await state.set_state(Form.waiting_for_sleep)


@dp.callback_query(lambda c: c.data == "category_nutrition")
async def process_nutrition(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.message is None:
        return
    await callback.message.answer(
        "Введите количество калорий и литры воды через пробел (например: `2500 0.5`):"
    )
    await state.set_state(Form.waiting_for_nutrition)


@dp.callback_query(lambda c: c.data == "category_health")
async def process_health(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.message is None:
        return
    await callback.message.answer("Введите количество шагов:")
    await state.set_state(Form.waiting_for_health)


@dp.callback_query(lambda c: c.data == "update_goals")
async def choose_goal_to_update(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.message is None:
        return
    await callback.message.answer(menu_update())
    await state.set_state(GoalForm.choosing_goal)


@dp.message(Form.waiting_for_sleep)
async def handle_sleep_input(message: Message, state: FSMContext):
    if message.from_user is None or message.text is None:
        return
    user_id = message.from_user.id
    try:
        hours = float(message.text)
        if hours < 0 or hours > 24:
            await message.answer(
                "❌ Некорректное значение. Введите количество часов сна от 0 до 24."
            )
        else:
            result = await update_sleep(user_telegram_id=user_id, hours=hours)
            await message.answer(result)
    except ValueError:
        await message.answer("❌ Введите значение в литрах(например 1 или 0.5).")
    await state.clear()
    await message.answer("🔙 Возврат в меню", reply_markup=send_main_menu())


@dp.message(Form.waiting_for_nutrition)
async def handle_nutrition_input(message: Message, state: FSMContext):
    if message.from_user is None or message.text is None:
        return
    try:
        calories_str, water_str = message.text.split()
        calories = int(calories_str)
        water = float(water_str)
        if not (1 <= calories <= 10000):
            await message.answer("❌ Калорий должно быть от 1 до 10000.")
        elif not (0.1 <= water <= 10):
            await message.answer("❌ Воды должно быть от 0.1 до 10 литров.")
        else:
            result = await update_nutrition(message.from_user.id, calories, water)
            await message.answer(result)
    except Exception:
        await message.answer(
            "❌ Ошибка введите данные в формате: калории вода (например: 2000 0.5)"
        )
    await state.clear()
    await message.answer("🔙 Возврат в меню", reply_markup=send_main_menu())


@dp.message(Form.waiting_for_health)
async def handle_health_input(message: Message, state: FSMContext):
    if message.from_user is None or message.text is None:
        return
    try:
        steps = int(message.text)
        if steps < 0 or steps > 50000:
            await message.answer("❌ Шагов должно быть от 0 до 50000.")
        else:
            result = await update_health(message.from_user.id, steps)
            await message.answer(result)
    except ValueError:
        await message.answer("❌ Ошибка введите целое число.")
    await state.clear()
    await message.answer("🔙 Возврат в меню", reply_markup=send_main_menu())


@dp.message(GoalForm.choosing_goal)
async def handle_goal_choice(message: Message, state: FSMContext):
    choices = {
        "1": "calories_goal",
        "2": "water_goal",
        "3": "sleep_goal",
        "4": "steps_goal",
        "5": "all",
    }
    if message.text is not None:
        choice = message.text.strip()
        goal_type = choices.get(choice)
    if not goal_type:
        await message.answer("❌ Некорректный выбор. Введите от 1 до 5.")
        return

    await state.update_data(goal_type=goal_type)
    if goal_type == "all":
        await message.answer(
            "Введите цели в формате: калории вода сон шаги\nПример: 2500 2.5 8 10000"
        )
    else:
        await message.answer("Введите новое значение:")

    await state.set_state(GoalForm.updating_goal)


@dp.message(GoalForm.updating_goal)
async def handle_goal_update(message: Message, state: FSMContext):
    if message.from_user is not None:
        telegram_id = message.from_user.id
        data = await state.get_data()
        goal_type = data["goal_type"]
    try:
        if goal_type == "all" and message.text is not None:
            # парсим сразу 4 значения
            c, w, s, st = message.text.strip().split()
            payload = {
                "calories_goal": int(c),
                "water_goal": float(w),
                "sleep_goal": float(s),
                "steps_goal": int(st),
            }
        else:
            value = message.text.strip()  # type: ignore
            if goal_type in ["calories_goal", "steps_goal"]:
                value = int(value)
            else:
                value = float(value)
            payload = {goal_type: value}
        result = await update_goals(telegram_id, payload)
        if result is True:
            await message.answer("🎯 Цели обновлены успешно!")
        else:
            await message.answer("❌ Ошибка при обновлении")
    except Exception:
        await message.answer("❌ Ошибка. Убедитесь, что ввели данные правильно.\n")
    await state.clear()
    await message.answer("🔙 Возврат в меню", reply_markup=send_main_menu())
