from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel
from pydantic.types import EmailStr
from typing import Set, List

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str = None
    


# Don't do this in production!
@app.post("/user/", response_model=UserIn)
async def create_user(*, user: UserIn):
    return user
