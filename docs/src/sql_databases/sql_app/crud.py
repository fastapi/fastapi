from sqlalchemy.orm import Session

from . import models


def get_user(db_session: Session, user_id: int):
    return db_session.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db_session: Session, email: str):
    return db_session.query(models.User).filter(models.User.email == email).first()


def get_users(db_session: Session, skip: int = 0, limit: int = 100):
    return db_session.query(models.User).offset(skip).limit(limit).all()


def get_items(db_session: Session, skip: int = 0, limit: int = 100):
    return db_session.query(models.Item).offset(skip).limit(limit).all()


def get_user_items(db_session: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db_session.query(models.Item)
        .filter(models.Item.owner_id == models.User.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
