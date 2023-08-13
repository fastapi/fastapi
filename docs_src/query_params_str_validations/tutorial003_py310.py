from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
<<<<<<< HEAD
async def read_items(q: str | None = Query(default=None, min_length=3, max_length=50)):
=======
async def read_items(
    q: Optional[str] = Query(default=None, min_length=3, max_length=50)
):
>>>>>>> a1c1fa61f06a55ee077e7fa1c980d1eceb698091
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
