from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Model(BaseModel):
    pass


class Model2(BaseModel):
    a: Model


class Model3(BaseModel):
    c: Model
    d: Model2


@app.get("/", response_model=Model3)
def f():
    return {"c": {}, "d": {"a": {}}}


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
                                "schema": {"$ref": "#/components/schemas/Model3"}
                            }
                        },
                    }
                },
            }
        }
    },
    "components": {
        "schemas": {
            "Model": {"title": "Model", "type": "object", "properties": {}},
            "Model2": {
                "title": "Model2",
                "required": ["a"],
                "type": "object",
                "properties": {"a": {"$ref": "#/components/schemas/Model"}},
            },
            "Model3": {
                "title": "Model3",
                "required": ["c", "d"],
                "type": "object",
                "properties": {
                    "c": {"$ref": "#/components/schemas/Model"},
                    "d": {"$ref": "#/components/schemas/Model2"},
                },
            },
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
    assert response.json() == {"c": {}, "d": {"a": {}}}
