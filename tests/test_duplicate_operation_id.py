"""
Test that routes with multiple methods get unique operation IDs.
Related to issue #13175
"""

import warnings

from fastapi import FastAPI


def test_multiple_methods_unique_operation_ids():
    """Test that a route with multiple methods generates unique operation IDs"""
    app = FastAPI()

    @app.api_route("/clear", methods=["POST", "DELETE"])
    def clear():
        return {"message": "cleared"}

    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # Get OpenAPI schema which triggers operation ID generation
        openapi_schema = app.openapi()

        # Check that no duplicate operation ID warning was raised
        duplicate_warnings = [
            warning for warning in w if "Duplicate Operation ID" in str(warning.message)
        ]
        assert len(duplicate_warnings) == 0, (
            f"Found {len(duplicate_warnings)} duplicate operation ID warnings: "
            f"{[str(w.message) for w in duplicate_warnings]}"
        )

    # Verify both methods are in the schema with different operation IDs
    assert "/clear" in openapi_schema["paths"]
    clear_path = openapi_schema["paths"]["/clear"]

    # Both POST and DELETE should be present
    assert "post" in clear_path
    assert "delete" in clear_path

    # Operation IDs should be different
    post_op_id = clear_path["post"]["operationId"]
    delete_op_id = clear_path["delete"]["operationId"]

    assert post_op_id != delete_op_id, (
        f"Operation IDs should be different: POST={post_op_id}, DELETE={delete_op_id}"
    )


def test_multiple_routes_with_multiple_methods():
    """Test multiple routes each with multiple methods"""
    app = FastAPI()

    @app.api_route("/clear", methods=["POST", "DELETE"])
    def clear():
        return {"message": "cleared"}

    @app.api_route("/reset", methods=["POST", "PUT"])
    def reset():
        return {"message": "reset"}

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        openapi_schema = app.openapi()

        duplicate_warnings = [
            warning for warning in w if "Duplicate Operation ID" in str(warning.message)
        ]
        assert len(duplicate_warnings) == 0

    # Verify all operation IDs are unique
    operation_ids = set()
    for path_data in openapi_schema["paths"].values():
        for method_data in path_data.values():
            if isinstance(method_data, dict) and "operationId" in method_data:
                op_id = method_data["operationId"]
                assert op_id not in operation_ids, f"Duplicate operation ID: {op_id}"
                operation_ids.add(op_id)


def test_single_method_route_unchanged():
    """Test that routes with single methods still work as before"""
    app = FastAPI()

    @app.get("/items")
    def get_items():
        return {"items": []}

    openapi_schema = app.openapi()

    # Should have the expected structure
    assert "/items" in openapi_schema["paths"]
    assert "get" in openapi_schema["paths"]["/items"]
    assert "operationId" in openapi_schema["paths"]["/items"]["get"]


def test_add_api_route_with_multiple_methods():
    """Test using add_api_route directly with multiple methods"""
    app = FastAPI()

    def clear_handler():
        return {"message": "cleared"}

    app.add_api_route("/clear", clear_handler, methods=["POST", "DELETE"])

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        openapi_schema = app.openapi()

        duplicate_warnings = [
            warning for warning in w if "Duplicate Operation ID" in str(warning.message)
        ]
        assert len(duplicate_warnings) == 0

    clear_path = openapi_schema["paths"]["/clear"]
    assert clear_path["post"]["operationId"] != clear_path["delete"]["operationId"]


def test_explicit_operation_id_with_multiple_methods():
    """Test that explicit operation_id is respected and not modified"""
    app = FastAPI()

    @app.api_route("/clear", methods=["POST", "DELETE"], operation_id="custom_clear")
    def clear():
        return {"message": "cleared"}

    # When explicit operation_id is provided, it's used as-is which may cause
    # duplicate operation ID warnings - this is expected behavior
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        openapi_schema = app.openapi()

        # If user provides explicit operation_id with multiple methods,
        # they'll get a duplicate warning - this is intentional
        duplicate_warnings = [
            warning for warning in w if "Duplicate Operation ID" in str(warning.message)
        ]
        # We expect a duplicate warning because the user explicitly set the same
        # operation_id for multiple methods
        assert len(duplicate_warnings) > 0

    clear_path = openapi_schema["paths"]["/clear"]
    # Both methods use the same explicit operation_id
    assert clear_path["post"]["operationId"] == "custom_clear"
    assert clear_path["delete"]["operationId"] == "custom_clear"
