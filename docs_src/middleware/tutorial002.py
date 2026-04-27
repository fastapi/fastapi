from fastapi import FastAPI
from fastapi.middleware.timing import TimingMiddleware

app = FastAPI()

app.add_middleware(TimingMiddleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
