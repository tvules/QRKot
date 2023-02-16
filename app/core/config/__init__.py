from pydantic import BaseSettings

from .app import AppConfig
from .db import DBConfig

__all__ = [
    "settings",
]


class Settings(AppConfig, DBConfig, BaseSettings):
    class Config:
        env_file = ".env"


settings = Settings()
