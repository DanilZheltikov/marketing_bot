from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    db_name: str
    db_path: str
    admin: int


settings = Settings()
