from core.database import BaseRepository
from core.schemas import UserCreate


class UsersRepository(BaseRepository):
    """Отвечает за CRUD-операции с сущностью User в базе SQLite"""

    async def add_user(self, user_data: UserCreate) -> None:
        """Сохраняет пользователя в базу."""
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
        """Добавляет к пользователю его номер телефона."""
        await self.db.execute(
            """
            UPDATE users
            SET phone_number = ?
            WHERE user_id = ?
            """,
            (phone_number, user_id)
        )
        await self.db.commit()
