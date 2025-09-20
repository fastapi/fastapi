from typing import Optional

from fastapi import FastAPI
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing_extensions import Annotated

if PYDANTIC_V2:
    from pydantic import WithJsonSchema

app = FastAPI()


class Item(BaseModel):
    name: str

    if PYDANTIC_V2:
        description: Annotated[
            Optional[str], WithJsonSchema({"type": ["string", "null"]})
        ] = None

        model_config = {
            "json_schema_extra": {
                "x-something-internal": {"level": 4},
            }
        }
    else:
        description: Optional[str] = None  # type: ignore[no-redef]

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
        },
        "description": {
            "title": "Description",
            "type": ["string", "null"] if PYDANTIC_V2 else "string",
        },
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
    assert response.json() == {"name": "Foo item", "description": None}
