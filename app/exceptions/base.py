from typing import Optional


class BaseDetailException(Exception):
    detail: Optional[str] = None

    def __init__(self, detail: Optional[str] = None) -> None:
        if detail is not None:
            self.detail = detail


class DoesNotExist(BaseDetailException):
    pass
