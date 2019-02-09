from app.core.security import get_password_hash
from app.models.role import Role
from app.models.user import User


def get_user(username, db_session):
    return db_session.query(User).filter(User.id == username).first()


def check_if_user_is_active(user):
    return user.is_active


def check_if_user_is_superuser(user):
    return user.is_superuser


def check_if_username_is_active(username, db_session):
    user = get_user(username, db_session)
    return check_if_user_is_active(user)


def get_role_by_name(name, db_session):
    role = db_session.query(Role).filter(Role.name == name).first()
    return role


def get_role_by_id(role_id, db_session):
    role = db_session.query(Role).filter(Role.id == role_id).first()
    return role


def create_role(name, db_session):
    role = Role(name=name)
    db_session.add(role)
    db_session.commit()
    return role


def get_roles(db_session):
    return db_session.query(Role).all()


def get_user_roles(user):
    return user.roles


def get_user_by_username(username, db_session) -> User:
    user = db_session.query(User).filter(User.email == username).first()  # type: User
    return user


def get_user_by_id(user_id, db_session):
    user = db_session.query(User).filter(User.id == user_id).first()  # type: User
    return user


def get_user_hashed_password(user):
    return user.password


def get_user_id(user):
    return user.id


def get_users(db_session):
    return db_session.query(User).all()


def create_user(
    db_session, username, password, first_name=None, last_name=None, is_superuser=False
):
    user = User(
        email=username,
        password=get_password_hash(password),
        first_name=first_name,
        last_name=last_name,
        is_superuser=is_superuser,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def assign_role_to_user(role: Role, user: User, db_session):
    user.roles.append(role)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
