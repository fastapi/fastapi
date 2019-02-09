from fastapi.encoders import jsonable_encoder

from app.crud.user import (
    authenticate_user,
    check_if_user_is_active,
    check_if_user_is_superuser,
    get_user,
    upsert_user,
)
from app.db.database import get_default_bucket
from app.models.role import RoleEnum
from app.models.user import UserInCreate
from app.tests.utils.utils import random_lower_string


def test_create_user():
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserInCreate(username=email, email=email, password=password)
    bucket = get_default_bucket()
    user = upsert_user(bucket, user_in, persist_to=1)
    assert hasattr(user, "username")
    assert user.username == email
    assert hasattr(user, "hashed_password")
    assert hasattr(user, "type")
    assert user.type == "userprofile"


def test_authenticate_user():
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserInCreate(username=email, email=email, password=password)
    bucket = get_default_bucket()
    user = upsert_user(bucket, user_in, persist_to=1)
    authenticated_user = authenticate_user(bucket, email, password)
    assert authenticated_user
    assert user.username == authenticated_user.username


def test_not_authenticate_user():
    email = random_lower_string()
    password = random_lower_string()
    bucket = get_default_bucket()
    user = authenticate_user(bucket, email, password)
    assert user is False


def test_check_if_user_is_active():
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserInCreate(username=email, email=email, password=password)
    bucket = get_default_bucket()
    user = upsert_user(bucket, user_in, persist_to=1)
    is_active = check_if_user_is_active(user)
    assert is_active is True


def test_check_if_user_is_active_inactive():
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserInCreate(
        username=email, email=email, password=password, disabled=True
    )
    bucket = get_default_bucket()
    user = upsert_user(bucket, user_in, persist_to=1)
    is_active = check_if_user_is_active(user)
    assert is_active is False


def test_check_if_user_is_superuser():
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserInCreate(
        username=email, email=email, password=password, admin_roles=[RoleEnum.superuser]
    )
    bucket = get_default_bucket()
    user = upsert_user(bucket, user_in, persist_to=1)
    is_superuser = check_if_user_is_superuser(user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user():
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserInCreate(username=username, email=username, password=password)
    bucket = get_default_bucket()
    user = upsert_user(bucket, user_in, persist_to=1)
    is_superuser = check_if_user_is_superuser(user)
    assert is_superuser is False


def test_get_user():
    password = random_lower_string()
    username = random_lower_string()
    user_in = UserInCreate(
        username=username,
        email=username,
        password=password,
        admin_roles=[RoleEnum.superuser],
    )
    bucket = get_default_bucket()
    user = upsert_user(bucket, user_in, persist_to=1)
    user_2 = get_user(bucket, username)
    assert user.username == user_2.username
    assert jsonable_encoder(user) == jsonable_encoder(user_2)
