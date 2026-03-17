from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int = Path(..., ge=1, le=1000)):
    return {"item_id": item_id}
