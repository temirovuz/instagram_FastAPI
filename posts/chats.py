from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.sql.functions import current_user
from starlette import status
from starlette.websockets import WebSocket

from auth.models import User
from auth.services import get_current_user
from core import database
from core.database import get_db
from posts.models import Room
from posts.schemas import RoomCreate, RoomOutput

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=RoomCreate)
def create_chat(room: RoomCreate, db=Depends(get_db), current_user: User = Depends(get_current_user)):
    new_room = Room(name=room.name)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@router.post('/create-private', status_code=status.HTTP_201_CREATED, response_model=RoomOutput)
def create_room_private(user_id: int, db=Depends(get_db), user: User = Depends(get_current_user)):
    if user.id == user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ozing bilan chat yaratolmaysan')
    room = db.query(Room).filter(
        or_(Room.name == f"{user_id}_{user.id}", Room.name == f"{user.id}_{user_id}")).first()
    if not room:
        new_room = Room(name=f"{user_id}_{user.id}")
        db.add(new_room)
        db.commit()
        db.refresh(new_room)
        return new_room
    return room


@router.get('/rooms-list', status_code=status.HTTP_200_OK, response_model=list[RoomOutput])
def get_rooms(current_user: User = Depends(get_current_user), db=Depends(get_db)):
    return db.query(Room).all()


@router.websocket('/room/{room_id}/message')
def create_message(room_id: int, websocket: WebSocket):
    pass