from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AppConfig(BaseModel):
    app_title: str = "QRKot"
    description: str = "Благотворительный фонд поддержки котиков QRKot"
    start_time: datetime = datetime.now()
    secret: str = "5*i*%w5x!m&rk8ci5mmndj4)w(=rs#d)s=u@!lj+k242l-9v@)"
    first_superuser_email: Optional[str] = None
    first_superuser_password: Optional[str] = None
