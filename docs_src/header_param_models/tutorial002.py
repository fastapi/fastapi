from typing import List, Union

from pydantic import BaseModel

from fastapi import FastAPI, Header

app = FastAPI()


class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modified_since: Union[str, None] = None
    traceparent: Union[str, None] = None
    x_tag: List[str] = []


@app.get("/items/")
async def read_items(headers: CommonHeaders = Header()):
    return headers
