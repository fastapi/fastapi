from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.types import EmailStr
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.security import get_current_user
from app.core import config
from app.crud import user as crud_user
from app.db_models.user import User as DBUser
from app.models.user import User, UserInCreate, UserInDB, UserInUpdate
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/users/", tags=["users"], response_model=List[User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: DBUser = Depends(get_current_user),
):
    """
    Retrieve users
    """
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/users/", tags=["users"], response_model=User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserInCreate,
    current_user: DBUser = Depends(get_current_user),
):
    """
    Create new user
    """
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud_user.create(db, user_in=user_in)
    if config.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/users/me", tags=["users"], response_model=User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: DBUser = Depends(get_current_user),
):
    """
    Update own user
    """
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    current_user_data = jsonable_encoder(current_user)
    user_in = UserInUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud_user.update(db, user=current_user, user_in=user_in)
    return user


@router.get("/users/me", tags=["users"], response_model=User)
def read_user_me(
    db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)
):
    """
    Get current user
    """
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/users/open", tags=["users"], response_model=User)
def create_user_open(
    *,
    db: Session = Depends(get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
):
    """
    Create new user without the need to be logged in
    """
    if not config.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user resgistration is forbidden on this server",
        )
    user = crud_user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = UserInCreate(password=password, email=email, full_name=full_name)
    user = crud_user.create(db, user_in=user_in)
    return user


@router.get("/users/{user_id}", tags=["users"], response_model=User)
def read_user_by_id(
    user_id: int,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get a specific user by username (email)
    """
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    user = crud_user.get(db, user_id=user_id)
    if user == current_user:
        return user
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/users/{user_id}", tags=["users"], response_model=User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserInUpdate,
    current_user: UserInDB = Depends(get_current_user),
):
    """
    Update a user
    """
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    user = crud_user.get(db, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud_user.update(db, user=user, user_in=user_in)
    return user
