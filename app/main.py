import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from core.config import settings
from core.database import init_db
from core.middlewares import DatabaseMiddleware
from handlers.contacts import router as contact_router
from handlers.admin import admin_router


async def main() -> None:
    await init_db()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.update.middleware(DatabaseMiddleware(db_path=settings.db_url))

    dp.include_router(admin_router)
    dp.include_router(contact_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
