from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BeforeValidator

app = FastAPI()


def nullable_str(val: str) -> str | None:
    if val in ("None", "", "null"):
        return None
    return val


@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(min_length=3), BeforeValidator(nullable_str)],
):
    return {"q": q}
