from fastapi import Body, FastAPI
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}


@app.put("/items/{item_id}")
async def upsert_item(item_id: str, name: str = Body(None), size: int = Body(None)):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=HTTP_201_CREATED, content=item)
