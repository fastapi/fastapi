from typing import List, Set

from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel
from pydantic.types import UrlStr
from starlette.status import HTTP_201_CREATED
from starlette.responses import UJSONResponse

app = FastAPI()


@app.get("/items/", content_type=UJSONResponse)
async def read_items():
    return [{"item_id": "Foo"}]
