from datetime import datetime, timedelta

import jwt
from fastapi import Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from app.core.config import SECRET_KEY
from app.crud.user import get_user
from app.db.database import get_default_bucket
from app.models.token import TokenPayload

ALGORITHM = "HS256"
access_token_jwt_subject = "access"

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


def get_current_user(token: str = Security(reusable_oauth2)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    bucket = get_default_bucket()
    user = get_user(bucket, username=token_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
