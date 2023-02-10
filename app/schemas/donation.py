from datetime import datetime
from typing import Optional

from pydantic import BaseModel, NonNegativeInt, PositiveInt

from app.core.config import settings


class DonationBase(BaseModel):
    """Base schema for the Donation model."""

    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "full_amount": 2000,
                "comment": "QRKot",
            },
        }


class DonationCreate(DonationBase):
    """Create schema for the Donation model."""

    pass


class DonationRead(DonationBase):
    """Read schema for the Donation model."""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                **DonationBase.Config.schema_extra["example"],
                "id": 1,
                "create_date": settings.start_time.isoformat(
                    timespec="seconds"
                ),
            },
        }


class DonationReadAll(DonationRead):
    """Read(all fields) schema for the Donation model."""

    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
                **DonationRead.Config.schema_extra["example"],
                "user_id": 1,
                "invested_amount": 100,
                "fully_invested": False,
                "close_date": None,
            },
        }
