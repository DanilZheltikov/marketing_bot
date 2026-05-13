from core.database import BaseRepository
from core.schemas import PostCreate


class PostRepository(BaseRepository):
    """Отвечает за CRUD-операции с сущностью Post в базе SQLite"""

    async def add_main_post(self, post_data: PostCreate) -> None:
        """Создает пост на главную страницу бота."""
        await self.db.execute(
            """--sql
            INSERT INTO posts(main_post, post_text)
            VALUES(:main_post, :post_text)
            """,
            post_data.model_dump(exclude_none=True)
        )
        await self.db.commit()

    async def add_warming_post(self, post_data: PostCreate) -> None:
        """Создает прогревающий пост для рассылки."""
        await self.db.execute(
            """--sql
            INSERT INTO posts(post_text, step_number)
            VALUES(:post_text, :step_number)
            """,
            post_data.model_dump(exclude_defaults=True)
        )
