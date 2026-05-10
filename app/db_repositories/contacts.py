import aiosqlite

from core.schemas import ContactCreate


class ContactsRepository:
    """Отвечает за CRUD-операции с сущностью Contact в базе SQLite"""

    def __init__(self, connection: aiosqlite.Connection):
        self.db = connection

    async def add_contact(self, user_data: ContactCreate) -> None:
        """Сохраняет контакт в базу."""
        await self.db.execute(
            """
            INSERT OR IGNORE INTO contacts (
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

    async def add_phone_number_to_contact(
            self,
            phone_number: str,
            user_id: int
    ) -> None:
        """Добавляет к контакту его номер телефона."""
        await self.db.execute(
            """--sql
            UPDATE contacts
            SET phone_number = ?
            WHERE user_id = ?
            """,
            (phone_number, user_id)
        )
        await self.db.commit()
