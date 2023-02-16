from typing import TypeVar

from sqlalchemy import Column, String, Text

from app.models.base import InvestBase


class CharityProject(InvestBase):
    """Charity project model."""

    name: str = Column(String(length=100), unique=True, nullable=False)
    description: str = Column(Text, nullable=False)


TProjectModel = TypeVar("TProjectModel", bound=CharityProject)
