from fastapi import FastAPI
from uuid import UUID

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: UUID):
    return {"item_id": item_id}
