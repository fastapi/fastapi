from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class Profile(BaseModel):
    name: str


class Preferences(BaseModel):
    tags: list[str] = []


@app.post("/profiles/")
async def create_profile(
    profile: Profile = Form(),
    preferences: Preferences = Form(),
    token: str = Form(),
):
    return {"profile": profile, "preferences": preferences, "token": token}
