import warnings

import pytest
from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient


def _no_duplicate_warnings(caught):
    return [w for w in caught if "Duplicate Operation" in str(w.message)]


def test_add_api_route_with_multiple_methods_produces_unique_operation_ids():
    app = FastAPI()

    def clear():
        return {}  # pragma: nocover

    app.add_api_route("/clear", clear, methods=["POST", "DELETE"])

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        schema = app.openapi()

    assert _no_duplicate_warnings(caught) == []

    post_id = schema["paths"]["/clear"]["post"]["operationId"]
    delete_id = schema["paths"]["/clear"]["delete"]["operationId"]
    assert post_id != delete_id
    assert post_id.endswith("_post")
    assert delete_id.endswith("_delete")


def test_api_route_decorator_with_multiple_methods_produces_unique_operation_ids():
    app = FastAPI()

    @app.api_route("/things", methods=["GET", "PUT", "PATCH"])
    def things():
        return {}  # pragma: nocover

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        schema = app.openapi()

    assert _no_duplicate_warnings(caught) == []

    ops = schema["paths"]["/things"]
    ids = {method: ops[method]["operationId"] for method in ("get", "put", "patch")}
    assert len(set(ids.values())) == 3
    for method, op_id in ids.items():
        assert op_id.endswith(f"_{method}")


def test_multiple_methods_with_explicit_operation_id_is_respected():
    app = FastAPI()

    def handler():
        return {}  # pragma: nocover

    app.add_api_route(
        "/explicit",
        handler,
        methods=["POST", "DELETE"],
        operation_id="my_custom_id",
    )

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        schema = app.openapi()

    duplicates = _no_duplicate_warnings(caught)
    assert len(duplicates) == 1
    assert "my_custom_id" in str(duplicates[0].message)

    assert schema["paths"]["/explicit"]["post"]["operationId"] == "my_custom_id"
    assert schema["paths"]["/explicit"]["delete"]["operationId"] == "my_custom_id"


def test_multiple_methods_with_custom_generate_unique_id_function():
    def custom(route: APIRoute) -> str:
        assert route.methods is not None
        method = next(iter(route.methods)).lower()
        return f"custom_{route.name}_{method}"

    app = FastAPI(generate_unique_id_function=custom)

    def handler():
        return {}  # pragma: nocover

    app.add_api_route("/custom", handler, methods=["POST", "DELETE"])

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        schema = app.openapi()

    assert _no_duplicate_warnings(caught) == []
    assert schema["paths"]["/custom"]["post"]["operationId"] == "custom_handler_post"
    assert (
        schema["paths"]["/custom"]["delete"]["operationId"] == "custom_handler_delete"
    )


def test_single_method_route_unchanged():
    app = FastAPI()

    @app.post("/one")
    def one():
        return {}  # pragma: nocover

    schema = app.openapi()
    assert schema["paths"]["/one"]["post"]["operationId"] == "one_one_post"


def test_multiple_methods_via_router_include():
    router = APIRouter()

    def handler():
        return {}  # pragma: nocover

    router.add_api_route("/r", handler, methods=["POST", "DELETE"])

    app = FastAPI()
    app.include_router(router)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        schema = app.openapi()

    assert _no_duplicate_warnings(caught) == []
    post_id = schema["paths"]["/r"]["post"]["operationId"]
    delete_id = schema["paths"]["/r"]["delete"]["operationId"]
    assert post_id != delete_id


def test_multiple_methods_response_model_name_still_stable():
    app = FastAPI()

    def handler():
        return {"ok": True}  # pragma: nocover

    app.add_api_route("/stable", handler, methods=["POST", "DELETE"])

    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "methods",
    [
        ["GET", "POST"],
        ["GET", "POST", "PUT", "DELETE", "PATCH"],
    ],
)
def test_many_method_combinations_produce_unique_ids(methods):
    app = FastAPI()

    def handler():
        return {}  # pragma: nocover

    app.add_api_route("/multi", handler, methods=methods)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        schema = app.openapi()

    assert _no_duplicate_warnings(caught) == []
    ops = schema["paths"]["/multi"]
    ids = [ops[m.lower()]["operationId"] for m in methods]
    assert len(set(ids)) == len(methods)
