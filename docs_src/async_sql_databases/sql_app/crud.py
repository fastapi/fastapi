from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_user(db: AsyncSession, user_id: int):
    db_execute = await db.execute(select(models.User).where(models.User.id == user_id))
    return db_execute.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    db_execute = await db.execute(select(models.User).where(models.User.email == email))
    return db_execute.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_execute = await db.execute(select(models.User).offset(skip).limit(limit))
    return db_execute.scalars().all()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_execute = await db.execute(select(models.User).where(models.User.id == user_id))
    db_user = db_execute.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(db_user)
    await db.commit()


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_execute = await db.execute(select(models.Item).offset(skip).limit(limit))
    return db_execute.scalars().all()


async def create_user_item(db: AsyncSession, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
