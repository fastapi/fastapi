from . import models, schemas
from .database import session


class Storage:
    @staticmethod
    def create_user(user: schemas.UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
        session().add(db_user)
        session().commit()
        session().refresh(db_user)
        return db_user

    @staticmethod
    def get_user(user_id: int):
        return session().query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_user_by_email(email: str):
        return session().query(models.User).filter(models.User.email == email).first()
