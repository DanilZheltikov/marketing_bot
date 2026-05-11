from typing import Any, Awaitable, Callable

import aiosqlite
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from core.database import UsersRepository


class DatabaseMiddleware(BaseMiddleware):

    def __init__(self, db_path: str):
        self.db_path = db_path

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            data['user_crud'] = UsersRepository(db)
            return await handler(event, data)
