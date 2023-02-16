from fastapi import APIRouter

from app.core.user import fastapi_users, jwt_backend
from app.schemas.user import UserCreate, UserRead

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(jwt_backend),
    prefix="/jwt",
)
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
