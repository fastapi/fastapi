from fastapi import FastAPI, Cookie
from pydantic import BaseModel
from pydantic.types import UrlStr
from typing import Set, List

app = FastAPI()


@app.get("/items/")
async def read_items(*, ads_id: str = Cookie(None)):
    return {"ads_id": ads_id}
