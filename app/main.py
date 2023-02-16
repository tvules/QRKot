from fastapi import FastAPI

from app.api import routers
from app.core.config import settings

app = FastAPI(title=settings.app_title, description=settings.description)

app.include_router(routers.main_router)
