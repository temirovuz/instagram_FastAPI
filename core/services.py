from fastapi import HTTPException
from jose import jwt, JWTError

from auth.services import SECRET_KEY, ALGORITHM


def check_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('user_id')
        if not email:
            raise HTTPException(status_code=401, detail='invalid Token')
    except JWTError:
        raise HTTPException(status_code=400, detail='JWT Error')
    return True