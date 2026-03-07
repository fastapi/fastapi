"""
Test that routes with multiple methods get unique operation IDs.
This is a regression test for issue #13175.
"""

import warnings

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_multiple_methods_generate_unique_operation_ids():
    """Test that add_api_route with multiple methods generates unique operation IDs."""
    app = FastAPI()

    def clear():
        return {"cleared": True}

    app.add_api_route("/clear", clear, methods=["POST", "DELETE"])

    # Capture warnings to check for duplicate operation_id warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        client = TestClient(app)
        response = client.get("/openapi.json")

        # There should be no duplicate operation_id warnings
        dup_warnings = [
            warning for warning in w if "Duplicate Operation ID" in str(warning.message)
        ]
        assert len(dup_warnings) == 0, (
            f"Expected no duplicate warnings, got: {dup_warnings}"
        )

    openapi_schema = response.json()

    # Get the operation IDs for POST and DELETE
    post_operation_id = openapi_schema["paths"]["/clear"]["post"]["operationId"]
    delete_operation_id = openapi_schema["paths"]["/clear"]["delete"]["operationId"]

    # They should be different
    assert post_operation_id != delete_operation_id, (
        f"POST and DELETE should have different operation IDs. "
        f"Got POST: {post_operation_id}, DELETE: {delete_operation_id}"
    )

    # Verify the operation IDs contain the correct method suffix
    assert post_operation_id.endswith("_post"), (
        f"POST operation_id should end with '_post', got: {post_operation_id}"
    )
    assert delete_operation_id.endswith("_delete"), (
        f"DELETE operation_id should end with '_delete', got: {delete_operation_id}"
    )


if __name__ == "__main__":
    test_multiple_methods_generate_unique_operation_ids()
    print("Test passed!")
