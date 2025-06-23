from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

router = Router()

async def is_admin(bot, chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except TelegramBadRequest:
        return False

@router.message(F.text.startswith("!кто"), F.chat.type.in_({"group", "supergroup"}))
async def whois_command(message: Message):
    bot = message.bot
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    # Проверяем админ или владелец
    if not await is_admin(bot, chat_id, from_user_id):
        await message.reply("❌ У вас нет прав для использования этой команды.")
        return

    parts = message.text.split()

    if len(parts) != 2:
        await message.reply("❌ Пожалуйста, укажите ID пользователя.\nПример: `!кто 123456789`", parse_mode="Markdown")
        return

    try:
        user_id = int(parts[1])
    except ValueError:
        await message.reply("❌ Неверный формат ID. Укажите числовой ID.")
        return

    try:
        member = await bot.get_chat_member(chat_id, user_id)
        user = member.user

        if user.username:
            name = f"@{user.username}"
        else:
            # Склеим имя и фамилию, если фамилия есть
            name = user.first_name
            if user.last_name:
                name += f" {user.last_name}"

        await message.reply(f"✅ Найден: {name}")
    except TelegramBadRequest:
        await message.reply("❌ Пользователь не найден или недоступен.")
