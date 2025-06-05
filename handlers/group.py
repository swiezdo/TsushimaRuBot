from aiogram import Router, F
from aiogram.types import ChatMemberUpdated, Message
from database import get_user

router = Router()

@router.chat_member()
async def on_user_join(event: ChatMemberUpdated):
    if event.new_chat_member.status == "member":
        user_id = event.from_user.id
        print(f"Новый участник: {user_id}")

        user = await get_user(user_id)

        if not user:
            try:
                await event.bot.send_message(
                    user_id,
                    "Вы не прошли регистрацию, поэтому были удалены из группы."
                )
            except Exception:
                pass

            try:
                await event.bot.ban_chat_member(event.chat.id, user_id)
                await event.bot.unban_chat_member(event.chat.id, user_id)
            except Exception as e:
                print(f"Не удалось удалить пользователя {user_id}: {e}")
