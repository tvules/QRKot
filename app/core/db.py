from operator import eq
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
)

from sqlalchemy import Column, Integer, MetaData, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
Base = declarative_base(cls=PreBase, metadata=meta)
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

TModel = TypeVar("TModel", bound=Base)


class SQLAlchemyDatabase(Generic[TModel]):
    """Base SQLAlchemy adapter for database."""

    def __init__(self, session: AsyncSession, db_table: Type[TModel]) -> None:
        self._session = session
        self.db_table = db_table

    async def get(self, **kwargs) -> Optional[TModel]:
        objs = await self._session.execute(self._get_equal_statement(**kwargs))
        return objs.scalars().first()

    async def get_mult(self) -> List[TModel]:
        objs = await self._session.execute(select(self.db_table))
        return objs.scalars().all()

    async def filter(self, **kwargs) -> List[TModel]:
        objs = await self._session.execute(self._get_equal_statement(**kwargs))
        return objs.scalars().all()

    async def create(self, create_dict: Dict[str, Any]) -> TModel:
        obj = self.db_table(**create_dict)
        return await self.save(obj, refresh=True)

    async def update(self, obj: TModel, update_dict: Dict[str, Any]) -> TModel:
        for key, value in update_dict.items():
            setattr(obj, key, value)
        return await self.save(obj, refresh=True)

    async def delete(self, obj: TModel) -> None:
        await self._session.delete(obj)
        await self._session.commit()

    async def save(self, obj: TModel, *, refresh: bool = True) -> TModel:
        self._session.add(obj)
        await self._session.commit()
        if refresh:
            await self._session.refresh(obj)
        return obj

    def _get_equal_statement(self, **kwargs):
        return select(self.db_table).where(
            *(
                eq(getattr(self.db_table, attr), value)
                for attr, value in kwargs.items()
            ),
        )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as async_session:
        try:
            yield async_session
        except Exception:
            await async_session.rollback()
            raise
