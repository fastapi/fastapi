from typing import Dict

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Model(BaseModel):
    text: str


@app.get("/")
def f() -> Model:
    return Model(text="Looks and feels natural")


@app.get("/no_type")
def no_type():
    return Model(text="No type no life")


@app.get("/response_model_priority", response_model=Model)
def response_model_priority() -> Dict[str, str]:
    return Model(text="Backward compatible")


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/": {
            "get": {
                "summary": "F",
                "operationId": "f__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Model"}
                            }
                        },
                    }
                },
            }
        },
        "/no_type": {
            "get": {
                "summary": "No Type",
                "operationId": "no_type_no_type_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
        "/response_model_priority": {
            "get": {
                "summary": "Response Model Priority",
                "operationId": "response_model_priority_response_model_priority_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Model"}
                            }
                        },
                    }
                },
            }
        },
    },
    "components": {
        "schemas": {
            "Model": {
                "title": "Model",
                "type": "object",
                "properties": {"text": {"title": "Text", "type": "string"}},
                "required": ["text"],
            }
        }
    },
}

client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_get_api_route():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {"text": "Looks and feels natural"}


def test_get_api_route_no_return_type():
    response = client.get("/no_type")
    assert response.status_code == 200, response.text
    assert response.json() == {"text": "No type no life"}


def test_get_api_route_response_model_priority():
    response = client.get("/response_model_priority")
    assert response.status_code == 200, response.text
    assert response.json() == {"text": "Backward compatible"}
