from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.charity_project import (
    ClosedProject,
    LessFullAmount,
    NotUniqueProject,
    ProjectAlreadyInvested,
)
from app.managers.base import ManagerBase
from app.models.charity_project import CharityProject


class CharityProjectManager(ManagerBase):
    """Operations manager for the CharityProject model."""

    model = CharityProject

    async def create(
        self, data: Dict[str, Any], *, session: AsyncSession
    ) -> model:
        await self.is_unique_name(data["name"], session=session)
        return await super().create(data, session=session)

    async def update(
        self, obj: model, data: Dict[str, Any], *, session: AsyncSession
    ) -> model:
        if obj.fully_invested:
            raise ClosedProject("Закрытый проект нельзя редактировать!")

        if data.get("name"):
            await self.is_unique_name(data["name"], session=session)

        if data.get("full_amount") and (
            data["full_amount"] < obj.invested_amount
        ):
            raise LessFullAmount(
                "Цель проекта не может быть меньше собранных пожертвований"
            )

        return await super().update(obj, data, session=session)

    async def delete(self, obj: model, *, session: AsyncSession):
        if obj.invested_amount:
            raise ProjectAlreadyInvested(
                "В проект были внесены средства, не подлежит удалению!"
            )
        return await super().delete(obj, session=session)

    async def is_unique_name(self, name, *, session: AsyncSession) -> None:
        if await self.get(name=name, session=session):
            raise NotUniqueProject("Проект с таким именем уже существует!")


charity_project_manager = CharityProjectManager()
