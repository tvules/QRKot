from datetime import datetime
from typing import TypeVar

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class InvestBase(Base):
    __abstract__ = True

    full_amount: int = Column(Integer, nullable=False)
    invested_amount: int = Column(Integer, default=0)
    fully_invested: bool = Column(Boolean, default=False)
    create_date: datetime = Column(DateTime, default=datetime.now)
    close_date: datetime = Column(DateTime)


TInvestModel = TypeVar("TInvestModel", bound=InvestBase)
