import aiosqlite
from config import DATABASE

async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                psn_id TEXT,
                platform TEXT,
                modes TEXT,
                goals TEXT,
                level TEXT,
                message_id INTEGER,
                state TEXT
            )
        """)
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return await cursor.fetchone()

async def add_user(user_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def update_user(user_id: int, field: str, value):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(f"UPDATE users SET {field} = ? WHERE user_id = ?", (value, user_id))
        await db.commit()

async def delete_user(user_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        await db.commit()

async def get_all_users():
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute("SELECT user_id FROM users")
        rows = await cursor.fetchall()
        return rows        