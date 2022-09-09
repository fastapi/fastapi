from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    return {"item_id": item_id, "q": q} if q else {"item_id": item_id}
