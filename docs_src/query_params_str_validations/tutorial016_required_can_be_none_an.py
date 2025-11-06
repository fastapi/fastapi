from typing import Union

from fastapi import FastAPI, Query
from typing_extensions import Annotated

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[Union[str, None], Query(min_length=3)] = ...):
    """
    Example of a required query parameter that can be None.

    The parameter 'q' is required (must be provided by the client)
    but can explicitly be set to None by passing "null" as string.

    - If q is provided and valid: returns items filtered by q
    - If q is "null": treats it as None and returns all items
    - If q is missing: returns 422 validation error (required parameter)
    - If q is too short: returns 422 validation error (min_length=3)
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}

    # Handle explicit None case
    if q == "null":
        q = None

    if q is not None:
        results.update({"q": q, "filtered": True})
    else:
        results.update({"q": None, "filtered": False})

    return results
