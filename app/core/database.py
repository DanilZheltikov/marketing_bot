import aiosqlite

from app.db_repositories.contacts import ContactsRepository
from core.config import settings


class Repositories:
    def __init__(self, db: aiosqlite.Connection):
        self.contacts = ContactsRepository(db)


async def init_db() -> None:
    """Инициализация таблиц при старте"""
    async with aiosqlite.connect(settings.db_name) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                user_role TEXT,
                phone_number TEXT,
                cold INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await db.commit()
