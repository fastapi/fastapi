from fastapi import FastAPI, Path
from fastapi.param_functions import Query
from typing_extensions import Annotated

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(item_id: Annotated[int, Path(gt=0)]):
    return {"item_id": item_id}


@app.get("/users")
async def read_users(user_id: Annotated[str, Query(min_length=1)] = "me"):
    return {"user_id": user_id}
