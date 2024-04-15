from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from auth.schemas import Token, CreateUser
from auth.models import User
from auth.services import crate_access_token
from core.database import get_db
from core.utils import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/signin', status_code=status.HTTP_200_OK, response_model=Token)
def signin(user_data: CreateUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    if not verify_password(user_data.password, user_data.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Invalid password')

    access_token = crate_access_token(**user_data.dict())
    return {'access_token': access_token, 'token_type': 'Bearer'}