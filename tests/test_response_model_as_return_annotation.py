from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class ModelOne(BaseModel):
    name: str


class ModelTwo(BaseModel):
    surname: str


app = FastAPI()


@app.get("/valid1")
def valid1() -> ModelOne:
    return ModelOne(name="Test")


@app.get("/valid2", response_model=ModelTwo)
def valid2():
    return ModelTwo(surname="Test")


@app.get("/valid3", response_model=ModelTwo)
def valid3() -> ModelOne:
    return ModelTwo(surname="Test")


@app.get("/valid4")
def valid4() -> "ModelOne":
    return ModelOne(name="Test")


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/valid1": {
            "get": {
                "summary": "Valid1",
                "operationId": "valid1_valid1_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ModelOne"}
                            }
                        },
                    }
                },
            }
        },
        "/valid2": {
            "get": {
                "summary": "Valid2",
                "operationId": "valid2_valid2_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ModelTwo"}
                            }
                        },
                    }
                },
            }
        },
        "/valid3": {
            "get": {
                "summary": "Valid3",
                "operationId": "valid3_valid3_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ModelTwo"}
                            }
                        },
                    }
                },
            }
        },
        "/valid4": {
            "get": {
                "summary": "Valid4",
                "operationId": "valid4_valid4_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ModelOne"}
                            }
                        },
                    }
                },
            }
        },
    },
    "components": {
        "schemas": {
            "ModelOne": {
                "title": "ModelOne",
                "required": ["name"],
                "type": "object",
                "properties": {"name": {"title": "Name", "type": "string"}},
            },
            "ModelTwo": {
                "title": "ModelTwo",
                "required": ["surname"],
                "type": "object",
                "properties": {"surname": {"title": "Surname", "type": "string"}},
            },
        }
    },
}

client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_path_operations():
    response = client.get("/valid1")
    assert response.status_code == 200, response.text
    response = client.get("/valid2")
    assert response.status_code == 200, response.text
    response = client.get("/valid3")
    assert response.status_code == 200, response.text
    response = client.get("/valid4")
    assert response.status_code == 200, response.text
