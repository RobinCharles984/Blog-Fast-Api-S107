from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.models.users import Users
from app.repositories.jwt_repo import JWTRepo
from dependencies.db import get_session

from sqlalchemy.orm import Session

from exceptions.http_exceptions import FORBIDDEN_EXCEPTION

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/login')


def get_current_user_dependency(db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    try:
        payload = JWTRepo.decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(Users).filter(Users.id == int(user_id)).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise FORBIDDEN_EXCEPTION


def get_admin_user_dependency(current_user: Users = Depends(get_current_user_dependency)):
    if current_user.role != "admin":
        raise FORBIDDEN_EXCEPTION
    return current_user
