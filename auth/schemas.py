from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class GetUser(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    signup_date: datetime


class UpdateUser(BaseModel):
    first_name: str
    last_name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr