from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException

from app.core import config
from app.core.jwt import create_access_token, get_current_user
from app.crud.user import (
    authenticate_user,
    check_if_user_is_active,
    check_if_user_is_superuser,
    get_user,
    update_user,
)
from app.db.database import get_default_bucket
from app.models.msg import Msg
from app.models.token import Token
from app.models.user import User, UserInDB, UserInUpdate
from app.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/login/access-token", response_model=Token, tags=["login"])
def route_login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    bucket = get_default_bucket()
    user = authenticate_user(bucket, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not check_if_user_is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"username": form_data.username}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", tags=["login"], response_model=User)
def route_test_token(current_user: UserInDB = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{username}", tags=["login"], response_model=Msg)
def route_recover_password(username: str):
    """
    Password Recovery
    """
    bucket = get_default_bucket()
    user = get_user(bucket, username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(username)
    send_reset_password_email(
        email_to=user.email, username=username, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", tags=["login"], response_model=Msg)
def route_reset_password(token: str, new_password: str):
    """
    Reset password
    """
    username = verify_password_reset_token(token)
    if not username:
        raise HTTPException(status_code=400, detail="Invalid token")
    bucket = get_default_bucket()
    user = get_user(bucket, username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not check_if_user_is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    user_in = UserInUpdate(name=username, password=new_password)
    user = update_user(bucket, user_in)
    return {"msg": "Password updated successfully"}
