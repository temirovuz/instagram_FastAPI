from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_

from starlette import status

from auth.services import get_current_user
from core.database import get_db
from posts.models import Post
from posts.schemas import CreatePost, UpdatePost, PostOutput, UserOutput

router = APIRouter(prefix='/post', tags=['post'])


@router.post('/create', status_code=status.HTTP_200_OK)
def create_post(data: CreatePost, db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    new_post = Post(**data.dict(), author=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/list', status_code=status.HTTP_200_OK)
def list_posts(db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    posts = db.query(Post).filter(Post.author == user.id).all()
    return posts


@router.get('/{id}', status_code=status.HTTP_200_OK)
def detail_post(post_id: int, db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    post = db.query(Post).filter(and_(Post.author == user.id, Post.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post sizga tegishli emas')
    return post


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_detail_post(post_id: int, data: UpdatePost, db=Depends(get_db),
                       user: UserOutput = Depends(get_current_user)):
    query = db.query(Post).filter(and_(Post.author == user.id, Post.id == post_id)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post sizga tegishli emas')
    db.query(Post).filter(Post.id == post_id).update(data.dict())
    db.commit()
    return {'message': f'Post updated.'}


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_post(post_id: int, db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    query = db.query(Post).filter(and_(Post.id == post_id, Post.author == user.id)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post sizga tegishli')
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()

    return {'message': f'Post  deleted.'}
