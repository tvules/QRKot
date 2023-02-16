from typing import TypeVar

from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import InvestBase


class Donation(InvestBase):
    """Donation model."""

    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)


TDonationModel = TypeVar("TDonationModel", bound=Donation)
