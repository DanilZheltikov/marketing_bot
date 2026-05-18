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

    step_number: int
    main_post: bool = False
    post_text: str | None
    content_type: str
    file_id: str | None = None


class PostRead(BaseModel):
    """Схема для представления поста."""

    content_type: str
    post_text: str | None
    file_id: str | None

    model_config = ConfigDict(extra='ignore')


class MailingStatsCreate(BaseModel):
    """Схема для создания статистики рассылки в базе."""

    success: int
    cold_users: int
    bot_blocked_users: int


class MailingStatsRead(MailingStatsCreate):
    """Схема для представления рассылки."""

    formatted_date: str

    model_config = ConfigDict(extra='ignore')


class MailingStatsDate(BaseModel):
    """Схема для отображения дат рассылок в базе."""

    id: int
    formatted_date: str
