from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.managers.donation import donation_manager
from app.models import User
from app.schemas.donation import DonationCreate, DonationRead, DonationReadAll
from app.service.investing import invest_donation
from app.utils import set_user_id

router = APIRouter()


@router.get(
    "/",
    response_model=List[DonationReadAll],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_manager.get_all(session=session)


@router.post(
    "/",
    response_model=DonationRead,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    data = donation.dict()
    set_user_id(data, user)
    donation = await donation_manager.create(data, session=session)
    return await invest_donation(donation, session=session)


@router.get(
    "/my",
    response_model=List[DonationRead],
    response_model_exclude_none=True,
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_manager.filter(user_id=user.id, session=session)
