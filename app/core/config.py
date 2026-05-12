from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):

    db_url: str = f'{BASE_DIR}/bot.sqlite3'
    bot_token: str
    admin: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8'
    )


settings = Settings()
