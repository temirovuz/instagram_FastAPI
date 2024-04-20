from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy import and_

from auth.services import get_current_user
from core.database import get_db
from .models import Follower, User
from posts.schemas import UserOutput
from .schemas import FollowerSchema, FollowingSchema

router = APIRouter(prefix="/followers", tags=["followers"])


@router.post("/obuna_bolish")
def add_following(user_id=Form(), db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    users = db.query(User).filter(User.id == user_id).first()
    if not users:
        raise HTTPException(status_code=404, detail="User topilmadi")
    following = db.query(Follower).filter(
        and_(Follower.obunachilar_id == user.id, Follower.obunalar_id == user_id)).first()
    if following:
        raise HTTPException(status_code=409, detail="Siz oldin sorov yuborgansiz")
    followings = Follower(obunalar_id=user_id, obunachilar_id=user.id)
    db.add(followings)
    db.commit()
    db.refresh(followings)
    return followings


@router.get("/kuzatishlar", status_code=200, response_model=list[FollowerSchema])
def get_follower(db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    followers = db.query(Follower).filter(and_(Follower.obunachilar_id == user.id, Follower.status == 'accepted')).all()
    return followers


@router.get("/kuzatuvchilar")
def get_following(db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    followings = db.query(Follower).filter(and_(Follower.obunalar_id == user.id, Follower.status == 'accepted')).all()
    return followings


@router.get('/kuzatish_sorovi', status_code=200, response_model=list[FollowingSchema])
def get_followings_request(db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    query = db.query(Follower).filter(and_(Follower.obunachilar_id == user.id, Follower.status == 'pending')).all()
    return query


@router.get('/kuzatuvchilar_sorovi')
def get_followers_request(db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    query = db.query(Follower).filter(and_(Follower.obunalar_id == user.id, Follower.status == 'pending')).all()
    return query


@router.post("/obunani/{follower_id}/qabul_qilish")
def follower_accept(follower_id, db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    query = db.query(Follower).filter(
        and_(Follower.id == follower_id, Follower.obunalar_id == user.id)).first()
    if not query:
        raise HTTPException(status_code=404, detail="Bunday sorov topilmadi")
    db.query(Follower).filter(Follower.id == follower_id).update({"status": "accepted"})
    db.commit()
    return {'message': 'Follower Accepted'}


@router.post("/obunani/{follower_id}/rat_qilish")
def follower_reject(follower_id, db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    query = db.query(Follower).filter(
        and_(Follower.id == follower_id, Follower.obunalar_id == user.id)).first()
    if not query:
        raise HTTPException(status_code=404, detail="Bunday sorov topilmadi")
    db.query(Follower).filter(Follower.id == follower_id).delete()
    db.commit()
    return {'message': 'Follower rejected'}


@router.post("/obunamni/{follower_id}/bekor_qilish")
def follower_cancel(follower_id, db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    query = db.query(Follower).filter(and_(Follower.id == follower_id, Follower.obunachilar_id == user.id)).first()
    if not query:
        raise HTTPException(status_code=404, detail="Bunday sorov topilmadi")
    db.query(Follower).filter(Follower.id == follower_id).delete()
    db.commit()
    return {'message': 'Follower request Canceled'}
