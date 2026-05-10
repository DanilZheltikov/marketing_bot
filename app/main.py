import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from core.config import settings
from core.database import init_db
from core.midlewares import DatabaseMiddleware
from handlers.contacts import router as contact_router


async def main() -> None:
    await init_db()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.update.middleware(DatabaseMiddleware(db_path=settings.db_name))
    dp.include_router(contact_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
