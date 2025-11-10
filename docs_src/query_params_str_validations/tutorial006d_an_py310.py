from fastapi import FastAPI, Query
from typing import Annotated, Optional

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[Optional[str], Query()] = ...):
    if q in ("None", "", "null"):
        q = None
    return {"q": q}
