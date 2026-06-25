import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Roadmap(Base):
    __tablename__ = 'roadmaps'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    category = Column(String, nullable=False, index=True)

    difficulty = Column(String, default='beginner')

    estimated_hours = Column(Integer, default=0)

    tags = Column(String, default='')

    created_at = Column(DateTime, default=datetime.utcnow)

    steps = relationship(
        'Step',
        back_populates='roadmap',
        order_by='Step.order',
        cascade='all, delete-orphan'
    )

    user_roadmaps = relationship(
        'UserRoadmap',
        back_populates='roadmap'
    )


class Step(Base):
    __tablename__ = 'steps'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    roadmap_id = Column(
        String,
        ForeignKey('roadmaps.id'),
        nullable=False
    )

    title = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    resource_url = Column(String, nullable=False)

    resource_type = Column(String, default='article')

    order = Column(Integer, nullable=False)

    duration_minutes = Column(Integer, default=30)

    roadmap = relationship(
        'Roadmap',
        back_populates='steps'
    )

    completed_steps = relationship(
        'CompletedStep',
        back_populates='step',
        cascade='all, delete-orphan'
    )