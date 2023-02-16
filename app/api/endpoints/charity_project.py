from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.exceptions.charity_project import (
    ProjectAlreadyExists,
    ProjectAlreadyInvested,
    ProjectClosed,
    ProjectLessAmount,
)
from app.managers.charity_project import ProjectManager, get_project_manager
from app.managers.donation import DonationManager, get_donation_manager
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
)
from app.services import investing
from app.utils import get_project_by_id_or_404

router = APIRouter()


@router.get(
    "/",
    response_model=List[ProjectRead],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    project_manager: ProjectManager = Depends(get_project_manager),
):
    return await project_manager.get_mult()


@router.post(
    "/",
    response_model=ProjectRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    project_create: ProjectCreate,
    project_manager: ProjectManager = Depends(get_project_manager),
    donation_manager: DonationManager = Depends(get_donation_manager),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        project = await project_manager.create(project_create)
    except ProjectAlreadyExists as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=exc.detail)
    else:
        not_invested_donations = await donation_manager.get_not_invested()
        return await investing(
            project, not_invested_donations, session=session
        )


@router.patch(
    "/{id}",
    response_model=ProjectRead,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_update: ProjectUpdate,
    project: CharityProject = Depends(get_project_by_id_or_404),
    project_manager: ProjectManager = Depends(get_project_manager),
    donation_manager: DonationManager = Depends(get_donation_manager),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        project = await project_manager.update(project, project_update)
    except (ProjectClosed, ProjectAlreadyExists, ProjectLessAmount) as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=exc.detail)
    else:
        not_invested_donations = await donation_manager.get_not_invested()
        return await investing(
            project, not_invested_donations, session=session
        )


@router.delete(
    "/{id}",
    response_model=ProjectRead,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project: CharityProject = Depends(get_project_by_id_or_404),
    project_manager: ProjectManager = Depends(get_project_manager),
):
    try:
        return await project_manager.delete(project)
    except ProjectAlreadyInvested as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=exc.detail)
