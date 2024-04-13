from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.models import User
from auth.schemas import CreateUser, UpdateUser
from core.database import get_db

router = APIRouter()


@router.post('/create')
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user = User(username=user.username, email=user.email, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/info')
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    else:
        return user


@router.post('/update')
def user_update(user_id: int, user_data: UpdateUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).update(dict(user_data))
    db.commit()
    return user_data
