from pydantic import BaseModel
from typing import List


class StepOut(BaseModel):
    id: str
    roadmap_id: str
    title: str
    description: str
    resource_url: str
    resource_type: str
    order: int
    duration_minutes: int

    class Config:
        from_attributes = True


class RoadmapOut(BaseModel):
    id: str
    title: str
    description: str
    category: str
    difficulty: str
    estimated_hours: int
    tags: str

    steps: List[StepOut] = []

    class Config:
        from_attributes = True