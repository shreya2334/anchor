from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.roadmap import Roadmap

from app.schemas.roadmap import RoadmapOut

from app.utils.auth import get_current_user


router = APIRouter()


@router.get('/', response_model=List[RoadmapOut])
def list_roadmaps(
    category: str = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    q = db.query(Roadmap)

    if category:
        q = q.filter(
            Roadmap.category == category
        )

    return q.all()


@router.get('/{roadmap_id}', response_model=RoadmapOut)
def get_roadmap(
    roadmap_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    r = db.query(Roadmap).filter(
        Roadmap.id == roadmap_id
    ).first()

    if not r:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail='Not found'
        )

    return r