from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.exceptions.charity_project import CharityProjectException
from app.managers.charity_project import charity_project_manager
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectRead,
    CharityProjectUpdate,
)
from app.utils import get_object_or_404

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectRead],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_manager.get_all(session=session)


@router.post(
    "/",
    response_model=CharityProjectRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await charity_project_manager.create(
            project.dict(), session=session
        )
    except CharityProjectException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.reason
        )


@router.patch(
    "/{project_id}",
    response_model=CharityProjectRead,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    project: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        obj = await get_object_or_404(
            charity_project_manager, session=session, id=project_id
        )
        return await charity_project_manager.update(
            obj, project.dict(exclude_unset=True), session=session
        )
    except CharityProjectException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.reason
        )


@router.delete(
    "/{project_id}",
    response_model=CharityProjectRead,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        project = await get_object_or_404(
            charity_project_manager, session=session, id=project_id
        )
        return await charity_project_manager.delete(project, session=session)
    except CharityProjectException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.reason
        )
