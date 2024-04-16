from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from auth.services import SECRET_KEY, ALGORITHM, get_current_user
from core import db
from core.database import get_db
from core.services import check_token
from posts.models import Post, create_post
from posts.schemas import CreatePost, UpdatePost, PostOutput, UserOutput

router = APIRouter(prefix='/posts', tags=['posts'])


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=PostOutput)
def create_post(data: CreatePost, db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    new_post = Post(**data.dict(), author=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



