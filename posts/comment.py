from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy import and_

from auth.services import get_current_user
from core.database import get_db
from posts.models import Post, Comment
from posts.schemas import CreateComment, UserOutput

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/")
async def create_comment(data: CreateComment, db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == data.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = Comment(text=data.text, post_id=data.post_id, author_id=user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get('/list')
def list_posts(post_id, db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = db.query(Comment).filter(and_(Comment.post_id == post_id, Comment.author_id == user.id)).all()
    return comments


@router.put('/edit')
def edit_comment(comment_id=Form(), text=Form(), db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.author_id == user.id)).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.query(Comment).filter(Comment.id == comment_id).update({"text": text})
    db.commit()
    return {'message': 'Comment edited'}


@router.delete('/delete')
def delete_comment(comment_id=Form(), db=Depends(get_db), user=Depends(get_current_user)):
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.author_id == user.id)).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.query(Comment).filter(Comment.id == comment_id).delete()
    db.commit()
    return {'message': 'Comment deleted'}
