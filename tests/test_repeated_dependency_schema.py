from fastapi import Depends, FastAPI, Header, status
from fastapi.testclient import TestClient

app = FastAPI()


def get_header(*, someheader: str = Header()):
    return someheader


def get_something_else(*, someheader: str = Depends(get_header)):
    return f"{someheader}123"


@app.get("/")
def get_deps(dep1: str = Depends(get_header), dep2: str = Depends(get_something_else)):
    return {"dep1": dep1, "dep2": dep2}


client = TestClient(app)

schema = {
    "components": {
        "schemas": {
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                        "title": "Detail",
                        "type": "array",
                    }
                },
                "title": "HTTPValidationError",
                "type": "object",
            },
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                        "title": "Location",
                        "type": "array",
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error " "Type", "type": "string"},
                },
                "required": ["loc", "msg", "type"],
                "title": "ValidationError",
                "type": "object",
            },
        }
    },
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "openapi": "3.0.2",
    "paths": {
        "/": {
            "get": {
                "operationId": "get_deps__get",
                "parameters": [
                    {
                        "in": "header",
                        "name": "someheader",
                        "required": True,
                        "schema": {"title": "Someheader", "type": "string"},
                    }
                ],
                "responses": {
                    "200": {
                        "content": {"application/json": {"schema": {}}},
                        "description": "Successful " "Response",
                    },
                    "422": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                        "description": "Validation " "Error",
                    },
                },
                "summary": "Get Deps",
            }
        }
    },
}


def test_schema():
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_200_OK
    actual_schema = response.json()
    assert actual_schema == schema
    assert (
        len(actual_schema["paths"]["/"]["get"]["parameters"]) == 1
    )  # primary goal of this test


def test_response():
    response = client.get("/", headers={"someheader": "hello"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"dep1": "hello", "dep2": "hello123"}
