from enum import Enum
from typing import Optional

from app.exceptions.base import DoesNotExist


class ProjectErrorDetail(str, Enum):
    """Project errors description."""

    PROJECT_ALREADY_EXISTS = "Проект с таким именем уже существует!"
    PROJECT_CLOSED = "Закрытый проект нельзя редактировать!"
    PROJECT_ALREADY_INVESTED = (
        "В проект были внесены средства, не подлежит удалению!"
    )
    PROJECT_LESS_AMOUNT = (
        "Цель проекта не может быть меньше уже инвестированной суммы."
    )


class ProjectException(Exception):
    """Base Charity project exception."""

    detail: Optional[str] = None

    def __init__(self, detail: Optional[str] = None) -> None:
        if detail is not None:
            self.detail = detail


class ProjectDoesNotExist(DoesNotExist, ProjectException):
    pass


class ProjectAlreadyExists(ProjectException):
    detail: str = ProjectErrorDetail.PROJECT_ALREADY_EXISTS


class ProjectClosed(ProjectException):
    detail: str = ProjectErrorDetail.PROJECT_CLOSED


class ProjectAlreadyInvested(ProjectException):
    detail: str = ProjectErrorDetail.PROJECT_ALREADY_INVESTED


class ProjectLessAmount(ProjectException):
    detail: str = ProjectErrorDetail.PROJECT_LESS_AMOUNT
