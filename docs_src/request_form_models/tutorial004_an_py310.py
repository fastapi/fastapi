from typing import Annotated

from fastapi import FastAPI, Form, UploadFile
from pydantic import BaseModel

app = FastAPI()


class Profile(BaseModel):
    name: str


@app.post("/profiles/")
async def create_profile(profile: Annotated[Profile, Form()], avatar: UploadFile):
    return {"profile": profile, "filename": avatar.filename}
