from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from auth.models import User
from auth.schemas import UpdateUser, CreateUsername
from auth.services import SECRET_KEY, ALGORITHM
from core.database import get_db
from core.services import check_token
from core.utils import hash_password, verify_password

router = APIRouter(prefix="/user", tags=["user"])


@router.get('/info')
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    else:
        return user


@router.post('/update/{id}')
def user_update(user_data: UpdateUser, db: Session = Depends(get_db), token: str = Depends):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('user_id')
        if not email:
            raise HTTPException(status_code=401, detail='invalid Token')
        else:
            db.query(User).filter(User.id == email).update(dict(user_data))
            db.commit()
            return {'message': 'User updated successfully'}
    except JWTError:
        raise HTTPException(status_code=400, detail='JWT Error')


@router.post('/add_username')
def add_username(username: CreateUsername, db: Session = Depends(get_db), token: str = Depends):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('user_id')
        if not email:
            raise HTTPException(status_code=401, detail='invalid Token')
        else:
            user = db.query(User).filter(User.id == email).first()
            if not user.username == username:
                db.query(User).filter(User.id == email).update(dict(username))
                db.commit()
            else:
                raise HTTPException(status_code=409, detail='Username already exists')
            return {'message': 'Username added successfully'}
    except JWTError:
        raise HTTPException(status_code=400, detail='JWT Error')
