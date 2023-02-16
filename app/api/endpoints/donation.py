from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.managers.charity_project import ProjectManager, get_project_manager
from app.managers.donation import DonationManager, get_donation_manager
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationRead, DonationReadAll
from app.services import investing

router = APIRouter()


@router.get(
    "/",
    response_model=List[DonationReadAll],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    donation_manager: DonationManager = Depends(get_donation_manager),
):
    return await donation_manager.get_mult()


@router.post(
    "/",
    response_model=DonationRead,
    response_model_exclude_none=True,
)
async def create_donation(
    donation_create: DonationCreate,
    user: User = Depends(current_user),
    donation_manager: DonationManager = Depends(get_donation_manager),
    project_manager: ProjectManager = Depends(get_project_manager),
    session: AsyncSession = Depends(get_async_session),
):
    donation = await donation_manager.create(user, donation_create)
    not_invested_projects = await project_manager.get_not_invested()
    return await investing(donation, not_invested_projects, session=session)


@router.get(
    "/my",
    response_model=List[DonationRead],
    response_model_exclude_none=True,
)
async def get_user_donations(
    user: User = Depends(current_user),
    donation_manager: DonationManager = Depends(get_donation_manager),
):
    return await donation_manager.get_by_user(user)
