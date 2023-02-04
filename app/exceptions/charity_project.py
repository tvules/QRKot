from typing import Any


class CharityProjectException(Exception):
    def __init__(self, reason: Any) -> None:
        self.reason = reason


class ProjectAlreadyInvested(CharityProjectException):
    pass


class NotUniqueProject(CharityProjectException):
    pass


class LessFullAmount(CharityProjectException):
    pass


class ClosedProject(CharityProjectException):
    pass
