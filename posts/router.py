from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from auth.services import SECRET_KEY, ALGORITHM
from core.database import get_db
from posts.models import Post, create_post
from posts.schemas import CreatePost

router = APIRouter()


@router.post('/create')
def create_post_(post: CreatePost, db: Session = Depends(get_db), token: str = Depends()):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail='invalid Token')
    except JWTError as e:
        raise HTTPException(status_code=400, detail=f'{e}')

    post = create_post(post.image, post.description, post.author, db)
    return post
