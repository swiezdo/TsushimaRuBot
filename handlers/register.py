# handlers/register.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards import start_keyboard, platform_keyboard, modes_keyboard, goals_keyboard, level_keyboard, after_register_keyboard
from database import add_user, update_user, get_user
from utils.db_fsm import DBFSM

router = Router()

# Состояния
class States:
    START = "start"
    NAME = "name"
    PSN_ID = "psn_id"
    PLATFORM = "platform"
    MODES = "modes"
    GOALS = "goals"
    LEVEL = "level"
    COMPLETE = "complete"
    PROFILE = "profile"

# Маппинги
platform_mapping = {
    "pc": "ПК",
    "playstation": "PlayStation",
}

mode_mapping = {
    "story": "Сюжет",
    "survival": "Выживание",
    "trials": "Испытания Иё",
    "chapters": "Главы",
}

goal_mapping = {
    "trophies": "Получение трофеев",
    "learn": "Узнать что-то новое",
    "teammates": "Поиск тиммейтов",
}

level_mapping = {
    "bronze": "Бронза",
    "silver": "Серебро",
    "gold": "Золото",
    "platinum": "Платина",
    "nightmare": "Кошмар",
    "hell": "HellMode",
}

async def edit_or_send(bot, user_id, text, reply_markup=None):
    user = await get_user(user_id)
    message_id = user[7]  # message_id
    if message_id:
        try:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=text,
                reply_markup=reply_markup
            )
        except Exception:
            msg = await bot.send_message(user_id, text=text, reply_markup=reply_markup)
            await update_user(user_id, "message_id", msg.message_id)
    else:
        msg = await bot.send_message(user_id, text=text, reply_markup=reply_markup)
        await update_user(user_id, "message_id", msg.message_id)

async def clear_registration_fields(user_id: int):
    fields_to_clear = ["name", "psn_id", "platform", "modes", "goals", "level"]
    for field in fields_to_clear:
        await update_user(user_id, field, None)

@router.message(Command("start"))
async def cmd_start(message: Message):
    await add_user(message.from_user.id)
    await DBFSM.set_state(message.from_user.id, States.START)
    await edit_or_send(message.bot, message.from_user.id,
                       "Привет! Чтобы вступить в сообщество Tsushima.ru, необходимо пройти небольшую регистрацию. После завершения вы получите ссылку для вступления в группу.",
                       reply_markup=start_keyboard())
    await message.delete()

@router.callback_query(F.data == "start_registration")
async def start_registration(callback: CallbackQuery):
    await clear_registration_fields(callback.from_user.id)  # Очищаем данные при начале регистрации
    await DBFSM.set_state(callback.from_user.id, States.NAME)
    await edit_or_send(callback.bot, callback.from_user.id, "Введите ваше имя:")
    await callback.answer()

@router.message()
async def handle_text(message: Message):
    await message.delete()
    user_id = message.from_user.id
    state = await DBFSM.get_state(user_id)

    if state == States.NAME:
        await update_user(user_id, "name", message.text)
        await DBFSM.set_state(user_id, States.PSN_ID)
        await edit_or_send(message.bot, user_id, "Введите ваш PSN ID:")
    elif state == States.PSN_ID:
        await update_user(user_id, "psn_id", message.text)
        await DBFSM.set_state(user_id, States.PLATFORM)
        await edit_or_send(message.bot, user_id, "Выберите платформу:", reply_markup=platform_keyboard())

@router.callback_query(F.data.startswith("platform_"))
async def choose_platform(callback: CallbackQuery):
    key = callback.data.split("_", 1)[1]
    platform = platform_mapping.get(key, key)
    await update_user(callback.from_user.id, "platform", platform)
    await DBFSM.set_state(callback.from_user.id, States.MODES)
    await edit_or_send(callback.bot, callback.from_user.id, "Выберите режимы игры (несколько вариантов):", reply_markup=modes_keyboard())
    await callback.answer()

@router.callback_query(F.data.startswith("mode_"))
async def choose_modes(callback: CallbackQuery):
    if callback.data == "mode_done":
        await DBFSM.set_state(callback.from_user.id, States.GOALS)
        await edit_or_send(callback.bot, callback.from_user.id, "Выберите цели участия (несколько вариантов):", reply_markup=goals_keyboard())
        await callback.answer()
        return

    user = await get_user(callback.from_user.id)
    current_modes = user[4] or ""
    key = callback.data.split("_", 1)[1]
    new_mode = mode_mapping.get(key, key)

    modes_list = [m.strip() for m in current_modes.split(", ") if m.strip()]
    if new_mode not in modes_list:
        modes_list.append(new_mode)

    updated_modes = ", ".join(modes_list)

    await update_user(callback.from_user.id, "modes", updated_modes)
    await callback.answer("Добавлено!")

@router.callback_query(F.data.startswith("goal_"))
async def choose_goals(callback: CallbackQuery):
    if callback.data == "goal_done":
        await DBFSM.set_state(callback.from_user.id, States.LEVEL)
        await edit_or_send(callback.bot, callback.from_user.id, "Выберите уровень сложности:", reply_markup=level_keyboard())
        await callback.answer()
        return

    user = await get_user(callback.from_user.id)
    current_goals = user[5] or ""
    key = callback.data.split("_", 1)[1]
    new_goal = goal_mapping.get(key, key)

    goals_list = [g.strip() for g in current_goals.split(", ") if g.strip()]
    if new_goal not in goals_list:
        goals_list.append(new_goal)

    updated_goals = ", ".join(goals_list)

    await update_user(callback.from_user.id, "goals", updated_goals)
    await callback.answer("Добавлено!")

@router.callback_query(F.data.startswith("level_"))
async def choose_level(callback: CallbackQuery):
    if callback.data == "level_done":
        await DBFSM.set_state(callback.from_user.id, States.COMPLETE)
        await edit_or_send(callback.bot, callback.from_user.id, "Спасибо, Вы успешно зарегистрировались!", reply_markup=after_register_keyboard())
        await callback.answer()
        return

    user = await get_user(callback.from_user.id)
    current_levels = user[6] or ""
    key = callback.data.split("_", 1)[1]
    new_level = level_mapping.get(key, key)

    levels_list = [l.strip() for l in current_levels.split(", ") if l.strip()]
    if new_level not in levels_list:
        levels_list.append(new_level)

    updated_levels = ", ".join(levels_list)

    await update_user(callback.from_user.id, "level", updated_levels)
    await callback.answer("Добавлено!")
