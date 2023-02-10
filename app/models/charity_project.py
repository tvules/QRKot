from sqlalchemy import Column, String, Text

from app.models.base import InvestedBase


class CharityProject(InvestedBase):
    """Charity project model."""

    name: str = Column(String(length=100), unique=True, nullable=False)
    description: str = Column(Text, nullable=False)
