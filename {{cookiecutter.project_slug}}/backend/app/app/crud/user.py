from typing import List, Union

from fastapi.encoders import jsonable_encoder

from app.core.security import get_password_hash, verify_password
from app.db_models.user import User
from app.models.user import UserInCreate, UserInUpdate


def get(db_session, *, user_id: int) -> Union[User, None]:
    return db_session.query(User).filter(User.id == user_id).first()


def get_by_email(db_session, *, email: str) -> Union[User, None]:
    return db_session.query(User).filter(User.email == email).first()


def authenticate(db_session, *, email: str, password: str) -> Union[User, bool]:
    user = get_by_email(db_session, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def is_active(user) -> bool:
    return user.is_active


def is_superuser(user) -> bool:
    return user.is_superuser


def get_multi(db_session, *, skip=0, limit=100) -> Union[List[User], List[None]]:
    return db_session.query(User).offset(skip).limit(limit).all()


def create(db_session, *, user_in: UserInCreate) -> User:
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_superuser=user_in.is_superuser,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def update(db_session, *, user: User, user_in: UserInUpdate) -> User:
    user_data = jsonable_encoder(user)
    for field in user_data:
        if field in user_in.fields:
            value_in = getattr(user_in, field)
            if value_in is not None:
                setattr(user, field, value_in)
    if user_in.password:
        passwordhash = get_password_hash(user_in.password)
        user.hashed_password = passwordhash
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
