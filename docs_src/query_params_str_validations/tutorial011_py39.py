from typing import Optional

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Optional[list[str]] = Query(None)):
    query_items = {"q": q}
    return query_items
