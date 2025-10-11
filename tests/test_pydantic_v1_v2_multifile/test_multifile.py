import sys

from tests.utils import pydantic_snapshot, skip_module_if_py_gte_314

if sys.version_info >= (3, 14):
    skip_module_if_py_gte_314()

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


def test_v2_same_name_to_v1():
    response = client.post(
        "/v2-to-v1/same-name",
        json={
            "item1": {
                "new_title": "Title1",
                "new_size": 100,
                "new_description": "Description1",
                "new_sub": {"new_sub_name": "Sub1"},
                "new_multi": [{"new_sub_name": "Multi1"}],
            },
            "item2": {
                "dup_title": "Title2",
                "dup_size": 200,
                "dup_description": "Description2",
                "dup_sub": {"dup_sub_name": "Sub2"},
                "dup_multi": [
                    {"dup_sub_name": "Multi2a"},
                    {"dup_sub_name": "Multi2b"},
                ],
            },
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "title": "Title1",
        "size": 200,
        "description": "Description1",
        "sub": {"name": "Sub1"},
        "multi": [{"name": "Multi2a"}, {"name": "Multi2b"}],
    }


def test_v2_items_in_list_to_v1_item_in_list():
    response = client.post(
        "/v2-to-v1/list-of-items-to-list-of-items",
        json={
            "data1": [{"name2": "Item1"}, {"name2": "Item2"}],
            "data2": [{"dup_name2": "Item3"}, {"dup_name2": "Item4"}],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"name1": "Item1"},
        {"name1": "Item3"},
    ]


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
                                    "schema": pydantic_snapshot(
                                        v2=snapshot(
                                            {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__Item"
                                                    }
                                                ],
                                                "title": "Data",
                                            }
                                        ),
                                        v1=snapshot(
                                            {
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__Item"
                                            }
                                        ),
                                    )
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
                                    "schema": pydantic_snapshot(
                                        v2=snapshot(
                                            {
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item-Input"
                                            }
                                        ),
                                        v1=snapshot(
                                            {
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
                                            }
                                        ),
                                    ),
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
                                    "schema": pydantic_snapshot(
                                        v2=snapshot(
                                            {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__Item"
                                                    }
                                                ],
                                                "title": "Data",
                                            }
                                        ),
                                        v1=snapshot(
                                            {
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__Item"
                                            }
                                        ),
                                    )
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
                                    "schema": pydantic_snapshot(
                                        v2=snapshot(
                                            {
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item-Input"
                                            }
                                        ),
                                        v1=snapshot(
                                            {
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
                                            }
                                        ),
                                    ),
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
                                        "items": pydantic_snapshot(
                                            v2=snapshot(
                                                {
                                                    "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item-Input"
                                                }
                                            ),
                                            v1=snapshot(
                                                {
                                                    "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
                                                }
                                            ),
                                        ),
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
                                        "items": pydantic_snapshot(
                                            v2=snapshot(
                                                {
                                                    "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item-Input"
                                                }
                                            ),
                                            v1=snapshot(
                                                {
                                                    "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
                                                }
                                            ),
                                        ),
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
                "/v2-to-v1/same-name": {
                    "post": {
                        "summary": "Handle V2 Same Name To V1",
                        "operationId": "handle_v2_same_name_to_v1_v2_to_v1_same_name_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_handle_v2_same_name_to_v1_v2_to_v1_same_name_post"
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
                "/v2-to-v1/list-of-items-to-list-of-items": {
                    "post": {
                        "summary": "Handle V2 Items In List To V1 Item In List",
                        "operationId": "handle_v2_items_in_list_to_v1_item_in_list_v2_to_v1_list_of_items_to_list_of_items_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_handle_v2_items_in_list_to_v1_item_in_list_v2_to_v1_list_of_items_to_list_of_items_post"
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
                                                "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv1__ItemInList"
                                            },
                                            "type": "array",
                                            "title": "Response Handle V2 Items In List To V1 Item In List V2 To V1 List Of Items To List Of Items Post",
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
                "schemas": pydantic_snapshot(
                    v1=snapshot(
                        {
                            "Body_handle_v2_items_in_list_to_v1_item_in_list_v2_to_v1_list_of_items_to_list_of_items_post": {
                                "properties": {
                                    "data1": {
                                        "items": {
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__ItemInList"
                                        },
                                        "type": "array",
                                        "title": "Data1",
                                    },
                                    "data2": {
                                        "items": {
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2b__ItemInList"
                                        },
                                        "type": "array",
                                        "title": "Data2",
                                    },
                                },
                                "type": "object",
                                "required": ["data1", "data2"],
                                "title": "Body_handle_v2_items_in_list_to_v1_item_in_list_v2_to_v1_list_of_items_to_list_of_items_post",
                            },
                            "Body_handle_v2_same_name_to_v1_v2_to_v1_same_name_post": {
                                "properties": {
                                    "item1": {
                                        "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item"
                                    },
                                    "item2": {
                                        "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2b__Item"
                                    },
                                },
                                "type": "object",
                                "required": ["item1", "item2"],
                                "title": "Body_handle_v2_same_name_to_v1_v2_to_v1_same_name_post",
                            },
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
                                            "anyOf": [
                                                {"type": "string"},
                                                {"type": "integer"},
                                            ]
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
                            "tests__test_pydantic_v1_v2_multifile__modelsv1__Item": {
                                "properties": {
                                    "title": {"type": "string", "title": "Title"},
                                    "size": {"type": "integer", "title": "Size"},
                                    "description": {
                                        "type": "string",
                                        "title": "Description",
                                    },
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
                            "tests__test_pydantic_v1_v2_multifile__modelsv1__ItemInList": {
                                "properties": {
                                    "name1": {"type": "string", "title": "Name1"}
                                },
                                "type": "object",
                                "required": ["name1"],
                                "title": "ItemInList",
                            },
                            "tests__test_pydantic_v1_v2_multifile__modelsv1__SubItem": {
                                "properties": {
                                    "name": {"type": "string", "title": "Name"}
                                },
                                "type": "object",
                                "required": ["name"],
                                "title": "SubItem",
                            },
                            "tests__test_pydantic_v1_v2_multifile__modelsv2__Item": {
                                "properties": {
                                    "new_title": {
                                        "type": "string",
                                        "title": "New Title",
                                    },
                                    "new_size": {
                                        "type": "integer",
                                        "title": "New Size",
                                    },
                                    "new_description": {
                                        "type": "string",
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
                            "tests__test_pydantic_v1_v2_multifile__modelsv2__ItemInList": {
                                "properties": {
                                    "name2": {"type": "string", "title": "Name2"}
                                },
                                "type": "object",
                                "required": ["name2"],
                                "title": "ItemInList",
                            },
                            "tests__test_pydantic_v1_v2_multifile__modelsv2__SubItem": {
                                "properties": {
                                    "new_sub_name": {
                                        "type": "string",
                                        "title": "New Sub Name",
                                    }
                                },
                                "type": "object",
                                "required": ["new_sub_name"],
                                "title": "SubItem",
                            },
                            "tests__test_pydantic_v1_v2_multifile__modelsv2b__Item": {
                                "properties": {
                                    "dup_title": {
                                        "type": "string",
                                        "title": "Dup Title",
                                    },
                                    "dup_size": {
                                        "type": "integer",
                                        "title": "Dup Size",
                                    },
                                    "dup_description": {
                                        "type": "string",
                                        "title": "Dup Description",
                                    },
                                    "dup_sub": {
                                        "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2b__SubItem"
                                    },
                                    "dup_multi": {
                                        "items": {
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2b__SubItem"
                                        },
                                        "type": "array",
                                        "title": "Dup Multi",
                                        "default": [],
                                    },
                                },
                                "type": "object",
                                "required": ["dup_title", "dup_size", "dup_sub"],
                                "title": "Item",
                            },
                            "tests__test_pydantic_v1_v2_multifile__modelsv2b__ItemInList": {
                                "properties": {
                                    "dup_name2": {
                                        "type": "string",
                                        "title": "Dup Name2",
                                    }
                                },
                                "type": "object",
                                "required": ["dup_name2"],
                                "title": "ItemInList",
                            },
                            "tests__test_pydantic_v1_v2_multifile__modelsv2b__SubItem": {
                                "properties": {
                                    "dup_sub_name": {
                                        "type": "string",
                                        "title": "Dup Sub Name",
                                    }
                                },
                                "type": "object",
                                "required": ["dup_sub_name"],
                                "title": "SubItem",
                            },
                        }
                    ),
                    v2=snapshot(
                        {
                            "Body_handle_v2_items_in_list_to_v1_item_in_list_v2_to_v1_list_of_items_to_list_of_items_post": {
                                "properties": {
                                    "data1": {
                                        "items": {
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__ItemInList"
                                        },
                                        "type": "array",
                                        "title": "Data1",
                                    },
                                    "data2": {
                                        "items": {
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2b__ItemInList"
                                        },
                                        "type": "array",
                                        "title": "Data2",
                                    },
                                },
                                "type": "object",
                                "required": ["data1", "data2"],
                                "title": "Body_handle_v2_items_in_list_to_v1_item_in_list_v2_to_v1_list_of_items_to_list_of_items_post",
                            },
                            "Body_handle_v2_same_name_to_v1_v2_to_v1_same_name_post": {
                                "properties": {
                                    "item1": {
                                        "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2__Item-Input"
                                    },
                                    "item2": {
                                        "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2b__Item"
                                    },
                                },
                                "type": "object",
                                "required": ["item1", "item2"],
                                "title": "Body_handle_v2_same_name_to_v1_v2_to_v1_same_name_post",
                            },
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
                            "SubItem-Output": {
                                "properties": {
                                    "new_sub_name": {
                                        "type": "string",
                                        "title": "New Sub Name",
                                    }
                                },
                                "type": "object",
                                "required": ["new_sub_name"],
                                "title": "SubItem",
                            },
                            "ValidationError": {
                                "properties": {
                                    "loc": {
                                        "items": {
                                            "anyOf": [
                                                {"type": "string"},
                                                {"type": "integer"},
                                            ]
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
                            "tests__test_pydantic_v1_v2_multifile__modelsv1__Item": {
                                "properties": {
                                    "title": {"type": "string", "title": "Title"},
                                    "size": {"type": "integer", "title": "Size"},
                                    "description": {
                                        "type": "string",
                                        "title": "Description",
                                    },
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
                            "tests__test_pydantic_v1_v2_multifile__modelsv1__ItemInList": {
                                "properties": {
                                    "name1": {"type": "string", "title": "Name1"}
                                },
                                "type": "object",
                                "required": ["name1"],
                                "title": "ItemInList",
                            },
                            "tests__test_pydantic_v1_v2_multifile__modelsv1__SubItem": {
                                "properties": {
                                    "name": {"type": "string", "title": "Name"}
                                },
                                "type": "object",
                                "required": ["name"],
                                "title": "SubItem",
                            },
                            "tests__test_pydantic_v1_v2_multifile__modelsv2__Item": {
                                "properties": {
                                    "new_title": {
                                        "type": "string",
                                        "title": "New Title",
                                    },
                                    "new_size": {
                                        "type": "integer",
                                        "title": "New Size",
                                    },
                                    "new_description": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "New Description",
                                    },
                                    "new_sub": {
                                        "$ref": "#/components/schemas/SubItem-Output"
                                    },
                                    "new_multi": {
                                        "items": {
                                            "$ref": "#/components/schemas/SubItem-Output"
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
                            "tests__test_pydantic_v1_v2_multifile__modelsv2__Item-Input": {
                                "properties": {
                                    "new_title": {
                                        "type": "string",
                                        "title": "New Title",
                                    },
                                    "new_size": {
                                        "type": "integer",
                                        "title": "New Size",
                                    },
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
                            "tests__test_pydantic_v1_v2_multifile__modelsv2__ItemInList": {
                                "properties": {
                                    "name2": {"type": "string", "title": "Name2"}
                                },
                                "type": "object",
                                "required": ["name2"],
                                "title": "ItemInList",
                            },
                            "tests__test_pydantic_v1_v2_multifile__modelsv2__SubItem": {
                                "properties": {
                                    "new_sub_name": {
                                        "type": "string",
                                        "title": "New Sub Name",
                                    }
                                },
                                "type": "object",
                                "required": ["new_sub_name"],
                                "title": "SubItem",
                            },
                            "tests__test_pydantic_v1_v2_multifile__modelsv2b__Item": {
                                "properties": {
                                    "dup_title": {
                                        "type": "string",
                                        "title": "Dup Title",
                                    },
                                    "dup_size": {
                                        "type": "integer",
                                        "title": "Dup Size",
                                    },
                                    "dup_description": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "Dup Description",
                                    },
                                    "dup_sub": {
                                        "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2b__SubItem"
                                    },
                                    "dup_multi": {
                                        "items": {
                                            "$ref": "#/components/schemas/tests__test_pydantic_v1_v2_multifile__modelsv2b__SubItem"
                                        },
                                        "type": "array",
                                        "title": "Dup Multi",
                                        "default": [],
                                    },
                                },
                                "type": "object",
                                "required": ["dup_title", "dup_size", "dup_sub"],
                                "title": "Item",
                            },
                            "tests__test_pydantic_v1_v2_multifile__modelsv2b__ItemInList": {
                                "properties": {
                                    "dup_name2": {
                                        "type": "string",
                                        "title": "Dup Name2",
                                    }
                                },
                                "type": "object",
                                "required": ["dup_name2"],
                                "title": "ItemInList",
                            },
                            "tests__test_pydantic_v1_v2_multifile__modelsv2b__SubItem": {
                                "properties": {
                                    "dup_sub_name": {
                                        "type": "string",
                                        "title": "Dup Sub Name",
                                    }
                                },
                                "type": "object",
                                "required": ["dup_sub_name"],
                                "title": "SubItem",
                            },
                        }
                    ),
                ),
            },
        }
    )
