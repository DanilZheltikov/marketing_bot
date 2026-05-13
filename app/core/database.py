import aiosqlite

from core.config import settings


class BaseRepository:
    """Базовый репозиторий."""

    def __init__(self, connection: aiosqlite.Connection):
        self.db = connection


async def init_db() -> None:
    """Инициализация таблиц при старте"""
    async with aiosqlite.connect(settings.db_url) as db:
        await db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                user_role TEXT,
                phone_number TEXT,
                pending_stage INTEGER DEFAULT 0,
                cold INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                main_post INTEGER NOT NULL DEFAULT 0,
                step_number INTEGER,
                post_text TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS mailing_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cold_users INTEGER,
                blocked_bot_users INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await db.commit()
