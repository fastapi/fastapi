from typing import List

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

client = TestClient(app)


class Item(BaseModel):
    data: str


def duplicate_dependency(item: Item):
    return item


def dependency(item2: Item):
    return item2


def sub_duplicate_dependency(
    item: Item, sub_item: Item = Depends(duplicate_dependency)
):
    return [item, sub_item]


@app.post("/with-duplicates")
async def with_duplicates(item: Item, item2: Item = Depends(duplicate_dependency)):
    return [item, item2]


@app.post("/no-duplicates")
async def no_duplicates(item: Item, item2: Item = Depends(dependency)):
    return [item, item2]


@app.post("/with-duplicates-sub")
async def no_duplicates_sub(
    item: Item, sub_items: List[Item] = Depends(sub_duplicate_dependency)
):
    return [item, sub_items]


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/with-duplicates": {
            "post": {
                "summary": "With Duplicates",
                "operationId": "with_duplicates_with_duplicates_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Item"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/no-duplicates": {
            "post": {
                "summary": "No Duplicates",
                "operationId": "no_duplicates_no_duplicates_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_no_duplicates_no_duplicates_post"
                            }
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/with-duplicates-sub": {
            "post": {
                "summary": "No Duplicates Sub",
                "operationId": "no_duplicates_sub_with_duplicates_sub_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Item"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
    },
    "components": {
        "schemas": {
            "Body_no_duplicates_no_duplicates_post": {
                "title": "Body_no_duplicates_no_duplicates_post",
                "required": ["item", "item2"],
                "type": "object",
                "properties": {
                    "item": {"$ref": "#/components/schemas/Item"},
                    "item2": {"$ref": "#/components/schemas/Item"},
                },
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                    }
                },
            },
            "Item": {
                "title": "Item",
                "required": ["data"],
                "type": "object",
                "properties": {"data": {"title": "Data", "type": "string"}},
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": ["loc", "msg", "type"],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_no_duplicates_invalid():
    response = client.post("/no-duplicates", json={"item": {"data": "myitem"}})
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "item2"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_no_duplicates():
    response = client.post(
        "/no-duplicates",
        json={"item": {"data": "myitem"}, "item2": {"data": "myitem2"}},
    )
    assert response.status_code == 200, response.text
    assert response.json() == [{"data": "myitem"}, {"data": "myitem2"}]


def test_duplicates():
    response = client.post("/with-duplicates", json={"data": "myitem"})
    assert response.status_code == 200, response.text
    assert response.json() == [{"data": "myitem"}, {"data": "myitem"}]


def test_sub_duplicates():
    response = client.post("/with-duplicates-sub", json={"data": "myitem"})
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"data": "myitem"},
        [{"data": "myitem"}, {"data": "myitem"}],
    ]
