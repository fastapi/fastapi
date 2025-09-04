from typing import Union

from pydantic import BaseModel, EmailStr

from fastapi import FastAPI

app = FastAPI()


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserIn(BaseUser):
    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user
