from fastapi import FastAPI, HTTPException, Response, Request

from . import models, schemas
from .storage import Storage
from .database import session_factory, session_var, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    with session_factory() as session:
        session_var.set(session)
        response = await call_next(request)
    return response


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    db_user = Storage.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return Storage.create_user(user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int):
    db_user = Storage.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
