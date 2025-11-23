from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(min_length=3)]):
    # q is REQUIRED, but can be None if client sends ?q=null
    if q == "null":
        q = None
    results = {"items": [{"item_id": "Foo"}]}
    if q is not None:
        results.update({"q": q})
    return results
