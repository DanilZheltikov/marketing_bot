from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    user_id: int = Field(..., alias='id')
    username: str | None
    first_name: str | None
    user_role: str | None = None

    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class PostCreate(BaseModel):
    main_post: bool = False
    post_text: str
    step_number: int | None = None


class MailingStatsCreate(BaseModel):
    cold_users: int
    bot_blocked_users: int


class MailingStatsRead(MailingStatsCreate):
    formatted_date: str

    model_config = ConfigDict(extra='ignore')
