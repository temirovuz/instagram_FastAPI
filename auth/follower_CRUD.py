from fastapi import Depends
from sqlalchemy.orm import Session

from auth.models import Follower
from core.database import get_db


def follower_add(follower_id, user_id, db: Session = Depends(get_db)):
    followings = Follower(obunalar_id=follower_id, obunachilar_id=user_id)
    db.add(followings)
    db.commit()
    db.refresh(followings)
    return followings
