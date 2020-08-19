from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", **{"x-my-open-api-extension": "value"})
async def read_items():
    return [{"item_id": "Foo"}]
