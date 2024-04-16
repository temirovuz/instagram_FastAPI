from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from auth.models import User
from auth.schemas import UpdateUser, CreateUsername
from auth.services import SECRET_KEY, ALGORITHM
from core.database import get_db


router = APIRouter(prefix="/user", tags=["user"])

