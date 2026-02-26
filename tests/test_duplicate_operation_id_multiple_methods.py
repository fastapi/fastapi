import warnings

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_no_duplicate_operation_id_with_multiple_methods():
    """Ensure routes with multiple methods get unique operation IDs."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        app = FastAPI()

        def handler():
            return {"status": "ok"}  # pragma: nocover

        app.add_api_route("/items", handler, methods=["POST", "DELETE"])

        client = TestClient(app)
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()

        post_op = schema["paths"]["/items"]["post"]
        delete_op = schema["paths"]["/items"]["delete"]

        assert post_op["operationId"] != delete_op["operationId"]
        assert "post" in post_op["operationId"]
        assert "delete" in delete_op["operationId"]

        dup_warnings = [x for x in w if "Duplicate" in str(x.message)]
        assert len(dup_warnings) == 0


def test_single_method_route_operation_id_unchanged():
    """Ensure single-method routes still generate the same operation IDs."""
    app = FastAPI()

    @app.get("/items")
    def get_items():
        return []  # pragma: nocover

    client = TestClient(app)
    response = client.get("/openapi.json")
    schema = response.json()

    get_op = schema["paths"]["/items"]["get"]
    assert get_op["operationId"] == "get_items_items_get"


def test_three_methods_unique_operation_ids():
    """Ensure routes with three methods all get unique operation IDs."""
    app = FastAPI()

    def handler():
        return {"status": "ok"}  # pragma: nocover

    app.add_api_route("/items", handler, methods=["GET", "POST", "DELETE"])

    client = TestClient(app)
    response = client.get("/openapi.json")
    schema = response.json()

    get_op = schema["paths"]["/items"]["get"]
    post_op = schema["paths"]["/items"]["post"]
    delete_op = schema["paths"]["/items"]["delete"]

    assert "get" in get_op["operationId"]
    assert "post" in post_op["operationId"]
    assert "delete" in delete_op["operationId"]
    assert (
        len({get_op["operationId"], post_op["operationId"], delete_op["operationId"]})
        == 3
    )
