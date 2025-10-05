from fastapi.testclient import TestClient
from inline_snapshot import snapshot

from .main import app

client = TestClient(app)


def test_v1_to_v2_item():
    response = client.post(
        "/v1-to-v2/item",
        json={"title": "Test", "size": 10, "sub": {"name": "SubTest"}},
    )
    assert response.status_code == 200
    assert response.json() == {
        "new_title": "Test",
        "new_size": 10,
        "new_description": None,
        "new_sub": {"new_sub_name": "SubTest"},
        "new_multi": [],
    }


def test_v2_to_v1_item():
    response = client.post(
        "/v2-to-v1/item",
        json={
            "new_title": "NewTest",
            "new_size": 20,
            "new_sub": {"new_sub_name": "NewSubTest"},
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "title": "NewTest",
        "size": 20,
        "description": None,
        "sub": {"name": "NewSubTest"},
        "multi": [],
    }


def test_v1_to_v2_item_to_list():
    response = client.post(
        "/v1-to-v2/item-to-list",
        json={"title": "ListTest", "size": 30, "sub": {"name": "SubListTest"}},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "new_title": "ListTest",
            "new_size": 30,
            "new_description": None,
            "new_sub": {"new_sub_name": "SubListTest"},
            "new_multi": [],
        },
        {
            "new_title": "ListTest",
            "new_size": 30,
            "new_description": None,
            "new_sub": {"new_sub_name": "SubListTest"},
            "new_multi": [],
        },
    ]


def test_v1_to_v2_list_to_list():
    response = client.post(
        "/v1-to-v2/list-to-list",
        json=[
            {"title": "Item1", "size": 40, "sub": {"name": "Sub1"}},
            {"title": "Item2", "size": 50, "sub": {"name": "Sub2"}},
        ],
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "new_title": "Item1",
            "new_size": 40,
            "new_description": None,
            "new_sub": {"new_sub_name": "Sub1"},
            "new_multi": [],
        },
        {
            "new_title": "Item2",
            "new_size": 50,
            "new_description": None,
            "new_sub": {"new_sub_name": "Sub2"},
            "new_multi": [],
        },
    ]


def test_v1_to_v2_list_to_item():
    response = client.post(
        "/v1-to-v2/list-to-item",
        json=[
            {"title": "FirstItem", "size": 60, "sub": {"name": "FirstSub"}},
            {"title": "SecondItem", "size": 70, "sub": {"name": "SecondSub"}},
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        "new_title": "FirstItem",
        "new_size": 60,
        "new_description": None,
        "new_sub": {"new_sub_name": "FirstSub"},
        "new_multi": [],
    }


def test_v2_to_v1_item_to_list():
    response = client.post(
        "/v2-to-v1/item-to-list",
        json={
            "new_title": "ListNew",
            "new_size": 80,
            "new_sub": {"new_sub_name": "SubListNew"},
        },
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "ListNew",
            "size": 80,
            "description": None,
            "sub": {"name": "SubListNew"},
            "multi": [],
        },
        {
            "title": "ListNew",
            "size": 80,
            "description": None,
            "sub": {"name": "SubListNew"},
            "multi": [],
        },
    ]


def test_v2_to_v1_list_to_list():
    response = client.post(
        "/v2-to-v1/list-to-list",
        json=[
            {
                "new_title": "New1",
                "new_size": 90,
                "new_sub": {"new_sub_name": "NewSub1"},
            },
            {
                "new_title": "New2",
                "new_size": 100,
                "new_sub": {"new_sub_name": "NewSub2"},
            },
        ],
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "New1",
            "size": 90,
            "description": None,
            "sub": {"name": "NewSub1"},
            "multi": [],
        },
        {
            "title": "New2",
            "size": 100,
            "description": None,
            "sub": {"name": "NewSub2"},
            "multi": [],
        },
    ]


def test_v2_to_v1_list_to_item():
    response = client.post(
        "/v2-to-v1/list-to-item",
        json=[
            {
                "new_title": "FirstNew",
                "new_size": 110,
                "new_sub": {"new_sub_name": "FirstNewSub"},
            },
            {
                "new_title": "SecondNew",
                "new_size": 120,
                "new_sub": {"new_sub_name": "SecondNewSub"},
            },
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        "title": "FirstNew",
        "size": 110,
        "description": None,
        "sub": {"name": "FirstNewSub"},
        "multi": [],
    }


def test_v1_to_v2_list_to_item_empty():
    response = client.post("/v1-to-v2/list-to-item", json=[])
    assert response.status_code == 200
    assert response.json() == {
        "new_title": "",
        "new_size": 0,
        "new_description": None,
        "new_sub": {"new_sub_name": ""},
        "new_multi": [],
    }


def test_v2_to_v1_list_to_item_empty():
    response = client.post("/v2-to-v1/list-to-item", json=[])
    assert response.status_code == 200
    assert response.json() == {
        "title": "",
        "size": 0,
        "description": None,
        "sub": {"name": ""},
        "multi": [],
    }


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/v1-to-v2/item": {
                    "post": {
                        "summary": "Handle V1 Item To V2",
                        "operationId": "handle_v1_item_to_v2_v1_to_v2_item_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__Item"
                                            }
                                        ],
                                        "title": "Data",
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
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
                                        }
                                    }
                                },
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
                "/v2-to-v1/item": {
                    "post": {
                        "summary": "Handle V2 Item To V1",
                        "operationId": "handle_v2_item_to_v1_v2_to_v1_item_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
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
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__Item"
                                        }
                                    }
                                },
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
                "/v1-to-v2/item-to-list": {
                    "post": {
                        "summary": "Handle V1 Item To V2 List",
                        "operationId": "handle_v1_item_to_v2_list_v1_to_v2_item_to_list_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__Item"
                                            }
                                        ],
                                        "title": "Data",
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
                                            "items": {
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
                                            },
                                            "type": "array",
                                            "title": "Response Handle V1 Item To V2 List V1 To V2 Item To List Post",
                                        }
                                    }
                                },
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
                "/v1-to-v2/list-to-list": {
                    "post": {
                        "summary": "Handle V1 List To V2 List",
                        "operationId": "handle_v1_list_to_v2_list_v1_to_v2_list_to_list_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__Item"
                                        },
                                        "type": "array",
                                        "title": "Data",
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
                                            "items": {
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
                                            },
                                            "type": "array",
                                            "title": "Response Handle V1 List To V2 List V1 To V2 List To List Post",
                                        }
                                    }
                                },
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
                "/v1-to-v2/list-to-item": {
                    "post": {
                        "summary": "Handle V1 List To V2 Item",
                        "operationId": "handle_v1_list_to_v2_item_v1_to_v2_list_to_item_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__Item"
                                        },
                                        "type": "array",
                                        "title": "Data",
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
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
                                        }
                                    }
                                },
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
                "/v2-to-v1/item-to-list": {
                    "post": {
                        "summary": "Handle V2 Item To V1 List",
                        "operationId": "handle_v2_item_to_v1_list_v2_to_v1_item_to_list_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
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
                                            "items": {
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__Item"
                                            },
                                            "type": "array",
                                            "title": "Response Handle V2 Item To V1 List V2 To V1 Item To List Post",
                                        }
                                    }
                                },
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
                "/v2-to-v1/list-to-list": {
                    "post": {
                        "summary": "Handle V2 List To V1 List",
                        "operationId": "handle_v2_list_to_v1_list_v2_to_v1_list_to_list_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
                                        },
                                        "type": "array",
                                        "title": "Data",
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
                                            "items": {
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__Item"
                                            },
                                            "type": "array",
                                            "title": "Response Handle V2 List To V1 List V2 To V1 List To List Post",
                                        }
                                    }
                                },
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
                "/v2-to-v1/list-to-item": {
                    "post": {
                        "summary": "Handle V2 List To V1 Item",
                        "operationId": "handle_v2_list_to_v1_item_v2_to_v1_list_to_item_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
                                        },
                                        "type": "array",
                                        "title": "Data",
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
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__Item"
                                        }
                                    }
                                },
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
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
                    },
                    "ValidationError": {
                        "properties": {
                            "loc": {
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                                "type": "array",
                                "title": "Location",
                            },
                            "msg": {"type": "string", "title": "Message"},
                            "type": {"type": "string", "title": "Error Type"},
                        },
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                    },
                    "tests__test_pydantic_v1_v2_multifile__modelsv1__SubItem": {
                        "properties": {"name": {"type": "string", "title": "Name"}},
                        "type": "object",
                        "required": ["name"],
                        "title": "SubItem",
                    },
                    "tests__test_pydantic_v1_v2_multifile__modelsv1__Item": {
                        "properties": {
                            "title": {"type": "string", "title": "Title"},
                            "size": {"type": "integer", "title": "Size"},
                            "description": {"type": "string", "title": "Description"},
                            "sub": {
                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__SubItem"
                            },
                            "multi": {
                                "items": {
                                    "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__SubItem"
                                },
                                "type": "array",
                                "title": "Multi",
                                "default": [],
                            },
                        },
                        "type": "object",
                        "required": ["title", "size", "sub"],
                        "title": "Item",
                    },
                    "tests__test_pydantic_v1_v2_multifile__modelsv2__Item": {
                        "properties": {
                            "new_title": {"type": "string", "title": "New Title"},
                            "new_size": {"type": "integer", "title": "New Size"},
                            "new_description": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "title": "New Description",
                            },
                            "new_sub": {
                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__SubItem"
                            },
                            "new_multi": {
                                "items": {
                                    "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__SubItem"
                                },
                                "type": "array",
                                "title": "New Multi",
                                "default": [],
                            },
                        },
                        "type": "object",
                        "required": ["new_title", "new_size", "new_sub"],
                        "title": "Item",
                    },
                    "tests__test_pydantic_v1_v2_multifile__modelsv2__SubItem": {
                        "properties": {
                            "new_sub_name": {"type": "string", "title": "New Sub Name"}
                        },
                        "type": "object",
                        "required": ["new_sub_name"],
                        "title": "SubItem",
                    },
                }
            },
        }
    )
