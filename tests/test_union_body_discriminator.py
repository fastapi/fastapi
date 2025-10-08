from typing import Any, Dict, Union

from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, Discriminator, Tag
from typing_extensions import Annotated

app = FastAPI()


class FirstItem(BaseModel):
    value: str
    price: int


class OtherItem(BaseModel):
    value: str
    price: float


def get_discriminator_value(v: Any) -> str:
    return v.get("value")


Item = Annotated[
    Union[
        Annotated[FirstItem, Tag("first")],
        Annotated[OtherItem, Tag("other")],
    ],
    Discriminator(get_discriminator_value),
]


@app.post("/items/")
def save_union_body_discriminator(
    item: Item, q: Annotated[str, Tag("query")]
) -> Dict[str, Any]:
    return {"item": item}


client = TestClient(app)


def test_openapi_schema() -> None:
    openapi = app.openapi()

    assert openapi["paths"]["/items/"]["post"]["requestBody"] == snapshot(
        {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "oneOf": [
                            {"$ref": "#/components/schemas/FirstItem"},
                            {"$ref": "#/components/schemas/OtherItem"},
                        ],
                        "title": "Item",
                    }
                }
            },
        }
    )


def test_post_item() -> None:
    response = client.post("/items/?q=first", json={"value": "first", "price": 100})
    assert response.status_code == 200, response.text
    assert response.json() == {"item": {"value": "first", "price": 100}}


def test_post_other_item() -> None:
    response = client.post("/items/?q=other", json={"value": "other", "price": 100.5})
    assert response.status_code == 200, response.text
    assert response.json() == {"item": {"value": "other", "price": 100.5}}
