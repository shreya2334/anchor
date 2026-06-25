from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base

import app.models.user
import app.models.roadmap
import app.models.user_roadmap

from app.routers import (
    auth,
    roadmaps,
    user_roadmaps,
    steps
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='Anchor API',
    description='One roadmap at a time.',
    version='1.0.0'
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        settings.frontend_url,
        'http://localhost:3000'
    ],

    allow_credentials=True,

    allow_methods=['*'],

    allow_headers=['*'],
)


app.include_router(
    auth.router,
    prefix='/api/auth',
    tags=['auth']
)

app.include_router(
    roadmaps.router,
    prefix='/api/roadmaps',
    tags=['roadmaps']
)

app.include_router(
    user_roadmaps.router,
    prefix='/api/user-roadmaps',
    tags=['user-roadmaps']
)

app.include_router(
    steps.router,
    prefix='/api/steps',
    tags=['steps']
)


@app.get('/')
def health():
    return {
        'status': 'ok',
        'message': 'Anchor API running'
    }