from typing import List

from fastapi import APIRouter, Body, Depends
from pydantic.types import EmailStr
from starlette.exceptions import HTTPException

from app.core import config
from app.core.jwt import get_current_user
from app.crud.user import (
    check_if_user_is_active,
    check_if_user_is_superuser,
    get_user,
    get_users,
    search_users,
    update_user,
    upsert_user,
)
from app.db.database import get_default_bucket
from app.models.user import User, UserInCreate, UserInDB, UserInUpdate
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/users/", tags=["users"], response_model=List[User])
def route_users_get(
    skip: int = 0, limit: int = 100, current_user: UserInDB = Depends(get_current_user)
):
    """
    Retrieve users
    """
    if not check_if_user_is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not check_if_user_is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    bucket = get_default_bucket()
    users = get_users(bucket, skip=skip, limit=limit)
    return users


@router.get("/users/search/", tags=["users"], response_model=List[User])
def route_search_users(
    q: str,
    skip: int = 0,
    limit: int = 100,
    current_user: UserInDB = Depends(get_current_user),
):
    """
    Search users, use Bleve Query String syntax: http://blevesearch.com/docs/Query-String-Query/

    For typeahead sufix with `*`. For example, a query with: `email:johnd*` will match users with
    email `johndoe@example.com`, `johndid@example.net`, etc.
    """
    if not check_if_user_is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not check_if_user_is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    bucket = get_default_bucket()
    users = search_users(bucket=bucket, query_string=q, skip=skip, limit=limit)
    return users


@router.post("/users/", tags=["users"], response_model=User)
def route_users_post(
    *, user_in: UserInCreate, current_user: UserInDB = Depends(get_current_user)
):
    """
    Create new user
    """
    if not check_if_user_is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not check_if_user_is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    bucket = get_default_bucket()
    user = get_user(bucket, user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = upsert_user(bucket, user_in, persist_to=1)
    if config.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.username, password=user_in.password
        )
    return user


@router.put("/users/me", tags=["users"], response_model=User)
def route_users_me_put(
    *,
    password: str = None,
    full_name: str = None,
    email: EmailStr = None,
    current_user: UserInDB = Depends(get_current_user),
):
    """
    Update own user
    """
    if not check_if_user_is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    user_in = UserInUpdate(**current_user.dict())
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    bucket = get_default_bucket()
    user = update_user(bucket, user_in)
    return user


@router.get("/users/me", tags=["users"], response_model=User)
def route_users_me_get(current_user: UserInDB = Depends(get_current_user)):
    """
    Get current user
    """
    if not check_if_user_is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/users/open", tags=["users"], response_model=User)
def route_users_post_open(
    *,
    username: str = Body(...),
    password: str = Body(...),
    email: EmailStr = Body(None),
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
    bucket = get_default_bucket()
    user = get_user(bucket, username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = UserInCreate(
        username=username, password=password, email=email, full_name=full_name
    )
    user = upsert_user(bucket, user_in, persist_to=1)
    return user


@router.get("/users/{username}", tags=["users"], response_model=User)
def route_users_id_get(
    username: str, current_user: UserInDB = Depends(get_current_user)
):
    """
    Get a specific user by username (email)
    """
    if not check_if_user_is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    bucket = get_default_bucket()
    user = get_user(bucket, username)
    if user == current_user:
        return user
    if not check_if_user_is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/users/{username}", tags=["users"], response_model=User)
def route_users_put(
    *,
    username: str,
    user_in: UserInUpdate,
    current_user: UserInDB = Depends(get_current_user),
):
    """
    Update a user
    """
    if not check_if_user_is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not check_if_user_is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    bucket = get_default_bucket()
    user = get_user(bucket, username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = update_user(bucket, user_in)
    return user
