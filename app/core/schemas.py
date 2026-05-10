from pydantic import BaseModel, ConfigDict, Field


class ContactCreate(BaseModel):
    user_id: int = Field(..., alias='id')
    username: str | None
    first_name: str | None
    user_role: str | None = None

    model_config = ConfigDict(populate_by_name=True, extra='ignore')
