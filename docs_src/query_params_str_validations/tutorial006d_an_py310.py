from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query()] = ...):
    if q in ("None", "", "null"):
        q = None
    return {"q": q}
