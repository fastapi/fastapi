from typing import Any, Dict

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/users/{user_id}")
async def get_user(user_id: int) -> Dict[str, Any]:
    user: Dict[str, Any] = {
        "id": user_id,
        "username": "example",
        "email": "user@example.com",
        "age": 25,
        "is_active": True,
    }
    return user


@app.get("/orders/{order_id}")
async def get_order_details(order_id: str) -> Dict[str, Any]:
    order_data: Dict[str, Any] = {
        "order_id": order_id,
        "status": "processing",
        "total_amount": 150.50,
        "tags": ["urgent", "new_customer"],
        "customer_info": {
            "name": "John Doe",
            "vip_status": False,
            "preferences": {"notifications": True, "theme": "dark"},
        },
        "items": [
            {
                "item_id": 1,
                "name": "Laptop Stand",
                "price": 45.00,
                "in_stock": True,
            },
        ],
        "metadata": None,
    }
    return order_data


@app.get("/edge_cases/mixed_types")
async def get_mixed_types() -> Dict[str, Any]:
    return {"mixed_list": [1, "two", 3.0], "description": "List starting with int"}


@app.get("/edge_cases/expressions")
async def get_expressions() -> Dict[str, Any]:
    return {"calc_int": 10 + 5, "calc_str": "foo" + "bar", "calc_bool": 5 > 3}


@app.get("/edge_cases/empty_structures")
async def get_empty_structures() -> Dict[str, Any]:
    return {"empty_list": [], "empty_dict": {}}


@app.get("/edge_cases/local_variable")
async def get_local_variable() -> Dict[str, Any]:
    response_data = {"status": "ok", "nested": {"check": True}}
    return response_data


@app.get("/edge_cases/explicit_response")
def get_explicit_response() -> JSONResponse:
    return JSONResponse({"should_not_be_inferred": True})


@app.get("/edge_cases/nested_function")
async def get_nested_function() -> Dict[str, Any]:
    def inner_function():
        return {"inner": "value"}

    return {"outer": "value"}


@app.get("/edge_cases/invalid_keys")
def get_invalid_keys() -> Dict[Any, Any]:
    return {1: "value", "valid": "key"}


class FakeDB:
    def get_user(self) -> Dict[str, Any]:
        return {"id": 1, "username": "db_user"}


fake_db = FakeDB()


@app.get("/db/direct_return")
def get_db_direct() -> Dict[str, Any]:
    return fake_db.get_user()


@app.get("/db/dict_construction")
def get_db_constructed() -> Dict[str, Any]:
    data = fake_db.get_user()
    return {"db_id": data["id"], "source": "database"}


client = TestClient(app)


def test_openapi_schema_ast_inference():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    paths = schema["paths"]

    user_schema = paths["/users/{user_id}"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]
    assert "$ref" in user_schema
    ref_name = user_schema["$ref"].split("/")[-1]
    user_props = schema["components"]["schemas"][ref_name]["properties"]

    assert user_props["id"]["type"] == "integer"
    assert user_props["username"]["type"] == "string"
    assert user_props["is_active"]["type"] == "boolean"

    order_schema = paths["/orders/{order_id}"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]
    assert "$ref" in order_schema
    order_ref = order_schema["$ref"].split("/")[-1]
    order_props = schema["components"]["schemas"][order_ref]["properties"]

    items_prop = order_props["items"]
    assert items_prop["type"] == "array"
    assert "$ref" in items_prop["items"]

    customer_prop = order_props["customer_info"]
    assert "$ref" in customer_prop

    mixed_schema = paths["/edge_cases/mixed_types"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]
    mixed_ref = mixed_schema["$ref"].split("/")[-1]
    mixed_props = schema["components"]["schemas"][mixed_ref]["properties"]
    assert mixed_props["mixed_list"]["type"] == "array"

    expr_schema = paths["/edge_cases/expressions"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]
    expr_ref = expr_schema["$ref"].split("/")[-1]
    expr_props = schema["components"]["schemas"][expr_ref]["properties"]

    assert expr_props["calc_int"]["type"] == "integer"
    assert expr_props["calc_bool"]["type"] == "boolean"

    explicit_schema = paths["/edge_cases/explicit_response"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]
    assert "$ref" not in explicit_schema

    nested_schema = paths["/edge_cases/nested_function"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]
    assert "$ref" in nested_schema
    nested_ref = nested_schema["$ref"].split("/")[-1]
    nested_props = schema["components"]["schemas"][nested_ref]["properties"]
    assert "outer" in nested_props
    assert "inner" not in nested_props

    invalid_keys_schema = paths["/edge_cases/invalid_keys"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]
    assert "$ref" not in invalid_keys_schema

    db_direct_schema = paths["/db/direct_return"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]
    assert "$ref" not in db_direct_schema

    db_constructed_schema = paths["/db/dict_construction"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]
    assert "$ref" in db_constructed_schema
    db_constructed_ref = db_constructed_schema["$ref"].split("/")[-1]
    db_constructed_props = schema["components"]["schemas"][db_constructed_ref][
        "properties"
    ]

    assert db_constructed_props["source"]["type"] == "string"
    assert (
        "type" not in db_constructed_props["db_id"]
        or db_constructed_props["db_id"] == {}
    )
