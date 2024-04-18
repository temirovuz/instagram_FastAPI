from datetime import timedelta, timezone, datetime

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status

from auth.models import User
from core.database import get_db

SECRET_KEY = 'test'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/signin'
)


# Token yaratish uchun funksiya
def crate_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Tokenni tekshirish agar token yaroqli bolsa user_id qaytaradi
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get('user_id'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token is invalid')
        token_data = payload.get('user_id')
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='JWT error')
    return token_data


# qaytgan user_id ni bazadan korish bor yoki yoqligini
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_access_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user
