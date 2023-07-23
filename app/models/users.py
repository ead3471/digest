from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base
from .posts import Digest, Subscription


class User(Base):
    """User model"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    digests = relationship(
        Digest, back_populates="user", cascade="all, delete"
    )
    subscriptions = relationship(
        Subscription, back_populates="user", cascade="all, delete"
    )
