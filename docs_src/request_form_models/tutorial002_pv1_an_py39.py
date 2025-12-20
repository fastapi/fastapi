from typing import Annotated

from fastapi import FastAPI
from fastapi.temp_pydantic_v1_params import Form
from pydantic.v1 import BaseModel

app = FastAPI()


class FormData(BaseModel):
    username: str
    password: str

    class Config:
        extra = "forbid"


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
