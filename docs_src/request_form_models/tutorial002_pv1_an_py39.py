from typing import Annotated

from pydantic import BaseModel

from fastapi import FastAPI, Form

app = FastAPI()


class FormData(BaseModel):
    username: str
    password: str

    class Config:
        extra = "forbid"


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
