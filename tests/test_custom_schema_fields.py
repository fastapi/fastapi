from fastapi import FastAPI
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str

    if PYDANTIC_V2:
        model_config = {
            "json_schema_extra": {
                "x-something-internal": {"level": 4},
            }
        }
    else:

        class Config:
            schema_extra = {
                "x-something-internal": {"level": 4},
            }


@app.get("/foo", response_model=Item)
def foo():
    return {"name": "Foo item"}


client = TestClient(app)


item_schema = {
    "title": "Item",
    "required": ["name"],
    "type": "object",
    "x-something-internal": {
        "level": 4,
    },
    "properties": {
        "name": {
            "title": "Name",
            "type": "string",
        }
    },
}


def test_custom_response_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["components"]["schemas"]["Item"] == item_schema


def test_response():
    # For coverage
    response = client.get("/foo")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo item"}
