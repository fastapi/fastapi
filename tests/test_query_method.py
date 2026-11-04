from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


@app.query("/items/")
def query_items(item: Item):
    return {"method": "QUERY", "item": item}


@app.api_route("/api-route/", methods=["QUERY"])
def api_route_query():
    return {"method": "QUERY", "source": "api_route"}


router = APIRouter()


@router.query("/router/")
def router_query():
    return {"method": "QUERY", "source": "router"}


app.include_router(router)

client = TestClient(app)


def test_app_query_with_body():
    body = {"name": "Foo", "price": 5.5}
    response = client.request("QUERY", "/items/", json=body)
    assert response.status_code == 200, response.text
    assert response.json() == {"method": "QUERY", "item": body}


def test_router_query():
    response = client.request("QUERY", "/router/")
    assert response.status_code == 200, response.text
    assert response.json() == {"method": "QUERY", "source": "router"}


def test_api_route_query():
    response = client.request("QUERY", "/api-route/")
    assert response.status_code == 200, response.text
    assert response.json() == {"method": "QUERY", "source": "api_route"}


def test_get_is_not_allowed():
    response = client.get("/items/")
    assert response.status_code == 405, response.text
    assert "QUERY" in response.headers["allow"]
