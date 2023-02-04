from operator import eq
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta


class ManagerBase:
    """Base model operations manager."""

    model: Optional[DeclarativeMeta] = None
    create_schema: BaseModel = BaseModel
    update_schema: BaseModel = BaseModel

    def __init__(self, model: DeclarativeMeta = None) -> None:
        if model is not None:
            self.model = model
        assert self.model, "You need to provide the model class"

    async def create(
        self, data: create_schema, *, session: AsyncSession
    ) -> model:
        """Create the object from data."""

        obj = self.model(**data.dict())
        return await self._save(obj, session=session)

    async def get(self, *, session: AsyncSession, **kwargs) -> Optional[model]:
        """Get the object filtered by attrs."""

        objs = await self._filter(session=session, **kwargs)
        return objs.scalars().first()

    async def get_all(self, *, session: AsyncSession) -> List[model]:
        """Get all objects."""

        objs = await self._filter(session=session)
        return objs.scalars().all()

    async def filter(self, *, session: AsyncSession, **kwargs) -> List[model]:
        """Get all objects filtered by attrs."""

        objs = await self._filter(session=session, **kwargs)
        return objs.scalars().all()

    async def update(
        self, obj: model, data: update_schema, *, session: AsyncSession
    ) -> model:
        """Update the object from data."""

        for attr, value in data.dict(exclude_unset=True).items():
            if hasattr(self.model, attr):
                setattr(obj, attr, value)
        return await self._save(obj, session=session)

    async def delete(self, obj: model, *, session: AsyncSession) -> model:
        """Delete the object."""

        return await self._delete(obj, session=session)

    async def _filter(self, *, session: AsyncSession, **kwargs):
        return await session.execute(
            select(self.model).where(
                *(
                    eq(getattr(self.model, attr), value)
                    for attr, value in kwargs.items()
                )
            )
        )

    async def _save(
        self, obj: model, *, refresh: bool = True, session: AsyncSession
    ):
        session.add(obj)
        await session.commit()
        if refresh:
            await session.refresh(obj)
        return obj

    async def _delete(self, obj: model, *, session: AsyncSession):
        await session.delete(obj)
        await session.commit()
        return obj
