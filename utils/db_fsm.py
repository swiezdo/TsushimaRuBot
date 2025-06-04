# utils/db_fsm.py

from database import update_user, get_user

class DBFSM:
    @staticmethod
    async def set_state(user_id: int, state: str):
        await update_user(user_id, "state", state)

    @staticmethod
    async def get_state(user_id: int):
        user = await get_user(user_id)
        if user:
            return user[-1]  # Поле state — последнее в таблице
        return None
