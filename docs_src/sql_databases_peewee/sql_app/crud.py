from . import models, schemas


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return models.User.filter(models.User.email == email).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_user(user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db_user.save()
    return db_user


def get_items(skip: int = 0, limit: int = 100):
    return list(models.Item.select().offset(skip).limit(limit))


def create_user_item(item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db_item.save()
    return db_item
