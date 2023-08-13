from fastapi import FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(q=None):
    if q is None:
        q = ["foo", "bar"]
    query_items = {"q": q}
    return query_items
