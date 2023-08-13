<<<<<<< HEAD
=======
from typing import Optional

>>>>>>> a1c1fa61f06a55ee077e7fa1c980d1eceb698091
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user
