from fastapi import FastAPI, Header
from pydantic import BaseModel
from pydantic.types import UrlStr
from typing import Set, List

app = FastAPI()


@app.get("/items/")
async def read_items(*, strange_header: str = Header(None, convert_underscores=False)):
    return {"strange_header": strange_header}
