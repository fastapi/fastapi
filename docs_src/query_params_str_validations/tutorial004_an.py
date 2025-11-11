from typing import Any, Union

from fastapi import FastAPI, Query
from typing_extensions import Annotated

app = FastAPI()


@app.get("/items/")
async def read_items(
    q: Annotated[
        Union[str, None], Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,
):
    results: dict[str, Any] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results["q"] = q
    return results
