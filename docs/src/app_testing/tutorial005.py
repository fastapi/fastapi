from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from starlette.testclient import TestClient


class Item(BaseModel):
    my_string: str
    my_int: int


router = APIRouter()


@router.get("/routeA")
async def route_a(item: Item):
    return item


app = FastAPI()


app.include_router(router, prefix="/prefix")


def test_with_url_for():
    with TestClient(app) as client:
        item_dict = Item(my_string="a_string", my_int=10).dict()
        url = app.url_path_for("route_a")
        response = client.get(url, json=item_dict)
        assert response.status_code == 200
        assert response.json() == item_dict


def test_without_url_for():
    with TestClient(app) as client:
        item_dict = Item(my_string="a_string", my_int=10).dict()
        response = client.get("/prefix/routeA", json=item_dict)
        assert response.status_code == 200
        assert response.json() == item_dict
