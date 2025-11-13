from fastapi import FastAPI, File, Form
from pydantic import BaseModel
from typing_extensions import Annotated

app = FastAPI()


class FormData(BaseModel):
    username: str
    password: str
    avatar: bytes = File()


@app.post("/users/")
async def create_user(data: Annotated[FormData, Form()]):
    return {
        "username": data.username,
        "password": data.password,
        "avatar_file_size": len(data.avatar),
    }
