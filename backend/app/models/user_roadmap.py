import uuid
import enum
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Float,
    Text,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.database import Base

class RoadmapStatus(str, enum.Enum):
    active = 'active'
    paused = 'paused'
    saved = 'saved'
    completed = 'completed'
    abandoned = 'abandoned'


class UserRoadmap(Base):
    __tablename__ = 'user_roadmaps'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(
        String,
        ForeignKey('users.id'),
        nullable=False
    )

    roadmap_id = Column(
        String,
        ForeignKey('roadmaps.id'),
        nullable=False
    )

    status = Column(String, default='active', nullable=False)

    progress_percentage = Column(Float, default=0.0)

    started_at = Column(DateTime, default=datetime.utcnow)

    completed_at = Column(DateTime, nullable=True)

    paused_at = Column(DateTime, nullable=True)

    last_activity_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
        'User',
        back_populates='user_roadmaps'
    )

    roadmap = relationship(
        'Roadmap',
        back_populates='user_roadmaps'
    )

    completed_steps = relationship(
        'CompletedStep',
        back_populates='user_roadmap',
        cascade='all, delete-orphan'
    )

    reflections = relationship(
        'Reflection',
        back_populates='user_roadmap',
        cascade='all, delete-orphan'
    )


class CompletedStep(Base):
    __tablename__ = 'completed_steps'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_roadmap_id = Column(
        String,
        ForeignKey('user_roadmaps.id'),
        nullable=False
    )

    step_id = Column(
        String,
        ForeignKey('steps.id'),
        nullable=False
    )

    completed_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            'user_roadmap_id',
            'step_id',
            name='unique_completion'
        ),
    )

    user_roadmap = relationship(
        'UserRoadmap',
        back_populates='completed_steps'
    )

    step = relationship(
        'Step',
        back_populates='completed_steps'
    )


class Reflection(Base):
    __tablename__ = 'reflections'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(
        String,
        ForeignKey('users.id'),
        nullable=False
    )

    user_roadmap_id = Column(
        String,
        ForeignKey('user_roadmaps.id'),
        nullable=False
    )

    trigger = Column(String, nullable=False)

    what_learned = Column(Text, nullable=True)

    why_stopping = Column(Text, nullable=True)

    next_steps = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
        'User',
        back_populates='reflections'
    )

    user_roadmap = relationship(
        'UserRoadmap',
        back_populates='reflections'
    )