from fastapi import FastAPI
from starlette.responses import UJSONResponse

app = FastAPI()


@app.get("/items/", content_type=UJSONResponse)
async def read_items():
    return [{"item_id": "Foo"}]
