from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    db_name: str
    admin: int


settings = Settings()
