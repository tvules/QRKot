from fastapi import APIRouter

from .auth import router as auth_router
from .charity_project import router as charity_project_router
from .donation import router as donation_router
from .user import router as user_router

main_router = APIRouter()

main_router.include_router(
    user_router,
    prefix="/users",
    tags=["users"],
)
main_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
)

main_router.include_router(
    charity_project_router,
    prefix="/charity_project",
    tags=["Charity Project"],
)
main_router.include_router(
    donation_router,
    prefix="/donation",
    tags=["Donations"],
)
