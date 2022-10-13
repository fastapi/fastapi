from typing import Union

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Union[list[str], None] = Query(default=None)):
    query_items = {"q": q}
    return query_items
