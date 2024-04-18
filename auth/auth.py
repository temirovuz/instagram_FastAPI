from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from auth.schemas import Token, CreateUser
from auth.models import User, create_user
from auth.services import crate_access_token
from core.database import get_db
from core.ultis import verify_password, hash_password

router = APIRouter(prefix='/auth', tags=["auth"])


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def create_users(user_data: CreateUser, db: Session = Depends(get_db)):
    password = hash_password(user_data.password)
    user = create_user(user_data.email, password, db)
    return user


@router.post("/login", status_code=200, response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    query = db.query(User).filter(User.email == user.username).first()

    if not query:
        raise HTTPException(status_code=409, detail="Incorrect email")
    if not verify_password(user.password, query.password):
        raise HTTPException(status_code=409, detail="Incorrect password")
    access_token = crate_access_token(data={'user_id': query.id})
    return {'access_token': access_token, 'token_type': 'Bearer'}
