import aiosqlite
from config import DATABASE

class DBFSM:
    @staticmethod
    async def set_state(user_id: int, state: str):
        async with aiosqlite.connect(DATABASE) as db:
            await db.execute(
                "UPDATE users SET state = ? WHERE user_id = ?",
                (state, user_id)
            )
            await db.commit()

    @staticmethod
    async def get_state(user_id: int):
        async with aiosqlite.connect(DATABASE) as db:
            cursor = await db.execute(
                "SELECT state FROM users WHERE user_id = ?",
                (user_id,)
            )
            row = await cursor.fetchone()
            if row:
                return row[0]
            return None
