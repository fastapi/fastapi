from fastapi import Body, FastAPI, Path, Query, Form
from pydantic import BaseModel
from pydantic.types import EmailStr
from typing import Set, List

app = FastAPI()


@app.post("/login/")
async def login(*, username: str = Form(...), password: str = Form(...)):
    return {"username": username}
