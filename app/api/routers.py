from fastapi import APIRouter

from app.api import endpoints

main_router = APIRouter()

main_router.include_router(
    endpoints.user_router,
    prefix="/users",
    tags=["users"],
)
main_router.include_router(
    endpoints.auth_router,
    prefix="/auth",
    tags=["auth"],
)

main_router.include_router(
    endpoints.project_router,
    prefix="/charity_project",
    tags=["Charity Project"],
)
main_router.include_router(
    endpoints.donation_router,
    prefix="/donation",
    tags=["Donations"],
)
