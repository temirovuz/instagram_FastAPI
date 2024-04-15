from fastapi import Depends
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import now

from core.database import Base, get_db


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    image = Column(String)
    description = Column(String)
    pub_date = Column(DateTime(), server_default=now())
    author = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return self.description


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    created = Column(DateTime(), server_default=now())
    post = Column(Integer, ForeignKey('posts.id'))
    author = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return self.text


class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    count = Column(Integer)
    post = Column(Integer, ForeignKey('posts.id'))
    author = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return self.count


def create_post(image, description, author, db: Session = Depends(get_db)):
    post = Post(image=image, description=description, author=author)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def create_comment(text: str, author: int, post_id: int, db: Session = Depends(get_db)):
    comment = Comment(text=text, post=post_id, author=author)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
