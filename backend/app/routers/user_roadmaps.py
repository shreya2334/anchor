from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.user_roadmap import (
    UserRoadmap,
    Reflection
)
from app.schemas.user_roadmap import (
    StartRoadmapRequest,
    UpdateStatusRequest,
    ReflectionRequest
)
from app.services.roadmap_service import (
    start_roadmap,
    update_roadmap_status,
    get_active_roadmap
)
from app.utils.auth import get_current_user

router = APIRouter()

def serialize_ur(ur):
    return {
        'id': ur.id,
        'user_id': ur.user_id,
        'roadmap_id': ur.roadmap_id,
        'status': ur.status,
        'progress_percentage': ur.progress_percentage,
        'started_at': str(ur.started_at),

        'completed_at': (
            str(ur.completed_at)
            if ur.completed_at else None
        ),

        'roadmap': {
            'id': ur.roadmap.id,
            'title': ur.roadmap.title,
            'description': ur.roadmap.description,
            'category': ur.roadmap.category,
            'difficulty': ur.roadmap.difficulty,
            'estimated_hours': ur.roadmap.estimated_hours,
            'tags': ur.roadmap.tags,

            'steps': [
                {
                    'id': s.id,
                    'roadmap_id': s.roadmap_id,
                    'title': s.title,
                    'description': s.description,
                    'resource_url': s.resource_url,
                    'resource_type': s.resource_type,
                    'order': s.order,
                    'duration_minutes': s.duration_minutes
                }
                for s in ur.roadmap.steps
            ]
        },

        'completed_steps': [
            {
                'step_id': cs.step_id
            }
            for cs in ur.completed_steps
        ]
    }

@router.post('/start')
def start(
    req: StartRoadmapRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    ur = start_roadmap(
        db,
        user.id,
        req.roadmap_id
    )

    return serialize_ur(ur)


@router.get('/active')
def active(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    ur = get_active_roadmap(
        db,
        user.id
    )

    if not ur:
        return None

    return serialize_ur(ur)


@router.get('/history')
def history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    urs = db.query(UserRoadmap).filter(
        UserRoadmap.user_id == user.id
    ).all()

    return [
        serialize_ur(ur)
        for ur in urs
    ]


@router.patch('/{ur_id}/status')
def update_status(
    ur_id: str,
    req: UpdateStatusRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    ur = update_roadmap_status(
        db,
        ur_id,
        user.id,
        req.status
    )

    return serialize_ur(ur)


@router.post('/{ur_id}/reflect')
def reflect(
    ur_id: str,
    req: ReflectionRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    ref = Reflection(
        user_id=user.id,
        user_roadmap_id=ur_id,
        trigger=req.trigger,
        what_learned=req.what_learned,
        why_stopping=req.why_stopping,
        next_steps=req.next_steps
    )

    db.add(ref)

    db.commit()

    return {
        'message': 'Reflection saved'
    }

@router.post('/{ur_id}/complete-step/{step_id}')
def complete_step(
    ur_id: str,
    step_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    ur = db.query(UserRoadmap).filter(
        UserRoadmap.id == ur_id,
        UserRoadmap.user_id == user.id
    ).first()

    if not ur:
        return {
            'message': 'Roadmap not found'
        }

    existing = next(
        (
            cs for cs in ur.completed_steps
            if cs.step_id == step_id
        ),
        None
    )

    if existing:
        return serialize_ur(ur)

    from app.models.user_roadmap import CompletedStep

    completed = CompletedStep(
        user_roadmap_id=ur.id,
        step_id=step_id
    )

    db.add(completed)

    total_steps = len(ur.roadmap.steps)

    completed_count = (
        len(ur.completed_steps) + 1
    )

    ur.progress_percentage = round(
        (completed_count / total_steps) * 100,
        1
    )

    if completed_count == total_steps:
        ur.status = 'completed'

    db.commit()

    db.refresh(ur)

    return serialize_ur(ur)