from core.database import BaseRepository
from core.schemas import (
    MailingStatsCreate,
    MailingStatsDate,
    MailingStatsRead
)


class MailingStatsRepository(BaseRepository):
    """Отвечает за CRUD-операции с сущностью MailingStats в базе SQLite"""

    async def add_mailing_stats(
        self,
        mailing_stats_data: MailingStatsCreate
    ) -> None:
        """Добавляет статистику рассылок в базу."""
        await self.db.execute(
            """--sql
            INSERT INTO mailing_stats(cold_users, blocked_bot_users, success)
            VALUES (:cold_users, :blocked_bot_users, :success)
            """,
            mailing_stats_data.model_dump()
        )
        await self.db.commit()

    async def get_dates_from_mailing_stats(self) -> list[MailingStatsDate]:
        """Возвращает список словарей с ID и отформатированной датой."""
        async with self.db.execute(
            """--sql
            SELECT
                id,
                strftime('%d.%m.%Y в %H:%M', created_at) as formatted_date
            FROM mailing_stats
            ORDER BY created_at DESC;
            """
        ) as cursor:
            rows = await cursor.fetchall()

            return [MailingStatsDate(**dict(row)) for row in rows]

    async def get_mailing_stats(
        self,
        mailing_stats_id: int
    ) -> MailingStatsRead | None:
        async with self.db.execute(
            """--sql
            SELECT
                success,
                cold_users,
                blocked_bot_users,
                strftime('%d.%m.%Y в %H:%M', created_at) as formatted_date
            FROM mailing_stats
            WHERE id = ?
            LIMIT 1;
            """,
            (mailing_stats_id,)
        ) as cursor:
            row = await cursor.fetchone()

            return MailingStatsRead(**dict(row)) if row else None
