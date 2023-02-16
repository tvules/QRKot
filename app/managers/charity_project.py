from datetime import datetime
from typing import Any, Dict, Generic, List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.exceptions.charity_project import (
    ProjectAlreadyExists,
    ProjectAlreadyInvested,
    ProjectClosed,
    ProjectDoesNotExist,
    ProjectLessAmount,
)
from app.managers.base import BaseInvestDatabase
from app.models.charity_project import CharityProject, TProjectModel
from app.schemas.charity_project import (
    ProjectCreate,
    ProjectUpdate,
    TProjectCreate,
    TProjectUpdate,
)


class ProjectDatabase(
    Generic[TProjectModel], BaseInvestDatabase[TProjectModel]
):
    """Charity project SQLAlchemy adapter for database."""

    pass


class ProjectManager(Generic[TProjectModel, TProjectCreate, TProjectUpdate]):
    """Charity project management logic."""

    _project_db: ProjectDatabase

    def __init__(self, project_db: ProjectDatabase) -> None:
        self._project_db = project_db

    async def get(self, **kwargs) -> TProjectModel:
        """Retrieve a project matching the given keyword arguments."""

        project = await self._project_db.get(**kwargs)
        if project is None:
            raise ProjectDoesNotExist

        return project

    async def get_mult(self) -> List[TProjectModel]:
        """Retrieve all projects."""

        return await self._project_db.get_mult()

    async def get_not_invested(self) -> List[TProjectModel]:
        """Retrieve projects which are not fully invested."""

        return await self._project_db.get_not_invested()

    async def create(self, project_create: TProjectCreate) -> TProjectModel:
        """Create a project."""

        await self.is_existing_project(project_create.name)
        return await self._project_db.create(project_create.dict())

    async def update(
        self, project: TProjectModel, project_update: TProjectUpdate
    ) -> TProjectModel:
        """Update a project in database."""

        if project.fully_invested:
            raise ProjectClosed

        return await self._update(
            project, project_update.dict(exclude_unset=True)
        )

    async def delete(self, project: TProjectModel) -> TProjectModel:
        """Delete a project from database."""

        if project.invested_amount:
            raise ProjectAlreadyInvested

        await self._project_db.delete(project)
        return project

    async def is_existing_project(self, name: str) -> None:
        """
        Raise an exception if a project already exists with the same name.
        """

        existing_project = await self._project_db.get(name=name)
        if existing_project:
            raise ProjectAlreadyExists

    async def _update(
        self, project: TProjectModel, update_dict: Dict[str, Any]
    ) -> TProjectModel:
        validated_update_dict = {}
        for field, value in update_dict.items():
            if field == "name" and value != project.name:
                await self.is_existing_project(value)

            elif field == "full_amount":
                if value < project.invested_amount:
                    raise ProjectLessAmount
                elif value == project.invested_amount:
                    validated_update_dict["fully_invested"] = True
                    validated_update_dict["close_date"] = datetime.now()

            validated_update_dict[field] = value
        return await self._project_db.update(project, validated_update_dict)


async def get_project_database(
    session: AsyncSession = Depends(get_async_session),
):
    yield ProjectDatabase[CharityProject](session, CharityProject)


async def get_project_manager(
    project_db: ProjectDatabase = Depends(get_project_database),
):
    yield ProjectManager[CharityProject, ProjectCreate, ProjectUpdate](
        project_db
    )
