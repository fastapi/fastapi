import json

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


data = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
}


def set_username():
    response = yield
    response.headers["X-Username"] = json.loads(response.body)["owner"]


@app.get("/items/{item_id}", dependencies=[Depends(set_username)])
def get_item(item_id: str):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    return data[item_id]
