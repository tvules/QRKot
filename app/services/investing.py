from datetime import datetime
from operator import attrgetter, sub
from typing import Iterable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.base import TInvestModel


async def investing(
    obj: TInvestModel,
    _from: Iterable[TInvestModel],
    *,
    session: AsyncSession = Depends(get_async_session)
) -> TInvestModel:
    get_amounts = attrgetter("full_amount", "invested_amount")

    for investment in _from:
        amount = min(sub(*get_amounts(obj)) for obj in (obj, investment))

        obj.invested_amount += amount
        investment.invested_amount += amount

        _close_obj(obj, investment, session=session)

    await session.commit()
    await session.refresh(obj)

    return obj


def _close_obj(*objs: TInvestModel, session: AsyncSession) -> None:
    for obj in objs:
        if obj.invested_amount < obj.full_amount:
            continue
        obj.fully_invested = True
        obj.close_date = datetime.now()
        session.add(obj)
