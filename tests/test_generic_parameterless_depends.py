from typing import TypeVar

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from typing_extensions import Annotated

app = FastAPI()

T = TypeVar("T")

Dep = Annotated[T, Depends()]


class A:
    pass


class B:
    pass


@app.get("/a")
async def a(dep: Dep[A]):
    return {"cls": dep.__class__.__name__}


@app.get("/b")
async def b(dep: Dep[B]):
    return {"cls": dep.__class__.__name__}


client = TestClient(app)


def test_generic_parameterless_depends():
    response = client.get("/a")
    assert response.status_code == 200, response.text
    assert response.json() == {"cls": "A"}

    response = client.get("/b")
    assert response.status_code == 200, response.text
    assert response.json() == {"cls": "B"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "openapi": "3.1.0",
        "paths": {
            "/a": {
                "get": {
                    "operationId": "a_a_get",
                    "responses": {
                        "200": {
                            "content": {"application/json": {"schema": {}}},
                            "description": "Successful " "Response",
                        }
                    },
                    "summary": "A",
                }
            },
            "/b": {
                "get": {
                    "operationId": "b_b_get",
                    "responses": {
                        "200": {
                            "content": {"application/json": {"schema": {}}},
                            "description": "Successful " "Response",
                        }
                    },
                    "summary": "B",
                }
            },
        },
    }
