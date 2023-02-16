from pydantic import BaseModel


class DBConfig(BaseModel):
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
