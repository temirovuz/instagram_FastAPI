from fastapi import APIRouter, Depends, HTTPException, Form

from auth.models import User
from auth.services import get_current_user
from core.database import get_db
from core.ultis import verify_password, hash_password
from posts.schemas import UserOutput

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/info", status_code=200, response_model=UserOutput)
def info_user(db=Depends(get_db), user: UserOutput = Depends(get_current_user)):
    return db.query(User).filter(User.id == user.id).first()


@router.put("/update_username")
def add_username(data=Form(), user: UserOutput = Depends(get_current_user), db=Depends(get_db)):
    username = db.query(User).filter(User.username == data.lower()).first()
    if username:
        raise HTTPException(status_code=400, detail="Bu Username band. Iltimos boshqa username kiriting!")
    db.query(User).filter(User.id == user.id).update({'username': data.lower()})
    db.commit()
    return {"message": "Username qoyildi"}


@router.put("/update_password")
def password_change(pwd=Form(), pwd2=Form(), user: UserOutput = Depends(get_current_user), db=Depends(get_db)):
    query = db.query(User).filter(User.id == user.id).first()
    if pwd != pwd2:
        raise HTTPException(status_code=400, detail="Parollar bir ekanligini tekshirib koring")
    else:
        ans = verify_password(pwd, query.password)
        if ans:
            raise HTTPException(status_code=400, detail='Yangi kiritgan kodingiz oldingi koddan farql bolishi lozim')
    up_password = hash_password(pwd)
    db.query(User).filter(User.id == user.id).update({'password': up_password})
    db.commit()
    return {"message": "Password ozgartirildi"}


@router.put("/update_fullname")
def update_fullname(last_name=Form(), first_name=Form(), db=Depends(get_db),
                    user: UserOutput = Depends(get_current_user)):
    db.query(User).filter(User.id == user.id).update({'first_name': first_name, 'last_name': last_name})
    db.commit()
    return {"message": "Fullname ozgartirildi"}


@router.delete('/delete')
def delete_user(user: UserOutput = Depends(get_current_user), db=Depends(get_db)):
    db.query(User).filter(User.id == user.id).delete()
    db.commit()
    return {"message": "User deleted"}
