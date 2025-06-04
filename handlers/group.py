# handlers/group.py

from aiogram import Router
from aiogram.types import ChatMemberUpdated
from database import get_user

router = Router()

# Обработка новых участников
@router.chat_member()
async def on_user_join(event: ChatMemberUpdated):
    # Проверяем только новых участников
    if event.new_chat_member.status == "member":
        user_id = event.from_user.id
        user = await get_user(user_id)

        if not user:
            try:
                # Пишем в личку пользователю
                await event.bot.send_message(
                    user_id,
                    "Вы не прошли регистрацию, поэтому были удалены из группы."
                )
            except Exception:
                # Возможно, пользователь запретил ЛС боту — молча проглотим ошибку
                pass

            # Кикаем из группы
            try:
                await event.bot.ban_chat_member(event.chat.id, user_id)
                await event.bot.unban_chat_member(event.chat.id, user_id)
            except Exception as e:
                print(f"Не удалось удалить пользователя {user_id}: {e}")
