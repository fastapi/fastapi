from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, needy: str
):
    item = {"item_id": item_id, "owner_id": user_id, "needy": needy}
    return item
