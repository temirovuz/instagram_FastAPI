from datetime import datetime

from pydantic import BaseModel


class CreatePost(BaseModel):
    image: str
    description: str


class UpdatePost(BaseModel):
    description: str


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
