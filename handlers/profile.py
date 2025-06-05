import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from keyboards import after_register_keyboard, back_to_main_keyboard, start_keyboard
from database import get_user, update_user
from utils.db_fsm import DBFSM
from handlers.register import States

router = Router()

async def edit_or_send(bot, user_id, text, reply_markup=None):
    user = await get_user(user_id)
    if not user:
        # Если пользователя нет — просто отправить новое сообщение
        msg = await bot.send_message(user_id, text=text, reply_markup=reply_markup)
        return

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
        return "Не заполнено"
    return value.strip()

def format_field_dynamic(label: str, value: str) -> str:
    if not value or value.strip() == "":
        return f"{label}: Не заполнено"
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

    if user and user[1] and user[2]:  # user[1] — имя, user[2] — psn_id
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
        await edit_or_send(callback.bot, callback.from_user.id, profile_text, reply_markup=back_to_main_keyboard())
        await callback.answer()

    else:
        # Тут ПРАВИЛЬНАЯ логика обработки ошибки
        # Создаём новое сообщение об ошибке
        msg = await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text="❌ Произошла ошибка. Пожалуйста, пройдите регистрацию заново."
        )
        # Сохраняем новый message_id
        await update_user(callback.from_user.id, "message_id", msg.message_id)

        # Переводим в START
        await DBFSM.set_state(callback.from_user.id, States.START)

        await callback.answer()

        # Ждём 3 секунды
        await asyncio.sleep(3)

        # Редактируем сообщение в "стартовое"
        try:
            await callback.bot.edit_message_text(
                chat_id=callback.from_user.id,
                message_id=msg.message_id,
                text="Привет! Чтобы вступить в сообщество Tsushima\u2060.Ru, необходимо пройти небольшую регистрацию. После завершения вы получите ссылку для вступления в группу.",
                reply_markup=start_keyboard()
            )
        except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")

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
    if message.reply_to_message:
        target_user_id = message.reply_to_message.from_user.id
    else:
        target_user_id = message.from_user.id

    user = await get_user(target_user_id)

    if user and user[1] and user[2]:  # user[1] — имя, user[2] — psn_id
        name = user[1]
        psn_id = user[2]
        platform = user[3] or "Не заполнено"
        modes = user[4] or "Не заполнено"
        goals = user[5] or "Не заполнено"
        level = user[6] or "Не заполнено"

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
        await message.reply(profile_text)
    else:
        if user:
            from database import delete_user
            await delete_user(target_user_id)  # ❗ Удаляем кривую анкету

        try:
            await message.reply("❌ Пользователь не зарегистрирован или регистрация некорректна.")
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
