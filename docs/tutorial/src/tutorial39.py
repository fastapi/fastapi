from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel
from pydantic.types import UrlStr
from typing import Set, List

app = FastAPI()


class Image(BaseModel):
    url: UrlStr
    name: str


@app.post("/images/multiple/")
async def create_multiple_images(*, images: List[Image]):
    return images
