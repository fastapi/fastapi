from typing import List

from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel


class Address(BaseModel):
    first_line: str
    postcode: str


class User(BaseModel):
    first_name: str
    last_name: str
    address: List[Address]


app = FastAPI()


@app.post("/files/")
async def create_file(
    file: bytes = File(...),
    fileb: UploadFile = File(...),
    token: str = Form(...),
    user: User = Form(...),
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
        "user": user,
    }
