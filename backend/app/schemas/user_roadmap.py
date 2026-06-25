from pydantic import BaseModel
from typing import List, Optional

from app.schemas.roadmap import RoadmapOut


class UserRoadmapOut(BaseModel):
    id: str
    user_id: str
    roadmap_id: str
    status: str
    progress_percentage: float
    started_at: str

    completed_at: Optional[str] = None

    roadmap: RoadmapOut

    completed_step_ids: List[str] = []

    class Config:
        from_attributes = True


class StartRoadmapRequest(BaseModel):
    roadmap_id: str


class UpdateStatusRequest(BaseModel):
    status: str


class ReflectionRequest(BaseModel):
    trigger: str

    what_learned: Optional[str] = None
    why_stopping: Optional[str] = None
    next_steps: Optional[str] = None