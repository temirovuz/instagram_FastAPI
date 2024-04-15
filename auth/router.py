from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from auth.models import User, create_user
from auth.schemas import CreateUser, UpdateUser
from core.database import get_db
from core.utils import hash_password, verify_password

router = APIRouter()


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def create_users(user_data: CreateUser, db: Session = Depends(get_db)):
    password = hash_password(user_data.password)
    user = create_user(user_data.email, password, db)
    return user


@router.post('/signin', status_code=status.HTTP_200_OK)
def login_user(user_data: CreateUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    if not verify_password(user_data.password, user_data.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Incorrect password',)







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
