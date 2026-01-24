from typing import Annotated, Union

from fastapi import FastAPI, Query
from pydantic import BeforeValidator

app = FastAPI()


def nullable_str(val: str) -> Union[str, None]:
    if val in ("None", "", "null"):
        return None
    return val


@app.get("/items/")
async def read_items(
    q: Annotated[Union[str, None], Query(min_length=3), BeforeValidator(nullable_str)],
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
