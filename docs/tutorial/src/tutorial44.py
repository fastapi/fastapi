from fastapi import FastAPI, Header
from pydantic import BaseModel
from pydantic.types import UrlStr
from typing import Set, List

app = FastAPI()


@app.get("/items/")
async def read_items(*, accept_encoding: str = Header(None)):
    return {"Accept-Encoding": accept_encoding}
