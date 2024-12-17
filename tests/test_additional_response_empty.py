from typing import Dict

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Items(BaseModel):
    items: Dict[str, int]


@app.post("/foo", responses={422: {}})
def foo(items: Items):
    pass  # pragma: no cover


client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/foo": {
            "post": {
                "summary": "Foo",
                "operationId": "foo_foo_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Items"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        }
    },
    "components": {
        "schemas": {
            "Items": {
                "title": "Items",
                "required": ["items"],
                "type": "object",
                "properties": {
                    "items": {
                        "title": "Items",
                        "type": "object",
                        "additionalProperties": {"type": "integer"},
                    }
                },
            }
        }
    },
}


def test_additional_properties_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema
