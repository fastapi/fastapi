from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class ResponseModelA(BaseModel):
    a: str


class ResponseModelB(BaseModel):
    b: str


@app.get("/a", response_model=ResponseModelA)
def get_a_with_response_model():
    return ResponseModelA(a="a")


@app.get("/b", response_model=ResponseModelA)
def get_b_with_response_model() -> ResponseModelB:
    return ResponseModelA(a="a")


@app.get("/c")
def get_c_with_return_type() -> ResponseModelB:
    return ResponseModelB(b="b")


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/a": {
            "get": {
                "summary": "Get A With Response Model",
                "operationId": "get_a_with_response_model_a_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ResponseModelA"
                                }
                            }
                        },
                    }
                },
            }
        },
        "/b": {
            "get": {
                "summary": "Get B With Response Model",
                "operationId": "get_b_with_response_model_b_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ResponseModelA"
                                }
                            }
                        },
                    }
                },
            }
        },
        "/c": {
            "get": {
                "summary": "Get C With Return Type",
                "operationId": "get_c_with_return_type_c_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ResponseModelB"
                                }
                            }
                        },
                    }
                },
            }
        },
    },
    "components": {
        "schemas": {
            "ResponseModelA": {
                "title": "ResponseModelA",
                "required": ["a"],
                "type": "object",
                "properties": {"a": {"title": "A", "type": "string"}},
            },
            "ResponseModelB": {
                "title": "ResponseModelB",
                "required": ["b"],
                "type": "object",
                "properties": {"b": {"title": "B", "type": "string"}},
            },
        }
    },
}


client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_response_model_a():
    response = client.get("/a")
    assert response.status_code == 200, response.text
    assert response.json() == {"a": "a"}
    assert ResponseModelA(**response.json())


def test_response_model_takes_precedence():
    response = client.get("/b")
    assert response.status_code == 200, response.text
    assert response.json() == {"a": "a"}
    assert ResponseModelA(**response.json())


def test_response_model_from_return_type():
    response = client.get("/c")
    assert response.status_code == 200, response.text
    assert response.json() == {"b": "b"}
    assert ResponseModelB(**response.json())
