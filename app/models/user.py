from typing import TypeVar

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    donations = relationship("Donation", backref="user")


TUserModel = TypeVar("TUserModel", bound=User)
