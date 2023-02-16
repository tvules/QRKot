from fastapi import APIRouter, HTTPException, status

from app.core.user import fastapi_users
from app.schemas.user import UserRead, UserUpdate

router = APIRouter()

router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))


@router.delete("/{id}", tags=["users"], deprecated=True)
async def delete_user(id: int):
    raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED)
