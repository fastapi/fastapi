from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.types import UrlStr

app = FastAPI()


class Image(BaseModel):
    url: UrlStr
    name: str


@app.post("/images/multiple/")
async def create_multiple_images(*, images: List[Image]):
    return images
