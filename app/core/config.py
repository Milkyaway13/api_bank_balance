from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)


class Settings(BaseSettings):
    """
    Конфигурационные настройки приложения.

    Attributes:
        app_title: Название приложения.
        database_url: URL подключения к базе данных.
        secret: Секретный ключ.
        postgres_db: Название базы данных PostgreSQL.

    """

    app_title: str
    database_url: str
    secret: str
    postgres_db: str

    class Config:
        """Мета-настройки для класса Settings"""

        env_file: str = "path/to/.env"
        env_file_encoding: str = "utf-8"
        extra: str = "ignore"


settings = Settings()
