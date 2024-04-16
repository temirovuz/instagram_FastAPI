from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from auth.services import SECRET_KEY, ALGORITHM
from core.database import get_db
from core.services import check_token
from posts.models import Post, create_post
from posts.schemas import CreatePost, UpdatePost

router = APIRouter(prefix='/posts', tags=['posts'])




@router.post('/create')
def create_post_(post: CreatePost, db: Session = Depends(get_db), token: str = Depends):
    check_user = check_token(token)
    if check_user:
        post = create_post(post.image, post.description, check_user, db)
        return post

@router.get('/update/{post_id}')
def update_post(info: UpdatePost, post_id: int, db: Session = Depends(get_db), token: str = Depends):
    pass