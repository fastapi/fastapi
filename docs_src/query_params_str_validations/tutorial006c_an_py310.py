from typing import Annotated, Any

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(min_length=3)]):
    results: dict[str, Any] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results["q"] = q
    return results
