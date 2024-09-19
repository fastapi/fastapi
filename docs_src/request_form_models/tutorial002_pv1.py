from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class FormData(BaseModel):
    username: str
    password: str

    class Config:
        extra = "forbid"


@app.post("/login/")
async def login(data: FormData = Form()):
    return data
