from datetime import datetime
from typing import MutableMapping, Union

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.managers.base import ManagerBase
from app.models import User
from app.models.base import InvestModel


async def get_object_or_404(
    model_manager: ManagerBase, *, session: AsyncSession, **kwargs
):
    """Calls get() on a given model manager,
    but it raises HTTPException(404) if object doesn't exist.
    """

    obj = await model_manager.get(session=session, **kwargs)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return obj


def set_user_id(
    data: MutableMapping, user: Union[User, int], *, to_key: str = "user_id"
) -> None:
    """Sets a user ID in the received data."""

    if isinstance(user, User):
        data[to_key] = user.id
    else:
        data[to_key] = user


def close_obj(*objs: InvestModel) -> None:
    """Closes an object if it's fully invested."""

    for obj in objs:
        if obj.invested_amount < obj.full_amount:
            continue
        obj.fully_invested = True
        obj.close_date = datetime.now()
