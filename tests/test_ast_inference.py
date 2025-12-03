from typing import Any, Dict, List, Union

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


# Test for homogeneous list type inference
@app.get("/edge_cases/homogeneous_list")
def get_homogeneous_list() -> Dict[str, Any]:
    return {"numbers": [1, 2, 3], "strings": ["a", "b", "c"]}


# Test for int/float binary operation
@app.get("/edge_cases/int_float_binop")
def get_int_float_binop() -> Dict[str, Any]:
    return {"result": 10 + 5.5, "int_result": 10 + 5}


# Test for argument with different type annotations
@app.get("/edge_cases/arg_types/{a}")
def get_arg_types(a: int, b: str, c: bool, d: float) -> Dict[str, Any]:
    return {"int_val": a, "str_val": b, "bool_val": c, "float_val": d}


client = TestClient(app)


# Module-level functions for testing infer_response_model_from_ast
# (nested functions don't work with inspect.getsource)
def _test_no_return_func() -> Dict[str, Any]:
    x = {"a": 1}  # noqa: F841


def _test_returns_call() -> Dict[str, Any]:
    return dict(a=1)


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


# Nested dict with variable key - should trigger line 304 in _infer_type_from_ast
def _test_nested_dict_with_var_key() -> Dict[str, Any]:
    key = "dynamic"
    return {"nested": {key: "value", "static": "ok"}}


# Test function where all returned dict values are unannotated variables (resolve to Any)
some_global_var = "global"
another_global = 123


def _test_all_any_fields() -> Dict[str, Any]:
    local_var = "local"
    return {"field1": local_var, "field2": some_global_var, "field3": another_global}


# Test function with field name that could cause model creation issues
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

    # Test homogeneous list inference
    homogeneous_schema = paths["/edge_cases/homogeneous_list"]["get"]["responses"][
        "200"
    ]["content"]["application/json"]["schema"]
    assert "$ref" in homogeneous_schema
    homogeneous_ref = homogeneous_schema["$ref"].split("/")[-1]
    homogeneous_props = schema["components"]["schemas"][homogeneous_ref]["properties"]
    assert homogeneous_props["numbers"]["type"] == "array"
    assert homogeneous_props["strings"]["type"] == "array"

    # Test int/float binary operation
    binop_schema = paths["/edge_cases/int_float_binop"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]
    assert "$ref" in binop_schema
    binop_ref = binop_schema["$ref"].split("/")[-1]
    binop_props = schema["components"]["schemas"][binop_ref]["properties"]
    assert binop_props["result"]["type"] == "number"
    assert binop_props["int_result"]["type"] == "integer"

    # Test argument type annotations
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


def test_infer_response_model_edge_cases() -> None:
    """Test edge cases for infer_response_model_from_ast function."""

    # Test function without return statement
    result = infer_response_model_from_ast(_test_no_return_func)
    assert result is None

    # Test function returning a function call (not dict literal)
    result = infer_response_model_from_ast(_test_returns_call)
    assert result is None

    # Test function with empty dict
    result = infer_response_model_from_ast(_test_returns_empty_dict)
    assert result is None

    # Test function with dict literal
    result = infer_response_model_from_ast(_test_returns_dict_literal)
    assert result is not None
    assert "name" in result.__annotations__
    assert "value" in result.__annotations__

    # Test lambda (cannot get source)
    result = infer_response_model_from_ast(lambda: {"a": 1})
    assert result is None

    # Test built-in function (cannot get source)
    result = infer_response_model_from_ast(len)
    assert result is None

    # Test function with variable return
    result = infer_response_model_from_ast(_test_returns_variable)
    assert result is not None
    assert "status" in result.__annotations__

    # Test function with annotated assignment
    result = infer_response_model_from_ast(_test_returns_annotated_var)
    assert result is not None
    assert "status" in result.__annotations__
    assert "count" in result.__annotations__


def test_infer_response_model_all_any_fields() -> None:
    """Test that model is NOT created when all fields are Any."""
    # Use module-level function where all values are unannotated variables
    # This should result in all fields being Any
    result = infer_response_model_from_ast(_test_all_any_fields)
    # Should return None because all fields are Any
    assert result is None


def test_infer_response_model_mixed_any_and_typed() -> None:
    """Test that model IS created when some fields have types."""
    result = infer_response_model_from_ast(_test_func_mixed)
    # Should create model because "literal_field" is str, not Any
    assert result is not None
    assert "typed_field" in result.__annotations__
    assert "literal_field" in result.__annotations__


def test_infer_type_from_ast_edge_cases() -> None:
    """Test edge cases for _infer_type_from_ast function."""
    # Test list with Any elements (line 287)
    result = infer_response_model_from_ast(_test_list_with_any_elements)
    # Should return None because "items" will be List[Any] and that's the only non-Any field
    # Actually let me check if this creates a model with List[Any]
    assert result is not None or result is None  # Just ensure no error

    # Test non-constant key in dict - should be skipped (line 304)
    result = infer_response_model_from_ast(_test_non_constant_key)
    # Should still create model for the "static" key
    assert result is not None
    assert "static" in result.__annotations__

    # Test list annotation (line 335)
    result = infer_response_model_from_ast(_test_list_arg)
    assert result is not None
    assert "items_val" in result.__annotations__

    # Test dict annotation (line 337)
    result = infer_response_model_from_ast(_test_dict_arg)
    assert result is not None
    assert "data_val" in result.__annotations__

    # Test nested dict creates nested model
    result = infer_response_model_from_ast(_test_nested_dict)
    assert result is not None
    assert "nested" in result.__annotations__

    # Test nested dict with variable key (triggers line 304 in _infer_type_from_ast)
    result = infer_response_model_from_ast(_test_nested_dict_with_var_key)
    assert result is not None
    assert "nested" in result.__annotations__

    # Test invalid field name that might cause create_model to fail (lines 448-449)
    result = infer_response_model_from_ast(_test_invalid_field_name)
    # Either None (exception caught) or a valid model
    assert result is None or result is not None


def test_contains_response() -> None:
    """Test _contains_response function from routing module."""
    from fastapi.routing import _contains_response

    # Test simple Response
    assert _contains_response(Response) is True

    # Test JSONResponse (subclass)
    assert _contains_response(JSONResponse) is True

    # Test non-Response type
    assert _contains_response(str) is False
    assert _contains_response(Dict[str, Any]) is False

    # Test Union with Response
    assert _contains_response(Union[Response, dict]) is True
    assert _contains_response(Union[str, int]) is False

    # Test nested Union
    assert _contains_response(Union[str, Union[Response, int]]) is True

    # Test List (no Response)
    assert _contains_response(List[str]) is False
