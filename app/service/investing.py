from operator import attrgetter, sub
from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from app.managers.charity_project import charity_project_manager
from app.managers.donation import donation_manager
from app.models.base import InvestModel
from app.utils import close_obj

get_amounts = attrgetter("full_amount", "invested_amount")


async def investing_process(
    _in: InvestModel, _from: Iterable[InvestModel], session: AsyncSession
) -> InvestModel:
    for investment in _from:
        amount = min(sub(*get_amounts(obj)) for obj in (_in, investment))

        _in.invested_amount += amount
        investment.invested_amount += amount

        close_obj(_in, investment)
        session.add_all((_in, investment))

        if _in.fully_invested:
            break

    await session.commit()
    await session.refresh(_in)

    return _in


async def invest_donation(
    donation: InvestModel, session: AsyncSession
) -> InvestModel:
    projects = await charity_project_manager.filter(
        fully_invested=False, session=session
    )
    return await investing_process(donation, projects, session=session)


async def invest_project(
    donation: InvestModel, session: AsyncSession
) -> InvestModel:
    donations = await donation_manager.filter(
        fully_invested=False, session=session
    )
    return await investing_process(donation, donations, session=session)
