from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserInDB
from app.core.security import verify_password, get_password_hash
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db_session: Session, *, email: str) -> Optional[User]:
        return db_session.query(User).filter(User.email == email).first()

    def create(self, db_session: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(self, db_session: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        if obj_in.password:
            update_data = obj_in.dict(exclude_unset=True)
            hashed_password = get_password_hash(obj_in.password)
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
            use_obj_in = UserInDB.parse_obj(update_data)
        return super().update(db_session, db_obj=db_obj, obj_in=use_obj_in)

    def authenticate(
        self, db_session: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = self.get_by_email(db_session, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
