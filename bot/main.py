import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.handlers import check

from bot.handlers import menu
from config.settings import settings
from bot.handlers import start
from bot.handlers import admin
from database.db import init_db
from bot.handlers import register
from bot.handlers import admin_requests
from bot.handlers import contests
from bot.handlers import navigation
from bot.handlers import subscribe
from bot.handlers import tokens
from bot.handlers import users
from bot.handlers import statistics

async def main():
    logging.basicConfig(
        level=logging.INFO
    )

    await init_db()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(register.router)
    dp.include_router(menu.router)
    dp.include_router(check.router)
    dp.include_router(admin.router)
    dp.include_router(admin_requests.router)
    dp.include_router(contests.router)
    dp.include_router(navigation.router)
    dp.include_router(subscribe.router)
    dp.include_router(tokens.router)
    dp.include_router(users.router)
    dp.include_router(statistics.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())