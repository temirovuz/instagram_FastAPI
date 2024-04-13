from datetime import datetime

from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    email: str
    password: str


class GetUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    signup_date: datetime
