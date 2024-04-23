from fastapi import Depends
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql.functions import now

from core.database import Base, get_db


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    image = Column(String)
    description = Column(String)
    pub_date = Column(DateTime(), server_default=now())
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', backref='posts')

    def __repr__(self):
        return self.description


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    created = Column(DateTime(), server_default=now())
    post_id = Column(Integer, ForeignKey('posts.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    post = relationship('Post', backref='comments')
    author = relationship('User', backref='comments')

    def __repr__(self):
        return self.text


class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    post = relationship('Post', backref='likes')
    author = relationship('User', backref='likes')


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True)
    created = Column(DateTime(), default=now)


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String, nullable=False)
    created = Column(DateTime(), default=now)
    room = relationship('Room', backref='messages')
    user = relationship('User', backref='messages')


def create_post(image_url, description, author, db: Session = Depends(get_db)):
    post = Post(image=image_url, description=description, author_id=author)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(post_if: int, description, db: Session = Depends(get_db)):
    db.query(Post).filter(Post.description == description).update({'description': description})


def create_comment(text: str, author: int, post_id: int, db: Session = Depends(get_db)):
    comment = Comment(text=text, post_id=post_id, author_id=author)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
