from typing import Optional

from fastapi import Depends, FastAPI
from typing_extensions import Annotated

app = FastAPI()


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


CommonParamsDepends = Annotated[dict, Depends(common_parameters)]


@app.get("/items/")
async def read_items(commons: CommonParamsDepends):
    return commons
