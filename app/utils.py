from fastapi import Depends, HTTPException
from starlette import status

from app.core.db import TModel
from app.exceptions.base import DoesNotExist
from app.managers.base import PManager
from app.managers.charity_project import ProjectManager, get_project_manager


async def get_object_or_404(model_manager: PManager, **kwargs) -> TModel:
    """
    Calls get() on a given model manager,
    but it raises HTTPException(404) if object doesn't exist.
    """
    try:
        return await model_manager.get(**kwargs)
    except DoesNotExist:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


async def get_project_by_id_or_404(
    id: int, project_manager: ProjectManager = Depends(get_project_manager)
):
    """Retrieve a project mathing the given ID, or raise HTTPException(404)."""

    return await get_object_or_404(project_manager, id=id)
