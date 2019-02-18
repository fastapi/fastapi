from typing import List

from pydantic import BaseModel
from pydantic.types import UrlStr

from fastapi import FastAPI

app = FastAPI()


class Image(BaseModel):
    url: UrlStr
    name: str


@app.post("/images/multiple/")
async def create_multiple_images(*, images: List[Image]):
    return images
