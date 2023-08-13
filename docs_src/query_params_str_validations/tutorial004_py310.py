from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
<<<<<<< HEAD
    q: str
    | None = Query(default=None, min_length=3, max_length=50, pattern="^fixedquery$")
=======
    q: Optional[str] = Query(
        default=None, min_length=3, max_length=50, pattern="^fixedquery$"
    )
>>>>>>> a1c1fa61f06a55ee077e7fa1c980d1eceb698091
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
