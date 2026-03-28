"""Test for fix of issue #13175: duplicate operation IDs with multi-method routes"""
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_no_duplicate_operation_ids_with_multiple_methods():
    """Test that routes with multiple methods generate unique operation IDs for each method."""
    app = FastAPI()

    @app.api_route("/items/", methods=["GET", "POST", "DELETE"])
    def handle_items():
        return {"message": "handled"}

    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    data = response.json()
    
    # Check that all three methods exist in the OpenAPI schema
    paths = data.get("paths", {})
    items_path = paths.get("/items/", {})
    
    assert "get" in items_path
    assert "post" in items_path
    assert "delete" in items_path
    
    # Verify each method has a unique operation ID
    get_op_id = items_path["get"].get("operationId")
    post_op_id = items_path["post"].get("operationId")
    delete_op_id = items_path["delete"].get("operationId")
    
    # All should exist
    assert get_op_id is not None
    assert post_op_id is not None
    assert delete_op_id is not None
    
    # All should be different
    assert get_op_id != post_op_id
    assert get_op_id != delete_op_id
    assert post_op_id != delete_op_id
    
    # Verify they follow the pattern: <name>_<path>_<method>
    assert "handle_items_items_" in get_op_id
    assert "handle_items_items_" in post_op_id
    assert "handle_items_items_" in delete_op_id
    
    assert "_get" in get_op_id
    assert "_post" in post_op_id
    assert "_delete" in delete_op_id


if __name__ == "__main__":
    test_no_duplicate_operation_ids_with_multiple_methods()
    print("✓ Test passed!")

