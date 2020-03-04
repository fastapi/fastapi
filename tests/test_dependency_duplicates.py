import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

client = TestClient(app)


class Item(BaseModel):
    data: str


def duplicate_dependency(item: Item):
    return item


def dependency(item2: Item):
    return item2


@app.post("/with-duplicates")
async def with_duplicates(item: Item, item2: Item = Depends(duplicate_dependency)):
    return [item, item2]


@app.post("/no-duplicates")
async def no_duplicates(item: Item, item2: Item = Depends(dependency)):
    return [item, item2]


@pytest.mark.parametrize(
    "params,status_code,expected",
    [
        (
            {"item": {"data": "myitem"}},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "item2"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            {"item": {"data": "myitem"}, "item2": {"data": "myitem2"}},
            200,
            [{"data": "myitem"}, {"data": "myitem2"}],
        ),
    ],
)
def test_no_duplicates(params, status_code, expected):
    response = client.post("/no-duplicates", json=params)
    assert response.status_code == status_code
    assert response.json() == expected


def test_duplicates():
    response = client.post("/with-duplicates", json={"data": "myitem"})
    assert response.status_code == 200
    assert response.json() == [{"data": "myitem"}, {"data": "myitem"}]
