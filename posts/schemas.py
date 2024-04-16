from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreatePost(BaseModel):
    image: str
    description: str


class UpdatePost(BaseModel):
    description: str


class UserOutput(BaseModel):
    id: int
    email: EmailStr
    pub_date: datetime

    class Config:
        orm_mode = True


class PostOutput(BaseModel):
    id: int
    created: datetime
    owner: UserOutput


class CreateComment(BaseModel):
    id: int
    text: str
    author: int
    post: int


class CreateLike(BaseModel):
    id: int
    count: int
    post: int
    author: int
