import uuid
from datetime import datetime
from sqlalchemy import Integer
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user_roadmaps = relationship(
        'UserRoadmap',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    reflections = relationship(
        'Reflection',
        back_populates='user',
        cascade='all, delete-orphan'
    )
