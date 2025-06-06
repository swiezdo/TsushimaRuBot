from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from database import get_all_users, delete_user
from aiogram.exceptions import TelegramBadRequest

router = Router()

def plural_form(n, form1, form2, form5):
    n = abs(n) % 100
    n1 = n % 10
    if 10 < n < 20:
        return form5
    if 1 < n1 < 5:
        return form2
    if n1 == 1:
        return form1
    return form5

async def is_admin(bot, chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except TelegramBadRequest:
        return False

@router.message(Command("clean"), F.chat.type.in_({"group", "supergroup"}))
async def clean_inactive_users(message: Message):
    bot = message.bot
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Проверка — админ ли пользователь
    if not await is_admin(bot, chat_id, user_id):
        await message.reply("❌ У вас нет прав для выполнения этой команды.")
        return

    users = await get_all_users()
    if not users:
        await message.reply("База данных пуста. Нет анкет для проверки.")
        return

    deleted_count = 0
    for user in users:
        user_id_in_db = user[0]
        try:
            member = await bot.get_chat_member(chat_id, user_id_in_db)
            if member.status in ["left", "kicked"]:
                await delete_user(user_id_in_db)
                deleted_count += 1
        except TelegramBadRequest:
            await delete_user(user_id_in_db)
            deleted_count += 1

    if deleted_count == 0:
        await message.reply("✅ Все анкеты актуальны. Ничего не удалено.")
    else:
        word = plural_form(deleted_count, "анкета", "анкеты", "анкет")
        await message.reply(f"✅ Успех! Удалено {deleted_count} {word}.")
