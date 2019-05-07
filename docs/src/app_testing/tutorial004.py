from fastapi import FastAPI
from pydantic import BaseModel
from starlette.testclient import TestClient

app = FastAPI()


class Item(BaseModel):
    my_string: str
    my_int: int


@app.post("/create_item")
async def create_item(item: Item):
    return item


def test_read_items():
    with TestClient(app) as client:
        item_dict = Item(my_string="a_string", my_int=10).dict()
        response = client.post("/create_item", json=item_dict)
        assert response.status_code == 200
        assert response.json() == item_dict
