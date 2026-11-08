from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class Profile(BaseModel):
    name: str
    age: int


@app.post("/profiles/")
async def create_profile(
    token: Annotated[str, Form()],
    profile: Annotated[Profile | None, Form()] = None,
):
    return {"token": token, "profile": profile}
