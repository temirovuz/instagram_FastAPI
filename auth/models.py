from fastapi import Depends, HTTPException
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql.functions import now

from core.database import Base, get_db


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(25), default=False)
    last_name = Column(String(25), default=False)
    username = Column(String(20), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(50))
    signup_date = Column(DateTime(), server_default=now())
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return self.username


class Follower(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    following_id = Column(Integer, ForeignKey('users.id'))
    follower_id = Column(Integer, ForeignKey('users.id'))
    follower = relationship('User', backref='followers')
    following = relationship('User', backref='followings')


def create_user(email, password, db: Session = Depends(get_db)):
    query = db.query(User).filter(User.email == email).first()
    if not query:
        user = User(email=email, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        raise HTTPException(status_code=409, detail='Email already registered')
    return user
