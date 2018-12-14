from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


class User(BaseModel):
    username: str
    full_name: str = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    access_token: str = Body(...),
    q: str = None,
):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "access_token": access_token,
    }
    if q:
        results.update({"q": q})
    return results
