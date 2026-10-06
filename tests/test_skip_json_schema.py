from typing import Annotated

import pytest
from fastapi import Body, Cookie, FastAPI, Form, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel
from pydantic.json_schema import SkipJsonSchema


class Item(BaseModel):
    visible: str
    hidden: SkipJsonSchema[int]


@pytest.fixture(params=[Body, Query, Form, Header, Cookie])
def client(request):
    app = FastAPI()

    @app.post("/items/")
    def echo(item: Annotated[Item, request.param()]):
        return item.model_dump()

    return TestClient(app), request.param


def test_openapi(client):
    test_client, source = client
    response = test_client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    operation = schema["paths"]["/items/"]["post"]
    if source in (Body, Form):
        item_schema = schema["components"]["schemas"]["Item"]
        assert item_schema == {
            "properties": {"visible": {"type": "string", "title": "Visible"}},
            "type": "object",
            "required": ["visible"],
            "title": "Item",
        }
    else:
        assert operation["parameters"] == [
            {
                "name": "visible",
                "in": source().in_.value,
                "required": True,
                "schema": {"type": "string", "title": "Visible"},
            }
        ]


def test_request(client):
    test_client, source = client
    payload = {"visible": "hello", "hidden": "42"}
    kwargs = {
        Body: {"json": payload},
        Query: {"params": payload},
        Form: {"data": payload},
        Header: {"headers": payload},
        Cookie: {"headers": {"cookie": "visible=hello; hidden=42"}},
    }[source]
    request = test_client.build_request("POST", "/items/", **kwargs)
    response = test_client.send(request)
    assert response.status_code == 200
    assert response.json() == {"visible": "hello", "hidden": 42}
