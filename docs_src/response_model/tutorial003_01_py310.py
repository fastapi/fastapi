from typing import Optional

from pydantic import BaseModel, EmailStr

from fastapi import FastAPI

app = FastAPI()


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn(BaseUser):
    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user
