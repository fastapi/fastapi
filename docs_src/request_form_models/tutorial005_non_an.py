from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class Profile(BaseModel):
    name: str
    age: int


@app.post("/profiles/")
async def create_profile(
    token: str = Form(),
    profile: Profile | None = Form(default=None),
):
    return {"token": token, "profile": profile}
