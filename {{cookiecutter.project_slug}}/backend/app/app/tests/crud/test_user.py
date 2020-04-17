from fastapi.encoders import jsonable_encoder

from app import crud
from app.core.security import get_password_hash, verify_password
from app.db.session import db_session
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_lower_string, random_email


def test_create_user():
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db_session, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user():
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db_session, obj_in=user_in)
    authenticated_user = crud.user.authenticate(
        db_session, email=email, password=password
    )
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user():
    email = random_email()
    password = random_lower_string()
    user = crud.user.authenticate(db_session, email=email, password=password)
    assert user is None


def test_check_if_user_is_active():
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db_session, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active is True


def test_check_if_user_is_active_inactive():
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, disabled=True)
    user = crud.user.create(db_session, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active


def test_check_if_user_is_superuser():
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = crud.user.create(db_session, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user():
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db_session, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is False


def test_get_user():
    password = random_lower_string()
    username = random_email()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user = crud.user.create(db_session, obj_in=user_in)
    user_2 = crud.user.get(db_session, id=user.id)
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user():
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = crud.user.create(db_session, obj_in=user_in)
    new_password = random_lower_string()
    user_in = UserUpdate(password=new_password, is_superuser=True)
    crud.user.update(db_session, db_obj=user, obj_in=user_in)
    user_2 = crud.user.get(db_session, id=user.id)
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
