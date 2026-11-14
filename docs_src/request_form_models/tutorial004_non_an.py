from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel

app = FastAPI()


class Profile(BaseModel):
    name: str


@app.post("/profiles/")
async def create_profile(profile: Profile = Form(), avatar: UploadFile = File()):
    return {"profile": profile, "filename": avatar.filename}
