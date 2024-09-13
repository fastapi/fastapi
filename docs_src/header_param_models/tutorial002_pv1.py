from typing import List, Union

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    class Config:
        extra = "forbid"

    host: str
    save_data: bool
    if_modified_since: Union[str, None] = None
    traceparent: Union[str, None] = None
    x_tag: List[str] = []


@app.get("/items/")
async def read_items(headers: CommonHeaders = Header()):
    return headers
