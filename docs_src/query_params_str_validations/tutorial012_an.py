from typing import List

from fastapi import FastAPI, Query
from typing_extensions import Annotated

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[List[str], Query()] = None):
    if q is None:
        q = ["foo", "bar"]
    query_items = {"q": q}
    return query_items
