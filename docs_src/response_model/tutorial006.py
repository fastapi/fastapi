from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Video(BaseModel):
    url: HttpUrl
    duration: int


class Item(BaseModel):
    name: str
    image: Optional[Image] = None
    videos: Optional[List[Video]] = None


items = {
    "foo": {
        "name": "Foo",
        "image": {"url": "http://test.com/img.jpg", "name": "Some image"},
        "videos": [
            {"url": "http://test.com/video_1.mp4", "duration": 40},
            {"url": "http://test.com/video_2.mp4", "duration": 120},
        ],
    },
}


@app.get(
    "/items/{item_id}/image_name",
    response_model=Item,
    response_model_exclude={"image": {"url"}, "videos": ...},
)
async def read_item_image_name(item_id: str):
    # Returns name of item and name of image
    return items[item_id]


@app.get(
    "/items/{item_id}/image",
    response_model=Item,
    response_model_include={"name": ..., "image": {"url"}},
)
async def read_item_image(item_id: str):
    # Returns name of item and url of image
    return items[item_id]


@app.get(
    "/items/{item_id}/first_video",
    response_model=Item,
    response_model_include={"name": ..., "videos": {0: ...}},
)
async def read_item_first_video(item_id: str):
    # Returns name of item and full info for first video
    return items[item_id]


@app.get(
    "/items/{item_id}/videos",
    response_model=Item,
    response_model_include={"name": ..., "videos": {"__all__": {"url"}}},
)
async def read_item_videos(item_id: str):
    # Returns name of item and url for all videos
    return items[item_id]
