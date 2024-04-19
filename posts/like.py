from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_

from auth.services import get_current_user
from core.database import get_db
from posts.models import Like, Post
from posts.schemas import UserOutput, CreateLike

router = APIRouter(prefix="/like", tags=["like"])


@router.post("/", status_code=200)
def create_like(like: CreateLike, db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    query = db.query(Post).filter(Post.id == like.post_id).first()
    if not query:
        raise HTTPException(status_code=204, detail="Not Found")
    else:
        likes = db.query(Like).filter(and_(Like.post_id == like.post_id, Like.author_id == user.id)).first()
        if not likes:
            add_like = Like(post_id=like.post_id, author_id=user.id)
            db.add(add_like)
            db.commit()
            db.refresh(add_like)
            return add_like
        else:
            db.delete(likes)
            db.commit()
            return {"message": "Like Ochirildi"}


@router.get('/list', status_code=200)
def list_posts(db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    query = db.query(Like).filter(Like.author_id == user.id).all()
    return query
