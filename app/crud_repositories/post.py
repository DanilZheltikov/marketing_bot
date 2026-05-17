from core.database import BaseRepository
from core.schemas import PostCreate


class PostRepository(BaseRepository):
    """Отвечает за CRUD-операции с сущностью Post в базе SQLite"""

    async def add_post(self, post_data: PostCreate) -> None:
        """Создает пост."""
        await self.db.execute(
            """--sql
            INSERT OR REPLACE INTO posts(main_post, post_text, step_number)
            VALUES(:main_post, :post_text, :step_number)
            """,
            post_data.model_dump()
        )
        await self.db.commit()

    async def get_main_post(self) -> str | None:
        """Возвращает текст поста для главной."""
        async with self.db.execute(
            """--sql
            SELECT post_text
            FROM posts
            WHERE main_post = 1
            LIMIT 1;
            """
        ) as cursor:
            row = await cursor.fetchone()

            return row['post_text'] if row else None

    async def get_warming_post(self, step: int) -> str | None:
        """Возвращает текст поста прогрева по его номеру."""
        async with self.db.execute(
            """--sql
            SELECT post_text
            FROM posts
            WHERE step_number = ?
            LIMIT 1
            """,
            (step,)
        ) as cursor:
            row = await cursor.fetchone()

            return row['post_text'] if row else None

    async def remove_main_post(self) -> None:
        """Удаляет пост главной страницы."""
        await self.db.execute(
            """--sql
            DELETE FROM posts
            WHERE main_post = 1
            """
        )
        await self.db.commit()

    async def remove_warming_post(self, step: int) -> None:
        """Удаляет прогревающий пост по его номеру."""
        await self.db.execute(
            """--sql
            DELETE FROM posts
            WHERE step_number = ?
            """,
            (step,)
        )
        await self.db.commit()
