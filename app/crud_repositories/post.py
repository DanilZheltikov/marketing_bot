from core.database import BaseRepository
from core.schemas import PostCreate, PostRead


class PostRepository(BaseRepository):
    """Отвечает за CRUD-операции с сущностью Post в базе SQLite"""

    async def add_post(self, post_data: PostCreate) -> None:
        """Создает пост."""
        await self.db.execute(
            """--sql
            INSERT OR REPLACE INTO posts(
                step_number,
                main_post,
                post_text,
                file_id,
                content_type
            )
            VALUES(
                :step_number,
                :main_post,
                :post_text,
                :file_id,
                :content_type
            )
            """,
            post_data.model_dump()
        )
        await self.db.commit()

    async def get_main_post(self) -> PostRead | None:
        """Возвращает текст поста для главной."""
        async with self.db.execute(
            """--sql
            SELECT *
            FROM posts
            WHERE main_post = 1
            LIMIT 1;
            """
        ) as cursor:
            row = await cursor.fetchone()

            return PostRead(**dict(row)) if row else None

    async def get_warming_post(self, step: int) -> PostRead | None:
        """Возвращает текст поста прогрева по его номеру."""
        async with self.db.execute(
            """--sql
            SELECT *
            FROM posts
            WHERE step_number = ?
            LIMIT 1
            """,
            (step,)
        ) as cursor:
            row = await cursor.fetchone()

            return PostRead(**dict(row)) if row else None

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
