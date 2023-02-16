from datetime import datetime
from typing import Optional, TypeVar

from pydantic import (
    BaseModel,
    Extra,
    Field,
    NonNegativeInt,
    PositiveInt,
    validator,
)

from app.core.config import settings


class ProjectBase(BaseModel):
    """Base schema for the CharityProject model."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            "example": {
                "name": "QRkot",
                "description": "На радости котикам",
                "full_amount": 5000,
            },
        }


class ProjectRead(ProjectBase):
    """Read schema for the CharityProject model."""

    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = ...

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **ProjectBase.Config.schema_extra["example"],
                "invested_amount": 0,
                "fully_invested": False,
                "create_date": settings.start_time,
                "close_date": None,
            },
        }


class ProjectCreate(ProjectBase):
    """Create schema for the CharityProject model."""

    pass


class ProjectUpdate(ProjectBase):
    """Update schema for the CharityProject model."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid

    @validator("name", "description", "full_amount")
    def cannot_be_null(cls, value):
        if value is None:
            raise ValueError("Value cannot be null")
        return value


TProjectCreate = TypeVar("TProjectCreate", bound=ProjectCreate)
TProjectUpdate = TypeVar("TProjectUpdate", bound=ProjectUpdate)
