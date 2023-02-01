from typing import Optional

from pydantic import BaseModel


class AppConfig(BaseModel):
    app_title: str = "QRKot"
    description: str = "Благотворительный фонд поддержки котиков QRKot"
    secret: str
    first_superuser_email: Optional[str] = None
    first_superuser_password: Optional[str] = None
