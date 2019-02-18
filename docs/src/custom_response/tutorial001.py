from starlette.responses import UJSONResponse

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", content_type=UJSONResponse)
async def read_items():
    return [{"item_id": "Foo"}]
