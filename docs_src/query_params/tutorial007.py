from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_user_item(item_id: str, limit: Optional[int] = None):
    item = {"item_id": item_id, "limit": limit}
    return item
