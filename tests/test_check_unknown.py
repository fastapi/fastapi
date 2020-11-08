from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app_no_check = FastAPI(check_unknown=False)

app_check = FastAPI(check_unknown=True)

client_no_check = TestClient(app_no_check)
client_check = TestClient(app_check)


class Item(BaseModel):
    data: str


@app_check.post("/with-check-unknown")
async def endpoint_check(item: Item, item2: Item):
    return [item, item2]


@app_no_check.post("/without-check-unknown")
async def endpoint_no_check(item: Item, item2: Item):
    return [item, item2]


def test_unknown_with_check():
    response = client_check.post(
        "/with-check-unknown",
        json={"item": {"data": "myitem"}, "item2": {"data": "item2"}, "data": "any"},
        params={"limit": 12},
    )
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "limit"],
                "msg": "extra fields not permitted",
                "type": "value_error.extra",
            },
            {
                "loc": ["body", "data"],
                "msg": "extra fields not permitted",
                "type": "value_error.extra",
            },
        ]
    }


def test_known_with_check():
    response = client_check.post(
        "/with-check-unknown",
        json={"item": {"data": "myitem"}, "item2": {"data": "item2"}},
    )
    assert response.status_code == 200, response.text
    assert response.json() == [{"data": "myitem"}, {"data": "item2"}]


def test_unknown_without_check():
    response = client_no_check.post(
        "/without-check-unknown",
        json={"item": {"data": "myitem"}, "item2": {"data": "item2"}, "data": "any"},
        params={"limit": 12},
    )
    assert response.status_code == 200, response.text
    assert response.json() == [{"data": "myitem"}, {"data": "item2"}]
