from typing import List

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(q: List[str]):
    query_items = {"q": q}
    return query_items
