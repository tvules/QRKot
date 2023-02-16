import re
from typing import AsyncGenerator, Union

from fastapi import Depends
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    InvalidPasswordException,
    models,
    schemas,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.user import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self, password: str, user: Union[schemas.UC, models.UP]
    ) -> None:
        if not re.fullmatch(r"\w{3,}", password):
            raise InvalidPasswordException(
                "Password should be at least 3 characters"
            )


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)
