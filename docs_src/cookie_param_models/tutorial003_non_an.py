from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Preferences(BaseModel):
    theme: str
    locale: str


@app.get("/items/")
async def read_items(preferences: Preferences | None = Cookie(default=None)):
    return preferences
