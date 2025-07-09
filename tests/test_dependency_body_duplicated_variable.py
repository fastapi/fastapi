from typing import Awaitable, Callable, List
from unittest.mock import ANY

from fastapi import Body, Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


def make_field(name: str) -> Callable[..., Awaitable[str]]:
    async def inner(value: str = Body(..., alias=name)) -> str:
        return value

    return inner


@app.post("/example")
def example(
    field_0: str = Body(...),
    field_1_: str = Body(..., alias="field_1"),
    field_2_: str = Depends(make_field("field_2")),
    field_3_: str = Depends(make_field("field_3")),
) -> List[str]:
    return [field_0, field_1_, field_2_, field_3_]


openapi_schema = {
    "openapi": "3.1.0",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/example": {
            "post": {
                "summary": "Example",
                "operationId": "example_example_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_example_example_post"
                            }
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Example Example Post",
                                    "type": "array",
                                    "items": {"type": "string"},
                                }
                            }
                        },
                    },
                    "422": ANY,
                },
            }
        }
    },
    "components": {
        "schemas": {
            "Body_example_example_post": {
                "title": "Body_example_example_post",
                "type": "object",
                "properties": {
                    "field_0": {"title": "Field 0", "type": "string"},
                    "field_1": {"title": "Field 1", "type": "string"},
                    "field_2": {"title": "Field 2", "type": "string"},
                    "field_3": {"title": "Field 3", "type": "string"},
                },
                "required": ["field_0", "field_1", "field_2", "field_3"],
            },
            "HTTPValidationError": ANY,
            "ValidationError": ANY,
        }
    },
}


client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_valid():
    response = client.post(
        "/example/",
        json={"field_0": "a", "field_1": "b", "field_2": "c", "field_3": "d"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == ["a", "b", "c", "d"]


def test_missing():
    response = client.post("/example/", json={})
    assert response.status_code == 422, response.text
    resp_json = response.json()
    assert len(resp_json["detail"]) == 4
    assert resp_json["detail"][0]["loc"] == ["body", "field_2"]
    assert str(resp_json["detail"][0]["msg"]).lower() == "field required"
    assert resp_json["detail"][1]["loc"] == ["body", "field_3"]
    assert str(resp_json["detail"][1]["msg"]).lower() == "field required"
    assert resp_json["detail"][2]["loc"] == ["body", "field_0"]
    assert str(resp_json["detail"][2]["msg"]).lower() == "field required"
    assert resp_json["detail"][3]["loc"] == ["body", "field_1"]
    assert str(resp_json["detail"][3]["msg"]).lower() == "field required"
