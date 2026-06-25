from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

from app.schemas.auth import (
    UserRegister,
    UserLogin,
    Token,
    UserOut
)

from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter()


@router.post('/register', response_model=Token)
def register(
    data: UserRegister,
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail='Email already registered'
        )

    user = User(
        email=data.email,
        name=data.name,
        hashed_password=hash_password(data.password)
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    token = create_access_token({
        'sub': user.id
    })

    return {
        'access_token': token,
        'token_type': 'bearer'
    }


@router.post('/login', response_model=Token)
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user or not verify_password(
        data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail='Invalid credentials'
        )

    token = create_access_token({
        'sub': user.id
    })

    return {
        'access_token': token,
        'token_type': 'bearer'
    }


@router.get('/me', response_model=UserOut)
def me(
    current_user: User = Depends(get_current_user)
):

    return UserOut(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        created_at=str(current_user.created_at)
    )