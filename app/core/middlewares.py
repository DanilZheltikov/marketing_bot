from typing import Any, Awaitable, Callable

import aiosqlite
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from crud_repositories.mailing_stats import MailingStatsRepository
from crud_repositories.post import PostRepository
from crud_repositories.user import UsersRepository


class DatabaseMiddleware(BaseMiddleware):
    """Мидлварь для работы с базой."""

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
            data['post_crud'] = PostRepository(db)
            data['mailing_stats_crud'] = MailingStatsRepository(db)

            return await handler(event, data)


class AdminMiddleware(BaseMiddleware):
    """Мидлварь для ограждения админских хенделреров."""

    def __init__(self, admin_id: int):
        self.admin_id = admin_id

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        user = data.get('event_from_user')

        if not user:
            return

        if user.id != self.admin_id:
            return

        return await handler(event, data)
