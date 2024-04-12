from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql.functions import now

from core.database import Base


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
