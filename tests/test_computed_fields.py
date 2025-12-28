import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(name="client")
def get_client(request):
    separate_input_output_schemas = request.param
    app = FastAPI(separate_input_output_schemas=separate_input_output_schemas)

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

    @app.get("/responses", responses={200: {"model": Rectangle}})
    def read_responses() -> Rectangle:
        return Rectangle(width=3, length=4)

    client = TestClient(app)
    return client


@pytest.mark.parametrize("client", [True, False], indirect=True)
@pytest.mark.parametrize("path", ["/", "/responses"])
def test_get(client: TestClient, path: str):
    response = client.get(path)
    assert response.status_code == 200, response.text
    assert response.json() == {"width": 3, "length": 4, "area": 12}


@pytest.mark.parametrize("client", [True, False], indirect=True)
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
            },
            "/responses": {
                "get": {
                    "summary": "Read Responses",
                    "operationId": "read_responses_responses_get",
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
            },
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
