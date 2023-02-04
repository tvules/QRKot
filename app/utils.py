from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.managers.base import ManagerBase


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
