from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: str = Query(..., min_length=3)):
    results = {"q": q, "items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    return results
