from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """Схема для создания пользователя в базе."""

    user_id: int = Field(..., alias='id')
    username: str | None
    first_name: str | None
    user_role: str | None = None

    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class PostCreate(BaseModel):
    """Схема для создания поста в базе."""

    main_post: bool = False
    post_text: str
    step_number: int | None = None


class MailingStatsCreate(BaseModel):
    """Схема для создания статистики рассылки в базе."""

    cold_users: int
    bot_blocked_users: int


class MailingStatsRead(MailingStatsCreate):
    """Схема для представления рассылки."""

    formatted_date: str

    model_config = ConfigDict(extra='ignore')


class MailingStatsDates(BaseModel):
    """Схема для отображения дат рассылок в базе."""

    id: int
    formatted_date: str
