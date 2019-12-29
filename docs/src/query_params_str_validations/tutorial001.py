from fastapi import FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(q: str = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q is not None and len(q) > 0:
        results.update({"q": q})
    return results
