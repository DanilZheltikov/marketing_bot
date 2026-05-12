import aiosqlite

from core.config import settings

from core.schemas import UserCreate


class UsersRepository:
    """Отвечает за CRUD-операции с сущностью Contact в базе SQLite"""

    def __init__(self, connection: aiosqlite.Connection):
        self.db = connection

    async def add_user(self, user_data: UserCreate) -> None:
        """Сохраняет контакт в базу."""
        await self.db.execute(
            """
            INSERT OR IGNORE INTO users (
                user_id,
                username,
                first_name,
                user_role
            )
            VALUES (
                :user_id,
                :username,
                :first_name,
                :user_role
            )
            """,
            user_data.model_dump()
        )
        await self.db.commit()

    async def set_phone_number(
            self,
            phone_number: str,
            user_id: int
    ) -> None:
        """Добавляет к контакту его номер телефона."""
        await self.db.execute(
            """
            UPDATE users
            SET phone_number = ?
            WHERE user_id = ?
            """,
            (phone_number, user_id)
        )
        await self.db.commit()


async def init_db() -> None:
    """Инициализация таблиц при старте"""
    async with aiosqlite.connect(settings.db_name) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                user_role TEXT,
                phone_number TEXT,
                cold INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS posts (
                step_number INTEGER PRIMARY KEY,
                post_text TEXT NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await db.commit()
