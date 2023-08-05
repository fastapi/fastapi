import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from .utils import needs_pydanticv2


@pytest.fixture(name="client")
def get_client():
    app = FastAPI()

    from pydantic import BaseModel, computed_field

    class Rectangle(BaseModel):
        width: int
        length: int

        @computed_field
        @property
        def area(self) -> int:
            return self.width * self.length

    @app.get("/")
    def read_root() -> Rectangle:
        return Rectangle(width=3, length=4)

    client = TestClient(app)
    return client


@needs_pydanticv2
def test_get(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {"width": 3, "length": 4, "area": 12}


@needs_pydanticv2
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "get": {
                    "summary": "Read Root",
                    "operationId": "read_root__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Rectangle"}
                                }
                            },
                        }
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "Rectangle": {
                    "properties": {
                        "width": {"type": "integer", "title": "Width"},
                        "length": {"type": "integer", "title": "Length"},
                        "area": {"type": "integer", "title": "Area", "readOnly": True},
                    },
                    "type": "object",
                    "required": ["width", "length", "area"],
                    "title": "Rectangle",
                }
            }
        },
    }
