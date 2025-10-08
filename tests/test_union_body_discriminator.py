from typing import Any, Dict, Union

from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, Field
from typing_extensions import Annotated, Literal

from .utils import needs_pydanticv1, needs_pydanticv2

app = FastAPI()


class FirstItem(BaseModel):
    value: Literal["first"]
    price: int


class OtherItem(BaseModel):
    value: Literal["other"]
    price: float


Item = Annotated[
    Union[FirstItem, OtherItem],
    Field(discriminator="value"),
]


@app.post("/items/")
def save_union_body_discriminator(
    item: Item, q: Annotated[str, Field(..., description="Query string")]
) -> Dict[str, Any]:
    return {"item": item}


client = TestClient(app)


@needs_pydanticv1
def test_openapi_schema_pydantic_v1() -> None:
    openapi = app.openapi()

    assert openapi["paths"]["/items/"]["post"]["requestBody"]["content"] == snapshot(
        {
            "application/json": {
                "schema": {
                    "anyOf": [
                        {"$ref": "#/components/schemas/FirstItem"},
                        {"$ref": "#/components/schemas/OtherItem"},
                    ],
                    "discriminator": {
                        "propertyName": "value",
                        "mapping": {
                            "first": "#/components/schemas/FirstItem",
                            "other": "#/components/schemas/OtherItem",
                        },
                    },
                    "title": "Item",
                }
            }
        }
    )


@needs_pydanticv2
def test_openapi_schema() -> None:
    openapi = app.openapi()

    assert openapi["paths"]["/items/"]["post"]["requestBody"]["content"] == snapshot(
        {
            "application/json": {
                "schema": {
                    "oneOf": [
                        {"$ref": "#/components/schemas/FirstItem"},
                        {"$ref": "#/components/schemas/OtherItem"},
                    ],
                    "discriminator": {
                        "propertyName": "value",
                        "mapping": {
                            "first": "#/components/schemas/FirstItem",
                            "other": "#/components/schemas/OtherItem",
                        },
                    },
                    "title": "Item",
                }
            }
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
