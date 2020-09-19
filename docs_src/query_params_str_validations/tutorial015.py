from typing import List

from fastapi import FastAPI, Query, QueryStyle

app = FastAPI()


@app.get("/items/")
async def read_items(
    q: List[str] = Query(
        ["foo", "bar"],
        explode=False,
        style=QueryStyle.pipe_delimited,
    )
):
    query_items = {"q": q}
    return query_items
