import uvicorn
from fastapi import FastAPI

app = FastAPI()

# Dynamic route
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Static route
@app.get("/items/stats")
async def read_stats():
    return {"status": "ok"}

if __name__ == '__main__':
    uvicorn.run('main:app')