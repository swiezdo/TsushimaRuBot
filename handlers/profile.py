from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from keyboards import after_register_keyboard, back_to_main_keyboard, start_keyboard
from database import get_user, update_user
from utils.db_fsm import DBFSM
from handlers.register import States

router = Router()

async def edit_or_send(bot, user_id, text, reply_markup=None):
    user = await get_user(user_id)
    message_id = user[7]
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

def format_field_single(value: str) -> str:
    if not value or value.strip() == "":
        return "Не заполнено 🚫"
    return value.strip()

def format_field_dynamic(label: str, value: str) -> str:
    if not value or value.strip() == "":
        return f"{label}: Не заполнено 🚫"
    items = [v.strip() for v in value.split(",") if v.strip()]
    if len(items) == 1:
        return f"{label}: {items[0]}"
    else:
        formatted_items = "\n".join(f"- {item}" for item in items)
        return f"{label}:\n{formatted_items}"

@router.callback_query(F.data == "view_profile")
async def view_profile(callback: CallbackQuery):
    await DBFSM.set_state(callback.from_user.id, States.PROFILE)
    user = await get_user(callback.from_user.id)
    if user:
        name = format_field_single(user[1])
        psn_id = format_field_single(user[2])
        platform = format_field_single(user[3])
        modes = format_field_dynamic("🕹️ Режимы", user[4])
        goals = format_field_dynamic("🎯 Цели", user[5])
        levels = format_field_dynamic("🏆 Сложности", user[6])

        profile_text = (
            "━━━━━━━━━━━━━━━\n"
            f"🧑 Имя: {name}\n"
            f"🎮 PSN: {psn_id}\n"
            f"🖥️ Платформа: {platform}\n"
            f"{modes}\n"
            f"{goals}\n"
            f"{levels}\n"
            "━━━━━━━━━━━━━━━"
        )
    else:
        profile_text = "Профиль не найден."

    await edit_or_send(callback.bot, callback.from_user.id, profile_text, reply_markup=back_to_main_keyboard())
    await callback.answer()

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await DBFSM.set_state(callback.from_user.id, States.COMPLETE)
    await edit_or_send(callback.bot, callback.from_user.id, "Спасибо, Вы успешно зарегистрировались!", reply_markup=after_register_keyboard())
    await callback.answer()

@router.callback_query(F.data == "start_over")
async def start_over(callback: CallbackQuery):
    await DBFSM.set_state(callback.from_user.id, States.START)
    await edit_or_send(callback.bot, callback.from_user.id,
                       "Привет! Чтобы вступить в сообщество Tsushima.ru, необходимо пройти небольшую регистрацию. После завершения вы получите ссылку для вступления в группу.",
                       reply_markup=start_keyboard())
    await callback.answer()

@router.message(F.text == "!п")
async def profile_by_command(message: Message):
    # Определяем на кого смотрим: если reply — берем пользователя из reply
    if message.reply_to_message:
        target_user_id = message.reply_to_message.from_user.id
    else:
        target_user_id = message.from_user.id

    user = await get_user(target_user_id)

    if user:
        name = user[1] or "Не указано"
        psn_id = user[2] or "Не указано"
        platform = user[3] or "Не указано"
        modes = user[4] or "Не указано"
        goals = user[5] or "Не указано"
        level = user[6] or "Не указано"

        profile_text = (
            "━━━━━━━━━━━━━━━\n"
            f"🧑 Имя: {name}\n"
            f"🎮 PSN: {psn_id}\n"
            f"🖥️ Платформа: {platform}\n"
            f"🕹️ Режимы: {modes}\n"
            f"🎯 Цели: {goals}\n"
            f"🏆 Сложности: {level}\n"
            "━━━━━━━━━━━━━━━"
        )
    else:
        profile_text = "Пользователь не зарегистрирован."

    try:
        # Делаем ответ reply на "!п"
        await message.reply(profile_text)
    except Exception as e:
        print(f"Ошибка при отправке профиля: {e}")