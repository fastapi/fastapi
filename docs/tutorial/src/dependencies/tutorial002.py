from pydantic import BaseModel

from fastapi import Depends, FastAPI

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams(BaseModel):
    q: str = None
    skip: int = None
    limit: int = None


async def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return CommonQueryParams(q=q, skip=skip, limit=limit)


@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(common_parameters)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.limit]
    response.update({"items": items})
    return response
