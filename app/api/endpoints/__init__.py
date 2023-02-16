from .auth import router as auth_router
from .charity_project import router as project_router
from .donation import router as donation_router
from .user import router as user_router

__all__ = [
    "auth_router",
    "project_router",
    "donation_router",
    "user_router",
]
