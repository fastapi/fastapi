"""
Regression tests for https://github.com/fastapi/fastapi/issues/XXXX

When a FastAPI route is registered with multiple HTTP methods
(e.g. methods=["GET", "POST"]), the OpenAPI schema must assign a *unique*
operationId to every operation.  Before the fix, all operations on such a
route shared the same operationId (the one baked into route.unique_id at
construction time), which is invalid per the OpenAPI 3.x specification and
caused a spurious "Duplicate Operation ID" UserWarning on every schema
generation.
"""

import warnings

import pytest
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from starlette.requests import Request


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _handler(request: Request) -> dict:
    return {"method": request.method}


# ---------------------------------------------------------------------------
# Core bug: duplicate operationId
# ---------------------------------------------------------------------------


def test_multi_method_route_generates_unique_operation_ids() -> None:
    """Each HTTP method of a multi-method route must get its own operationId."""
    app = FastAPI()
    app.add_api_route("/multi", _handler, methods=["GET", "POST"], name="multi_handler")

    client = TestClient(app)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        response = client.get("/openapi.json")

    assert response.status_code == 200

    # No duplicate-operation-ID warning must be emitted
    dup_warnings = [w for w in caught if "Duplicate Operation ID" in str(w.message)]
    assert dup_warnings == [], f"Unexpected duplicate-ID warnings: {dup_warnings}"

    paths = response.json()["paths"]
    assert "/multi" in paths
    get_op_id = paths["/multi"]["get"]["operationId"]
    post_op_id = paths["/multi"]["post"]["operationId"]

    assert get_op_id != post_op_id, (
        f"GET and POST operations share the same operationId {get_op_id!r}; "
        "they must be unique"
    )
    assert "get" in get_op_id.lower(), f"Expected 'get' in {get_op_id!r}"
    assert "post" in post_op_id.lower(), f"Expected 'post' in {post_op_id!r}"


def test_three_method_route_all_operation_ids_unique() -> None:
    """A route with three methods must produce three distinct operationIds."""
    app = FastAPI()
    app.add_api_route(
        "/resource",
        _handler,
        methods=["GET", "POST", "PUT"],
        name="resource_handler",
    )

    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200

    ops = response.json()["paths"]["/resource"]
    ids = [ops[m]["operationId"] for m in ("get", "post", "put")]
    assert len(set(ids)) == 3, f"Expected 3 unique operationIds, got {ids}"


# ---------------------------------------------------------------------------
# Backward compatibility: single-method routes must be unchanged
# ---------------------------------------------------------------------------


def test_single_method_routes_operation_ids_unchanged() -> None:
    """
    Single-method routes (the overwhelming majority) must generate the same
    operationId as they did before the fix.
    """
    app = FastAPI()

    @app.get("/items")
    def get_items() -> list:
        return []  # pragma: no cover

    @app.post("/items")
    def create_item() -> dict:
        return {}  # pragma: no cover

    @app.put("/items/{item_id}")
    def update_item(item_id: int) -> dict:
        return {}  # pragma: no cover

    @app.delete("/items/{item_id}")
    def delete_item(item_id: int) -> None:
        return None  # pragma: no cover

    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200

    paths = response.json()["paths"]
    assert paths["/items"]["get"]["operationId"] == "get_items_items_get"
    assert paths["/items"]["post"]["operationId"] == "create_item_items_post"
    assert paths["/items/{item_id}"]["put"]["operationId"] == "update_item_items__item_id__put"
    assert paths["/items/{item_id}"]["delete"]["operationId"] == "delete_item_items__item_id__delete"


# ---------------------------------------------------------------------------
# Explicit operation_id always wins (unchanged behaviour)
# ---------------------------------------------------------------------------


def test_explicit_operation_id_not_affected() -> None:
    """
    When a route has an explicit operation_id, it is used as-is for every
    method on that route, exactly as before.
    """
    app = FastAPI()
    app.add_api_route(
        "/explicit",
        _handler,
        methods=["GET", "POST"],
        name="explicit_handler",
        operation_id="my_custom_operation",
    )

    client = TestClient(app)

    # Explicit duplicate operation IDs will still warn – that's expected and
    # intentional (the user set them explicitly).
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        response = client.get("/openapi.json")

    paths = response.json()["paths"]["/explicit"]
    assert paths["get"]["operationId"] == "my_custom_operation"
    assert paths["post"]["operationId"] == "my_custom_operation"


# ---------------------------------------------------------------------------
# Router-level routes
# ---------------------------------------------------------------------------


def test_multi_method_route_via_api_router() -> None:
    """Multi-method routes added via APIRouter must also get unique operationIds."""
    router = APIRouter()
    router.add_api_route(
        "/things",
        _handler,
        methods=["GET", "POST"],
        name="things_handler",
    )

    app = FastAPI()
    app.include_router(router)

    client = TestClient(app)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        response = client.get("/openapi.json")

    dup_warnings = [w for w in caught if "Duplicate Operation ID" in str(w.message)]
    assert dup_warnings == [], f"Unexpected duplicate-ID warnings: {dup_warnings}"

    ops = response.json()["paths"]["/things"]
    get_op_id = ops["get"]["operationId"]
    post_op_id = ops["post"]["operationId"]
    assert get_op_id != post_op_id


# ---------------------------------------------------------------------------
# Determinism: unique_id must not change across runs
# ---------------------------------------------------------------------------


def test_generate_unique_id_is_deterministic() -> None:
    """
    generate_unique_id must return the same value regardless of set-iteration
    order (i.e. it must not depend on PYTHONHASHSEED).
    """
    from fastapi.utils import generate_unique_id

    app = FastAPI()
    app.add_api_route(
        "/stable",
        _handler,
        methods=["POST", "GET"],  # intentionally reversed order
        name="stable_handler",
    )

    route = next(r for r in app.routes if getattr(r, "name", None) == "stable_handler")
    uid1 = generate_unique_id(route)

    # Call again – must be identical
    uid2 = generate_unique_id(route)
    assert uid1 == uid2

    # The baked-in method must be the alphabetically first one ("get" < "post")
    assert uid1.endswith("_get"), (
        f"Expected unique_id to end with '_get' (sorted first), got {uid1!r}"
    )
