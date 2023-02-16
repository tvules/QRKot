from typing import Generic, List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.exceptions.donation import DonationDoesNotExist
from app.managers.base import BaseInvestDatabase
from app.models.donation import Donation, TDonationModel
from app.models.user import TUserModel, User
from app.schemas.donation import DonationCreate, TDonationCreate


class DonationDatabase(
    Generic[TDonationModel], BaseInvestDatabase[TDonationModel]
):
    """Donation SQLAlchemy adapter for database."""

    pass


class DonationManager(Generic[TDonationModel, TUserModel, TDonationCreate]):
    """Donation management logic."""

    _donation_db: DonationDatabase

    def __init__(self, donation_db: DonationDatabase) -> None:
        self._donation_db = donation_db

    async def get(self, **kwargs) -> TDonationModel:
        """Retrieve a donation matching the given keyword arguments."""

        donation = await self._donation_db.get(**kwargs)
        if donation is None:
            raise DonationDoesNotExist

        return donation

    async def get_mult(self) -> List[TDonationModel]:
        """Retrieve all donations."""

        return await self._donation_db.get_mult()

    async def get_by_user(self, user: TUserModel) -> List[TDonationModel]:
        """Retrieve all donations of the given user."""

        return await self._donation_db.filter(user_id=user.id)

    async def get_not_invested(self) -> List[TDonationModel]:
        """Retrieve donations which are not fully invested."""

        return await self._donation_db.get_not_invested()

    async def create(
        self, user: TUserModel, donation_create: TDonationCreate
    ) -> TDonationModel:
        """Create a donation."""

        create_dict = donation_create.dict(exclude_unset=True)
        create_dict["user_id"] = user.id

        return await self._donation_db.create(create_dict)


async def get_donation_database(
    session: AsyncSession = Depends(get_async_session),
):
    yield DonationDatabase[Donation](session, Donation)


async def get_donation_manager(
    donation_db: DonationDatabase = Depends(get_donation_database),
):
    yield DonationManager[Donation, User, DonationCreate](donation_db)
