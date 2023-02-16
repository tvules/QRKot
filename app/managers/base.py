from typing import Generic, List, Protocol, TypeVar

from sqlalchemy.sql.expression import desc

from app.core.db import SQLAlchemyDatabase, TModel
from app.models.base import TInvestModel


class ManagerProtocol(Protocol[TModel]):
    async def get(self, **kwargs) -> TModel:
        ...


PManager = TypeVar("PManager", bound=ManagerProtocol)


class BaseInvestDatabase(
    Generic[TInvestModel], SQLAlchemyDatabase[TInvestModel]
):
    async def get_not_invested(self, *, _desc=False) -> List[TInvestModel]:
        order_column = self.db_table.create_date
        objs = await self._session.execute(
            self._get_equal_statement(fully_invested=False).order_by(
                desc(order_column) if _desc else order_column
            )
        )
        return objs.scalars().all()
