from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateComment(BaseModel):
    text: str
    post_id: int


class CommentOutput(BaseModel):
    id: int
    text: str
    created: datetime


class CreatePost(BaseModel):
    image: str
    description: str


class PostOutput(BaseModel):
    id: int
    image: str
    description: str
    pub_date: datetime
    # author: int


class PostOutputAll(CreatePost):
    id: int
    comments: list[CommentOutput]


class UpdatePost(BaseModel):
    description: str


class UserOutput(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    signup_date: datetime

    class Config:
        orm_mode = True


class CreateLike(BaseModel):
    post_id: int
