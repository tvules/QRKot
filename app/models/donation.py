from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import InvestedBase


class Donation(InvestedBase):
    """Donation model."""

    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)
