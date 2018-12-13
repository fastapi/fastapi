from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", deprecated=True)
async def read_items():
    return [{"item_id": "Foo"}]
