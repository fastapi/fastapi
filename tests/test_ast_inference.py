from typing import Any, Dict, List, Union

import pytest
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from fastapi.utils import infer_response_model_from_ast

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


@app.get("/edge_cases/homogeneous_list")
def get_homogeneous_list() -> Dict[str, Any]:
    return {"numbers": [1, 2, 3], "strings": ["a", "b", "c"]}


@app.get("/edge_cases/int_float_binop")
def get_int_float_binop() -> Dict[str, Any]:
    return {"result": 10 + 5.5, "int_result": 10 + 5}


@app.get("/edge_cases/arg_types/{a}")
def get_arg_types(a: int, b: str, c: bool, d: float) -> Dict[str, Any]:
    return {"int_val": a, "str_val": b, "bool_val": c, "float_val": d}


client = TestClient(app)


def _test_no_return_func() -> Dict[str, Any]:
    x = {"a": 1}  # noqa: F841


def _test_returns_call() -> Dict[str, Any]:
    return {}.copy()


def _test_returns_empty_dict() -> Dict[str, Any]:
    return {}


def _test_returns_dict_literal() -> Dict[str, Any]:
    return {"name": "test", "value": 123}


def _test_returns_variable() -> Dict[str, Any]:
    data = {"status": "ok"}
    return data


def _test_returns_annotated_var() -> Dict[str, Any]:
    data: Dict[str, Any] = {"status": "ok", "count": 42}
    return data


def _test_func_mixed(item: int) -> Dict[str, Any]:
    return {"typed_field": item, "literal_field": "hello"}


def _test_list_with_any_elements(x: Any) -> Dict[str, Any]:
    return {"items": [x]}


def _test_non_constant_key() -> Dict[str, Any]:
    key = "dynamic"
    return {key: "value", "static": "ok"}


def _test_list_arg(items: list) -> Dict[str, Any]:
    return {"items_val": items}


def _test_dict_arg(data: dict) -> Dict[str, Any]:
    return {"data_val": data}


def _test_nested_dict() -> Dict[str, Any]:
    return {"nested": {"inner": "value"}}


def _test_nested_dict_with_var_key() -> Dict[str, Any]:
    key = "dynamic"
    return {"nested": {key: "value", "static": "ok"}}


some_global_var = "global"
another_global = 123


def _test_all_any_fields() -> Dict[str, Any]:
    local_var = "local"
    return {"field1": local_var, "field2": some_global_var, "field3": another_global}


def _test_invalid_field_name() -> Dict[str, Any]:
    return {"__class__": "invalid", "normal": "ok"}


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

    homogeneous_schema = paths["/edge_cases/homogeneous_list"]["get"]["responses"][
        "200"
    ]["content"]["application/json"]["schema"]
    assert "$ref" in homogeneous_schema
    homogeneous_ref = homogeneous_schema["$ref"].split("/")[-1]
    homogeneous_props = schema["components"]["schemas"][homogeneous_ref]["properties"]
    assert homogeneous_props["numbers"]["type"] == "array"
    assert homogeneous_props["strings"]["type"] == "array"

    binop_schema = paths["/edge_cases/int_float_binop"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]
    assert "$ref" in binop_schema
    binop_ref = binop_schema["$ref"].split("/")[-1]
    binop_props = schema["components"]["schemas"][binop_ref]["properties"]
    assert binop_props["result"]["type"] == "number"
    assert binop_props["int_result"]["type"] == "integer"

    arg_types_schema = paths["/edge_cases/arg_types/{a}"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]
    assert "$ref" in arg_types_schema
    arg_types_ref = arg_types_schema["$ref"].split("/")[-1]
    arg_types_props = schema["components"]["schemas"][arg_types_ref]["properties"]
    assert arg_types_props["int_val"]["type"] == "integer"
    assert arg_types_props["str_val"]["type"] == "string"
    assert arg_types_props["bool_val"]["type"] == "boolean"
    assert arg_types_props["float_val"]["type"] == "number"

@pytest.mark.parametrize(
    "func",
    [
        _test_no_return_func,
        _test_returns_call,
        _test_returns_empty_dict,
        _test_all_any_fields,
    ],
)
def test_infer_response_model_returns_none(func):
    """Test cases where AST inference should return None."""
    assert infer_response_model_from_ast(func) is None


def test_infer_response_model_returns_none_for_lambdas_and_builtins():
    """Test cases where AST inference cannot get source code."""
    assert infer_response_model_from_ast(lambda: {"a": 1}) is None
    assert infer_response_model_from_ast(len) is None


@pytest.mark.parametrize(
    "func,expected_fields",
    [
        (_test_returns_dict_literal, ["name", "value"]),
        (_test_returns_variable, ["status"]),
        (_test_returns_annotated_var, ["status", "count"]),
        (_test_func_mixed, ["typed_field", "literal_field"]),
        (_test_list_with_any_elements, ["items"]),
        (_test_non_constant_key, ["static"]),
        (_test_list_arg, ["items_val"]),
        (_test_dict_arg, ["data_val"]),
        (_test_nested_dict, ["nested"]),
        (_test_nested_dict_with_var_key, ["nested"]),
    ],
)
def test_infer_response_model_success(func, expected_fields):
    """Test cases where AST inference should succeed and return a model with specific fields."""
    result = infer_response_model_from_ast(func)
    assert result is not None
    for field in expected_fields:
        assert field in result.__annotations__


def test_infer_response_model_invalid_field_name():
    """Test that invalid field names are handled gracefully (either skipped or model creation fails safely)."""
    # This specifically tests protections against things like {"__class__": ...}
    # It might return None (if create_model fails) or a model (if pydantic handles it)
    # We just want to ensure it doesn't raise an unhandled exception
    try:
        infer_response_model_from_ast(_test_invalid_field_name)
    except Exception as e:
        pytest.fail(f"infer_response_model_from_ast raised exception: {e}")


def test_contains_response() -> None:
    from fastapi.routing import _contains_response

    assert _contains_response(Response) is True
    assert _contains_response(JSONResponse) is True
    assert _contains_response(str) is False
    assert _contains_response(Dict[str, Any]) is False
    assert _contains_response(Union[Response, dict]) is True
    assert _contains_response(Union[str, int]) is False
    assert _contains_response(Union[str, Union[Response, int]]) is True
    assert _contains_response(List[str]) is False
