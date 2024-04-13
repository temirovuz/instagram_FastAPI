from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from posts.models import Post
from posts.schemas import CreatePost

router = APIRouter()


@router.post('/create_post')
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    post = Post(image=post.image, description=post.description, pub_date=datetime.now(), author=post.author)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
