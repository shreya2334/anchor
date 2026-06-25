from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_roadmap import (
    UserRoadmap,
    RoadmapStatus,
    CompletedStep,
    Reflection
)
from app.models.roadmap import Roadmap
from app.models.user import User
from datetime import timedelta


def get_active_roadmap(
    db: Session,
    user_id: str
):
    return db.query(UserRoadmap).filter(
        UserRoadmap.user_id == user_id,
        UserRoadmap.status == RoadmapStatus.active
    ).first()


def start_roadmap(
    db: Session,
    user_id: str,
    roadmap_id: str
):
    existing = db.query(UserRoadmap).filter(
        UserRoadmap.user_id == user_id,
        UserRoadmap.roadmap_id == roadmap_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail='You already have this roadmap.'
        )

    active = get_active_roadmap(db, user_id)

    roadmap_status = RoadmapStatus.active
    if active:
        roadmap_status = RoadmapStatus.saved

    roadmap = db.query(Roadmap).filter(
        Roadmap.id == roadmap_id
    ).first()

    if not roadmap:
        raise HTTPException(
            status_code=404,
            detail='Roadmap not found'
        )

    ur = UserRoadmap(
        user_id=user_id,
        roadmap_id=roadmap_id,
        status=roadmap_status
    )

    db.add(ur)

    db.commit()

    db.refresh(ur)

    return ur


def update_roadmap_status(
    db: Session,
    user_roadmap_id: str,
    user_id: str,
    new_status: str
):
    ur = db.query(UserRoadmap).filter(
        UserRoadmap.id == user_roadmap_id,
        UserRoadmap.user_id == user_id
    ).first()

    if not ur:
        raise HTTPException(
            status_code=404,
            detail='Roadmap not found'
        )
    
    if new_status == 'active':
        active = get_active_roadmap(
            db,
            user_id
        )

        if active and active.id != ur.id:
            raise HTTPException(
                status_code=409,
                detail='You already have an active roadmap.'
            )

    ur.status = new_status

    if new_status == 'completed':
        ur.completed_at = datetime.utcnow()

    if new_status == 'paused':
        ur.paused_at = datetime.utcnow()

    db.commit()

    db.refresh(ur)

    return ur


def complete_step(
    db: Session,
    user_roadmap_id: str,
    step_id: str,
    user_id: str
):
    ur = db.query(UserRoadmap).filter(
        UserRoadmap.id == user_roadmap_id,
        UserRoadmap.user_id == user_id
    ).first()

    if not ur:
        raise HTTPException(
            status_code=404,
            detail='Not found'
        )

    existing = db.query(CompletedStep).filter(
        CompletedStep.user_roadmap_id == user_roadmap_id,
        CompletedStep.step_id == step_id
    ).first()

    if not existing:
        cs = CompletedStep(
            user_roadmap_id=user_roadmap_id,
            step_id=step_id
        )

        db.add(cs)

    total = len(ur.roadmap.steps)

    done = db.query(CompletedStep).filter(
        CompletedStep.user_roadmap_id == user_roadmap_id
    ).count() + (0 if existing else 1)

    ur.progress_percentage = (
        done / total * 100
    ) if total > 0 else 0

    ur.last_activity_at = datetime.utcnow()

    if ur.progress_percentage >= 100:
        ur.status = RoadmapStatus.completed
        ur.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(ur)
    
    return ur