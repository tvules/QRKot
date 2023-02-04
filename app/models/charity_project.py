from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.db import Base


class CharityProject(Base):
    """Charity project model."""

    id = Column(Integer, primary_key=True)
    name: str = Column(String(length=100), unique=True, nullable=False)
    description: str = Column(Text, nullable=False)
    full_amount: int = Column(Integer, nullable=False)
    invested_amount: int = Column(Integer, default=0)
    fully_invested: bool = Column(Boolean, default=False)
    create_date: datetime = Column(DateTime, default=datetime.now)
    close_date: datetime = Column(DateTime)
