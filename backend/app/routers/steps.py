from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.services.roadmap_service import complete_step
from app.utils.auth import get_current_user

router = APIRouter()

class CompleteStepRequest(BaseModel):
    user_roadmap_id: str
    step_id: str

@router.post('/complete')
def mark_complete(
    req: CompleteStepRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    ur = complete_step(
        db,
        req.user_roadmap_id,
        req.step_id,
        user.id
    )

    return {
        'progress_percentage': ur.progress_percentage,
        'status': ur.status
    }