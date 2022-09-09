import time
from typing import List

from fastapi import Depends, FastAPI, HTTPException

from . import crud, database, models, schemas
from .database import db_state_default

database.db.connect()
database.db.create_tables([models.User, models.Item])
database.db.close()

app = FastAPI()

sleep_time = 10


async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


@app.post("/users/", response_model=schemas.User, dependencies=[Depends(get_db)])
def create_user(user: schemas.UserCreate):
    if db_user := crud.get_user_by_email(email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(user=user)


@app.get("/users/", response_model=List[schemas.User], dependencies=[Depends(get_db)])
def read_users(skip: int = 0, limit: int = 100):
    return crud.get_users(skip=skip, limit=limit)


@app.get(
    "/users/{user_id}", response_model=schemas.User, dependencies=[Depends(get_db)]
)
def read_user(user_id: int):
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post(
    "/users/{user_id}/items/",
    response_model=schemas.Item,
    dependencies=[Depends(get_db)],
)
def create_item_for_user(user_id: int, item: schemas.ItemCreate):
    return crud.create_user_item(item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item], dependencies=[Depends(get_db)])
def read_items(skip: int = 0, limit: int = 100):
    return crud.get_items(skip=skip, limit=limit)


@app.get(
    "/slowusers/", response_model=List[schemas.User], dependencies=[Depends(get_db)]
)
def read_slow_users(skip: int = 0, limit: int = 100):
    global sleep_time
    sleep_time = max(0, sleep_time - 1)
    time.sleep(sleep_time)  # Fake long processing request
    return crud.get_users(skip=skip, limit=limit)
