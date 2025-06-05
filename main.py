import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from database import init_db
from handlers import register, profile, group

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(message)s"
    )

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    await init_db()

    dp.include_routers(
        register.router,
        profile.router,
        group.router
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
