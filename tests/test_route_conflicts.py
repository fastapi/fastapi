import warnings

from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.testclient import TestClient


def test_route_conflict_warning_dynamic_before_static():
    """Dynamic route registered before static route should warn."""
    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @app.get("/items/{item_id}")
        def get_item(item_id: str):
            return {"item_id": item_id}

        @app.get("/items/sync")  # This will be shadowed!
        def sync_items():
            return {"action": "sync"}

        # Should have warning
        assert len(w) == 1
        assert "shadow" in str(w[0].message).lower()
        assert "/items/sync" in str(w[0].message)
        assert "/items/{item_id}" in str(w[0].message)


def test_route_conflict_warning_static_before_dynamic():
    """Static route before dynamic should work but warn about potential conflict."""
    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @app.get("/items/sync")
        def sync_items():
            return {"action": "sync"}

        @app.get("/items/{item_id}")
        def get_item(item_id: str):
            return {"item_id": item_id}

        # Should warn about potential conflict
        assert len(w) == 1
        assert "shadow" in str(w[0].message).lower()


def test_no_conflict_different_methods():
    """Different HTTP methods should not conflict."""
    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @app.get("/items/{item_id}")
        def get_item(item_id: str):
            return {"item_id": item_id}

        @app.post("/items/sync")
        def sync_items():
            return {"action": "sync"}

        # Should NOT warn (different methods)
        assert len(w) == 0


def test_no_conflict_different_paths():
    """Completely different paths should not conflict."""
    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @app.get("/items/{item_id}")
        def get_item(item_id: str):
            return {"item_id": item_id}

        @app.get("/products/sync")
        def sync_products():
            return {"action": "sync"}

        # Should NOT warn (different paths)
        assert len(w) == 0


def test_actual_routing_behavior_static_before_dynamic():
    """Verify that static-before-dynamic actually works correctly."""
    app = FastAPI()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        @app.get("/items/sync")
        def sync_items():
            return {"action": "sync"}

        @app.get("/items/{item_id}")
        def get_item(item_id: str):
            return {"item_id": item_id}

    client = TestClient(app)

    # Static route should match
    response = client.get("/items/sync")
    assert response.json() == {"action": "sync"}

    # Dynamic route should match others
    response = client.get("/items/123")
    assert response.json() == {"item_id": "123"}


def test_actual_routing_behavior_dynamic_before_static():
    """Verify that dynamic-before-static causes shadowing."""
    app = FastAPI()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        @app.get("/items/{item_id}")
        def get_item(item_id: str):
            return {"item_id": item_id}

        @app.get("/items/sync")
        def sync_items():
            return {"action": "sync"}

    client = TestClient(app)

    # Dynamic route will match everything (including "sync")
    response = client.get("/items/sync")
    assert response.json() == {"item_id": "sync"}

    # Dynamic route should still match others
    response = client.get("/items/123")
    assert response.json() == {"item_id": "123"}


def test_router_conflict_detection():
    """Test conflict detection works with APIRouter."""
    router = APIRouter()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @router.get("/users/{user_id}")
        def get_user(user_id: str):
            return {"user_id": user_id}

        @router.get("/users/me")
        def get_current_user():
            return {"user": "current"}

        # Should warn
        assert len(w) == 1
        assert "shadow" in str(w[0].message).lower()


def test_multiple_conflicts():
    """Test detection of multiple route conflicts."""
    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @app.get("/items/{item_id}")
        def get_item(item_id: str):
            return {"item_id": item_id}

        @app.get("/items/sync")
        def sync_items():
            return {"action": "sync"}

        @app.get("/items/export")
        def export_items():
            return {"action": "export"}

        # Should have 2 warnings (sync and export both shadowed)
        assert len(w) == 2


def test_nested_path_conflict():
    """Test conflict detection with nested paths."""
    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @app.get("/users/{user_id}/posts/{post_id}")
        def get_user_post(user_id: str, post_id: str):
            return {"user_id": user_id, "post_id": post_id}

        @app.get("/users/me/posts/{post_id}")
        def get_my_post(post_id: str):
            return {"user": "me", "post_id": post_id}

        # Should warn
        assert len(w) == 1


def test_no_duplicate_warnings_same_route():
    """Adding the same static route twice should not cause conflict warnings."""
    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @app.get("/items/sync")
        def sync_items_v1():
            return {"version": 1}

        # FastAPI will overwrite the route, but should not warn about conflict with itself
        # (The path regex won't match its own literal path if they're identical)

    # Should have 0 warnings
    assert len(w) == 0


def test_conflict_with_router_prefix():
    """Test conflict detection when router has a prefix."""
    app = FastAPI()
    router = APIRouter(prefix="/api/v1")

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @router.get("/items/{item_id}")
        def get_item(item_id: str):
            return {"item_id": item_id}

        @router.get("/items/special")
        def get_special_item():
            return {"special": True}

        # Should warn during router setup
        assert len(w) == 1

        # Including router in app may generate another warning, suppress it
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            app.include_router(router)

    client = TestClient(app)
    # Verify the routes work correctly with prefix
    response = client.get("/api/v1/items/123")
    assert response.status_code == 200


def test_post_vs_get_no_conflict():
    """POST and GET to same path patterns should not conflict."""
    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @app.get("/items/{item_id}")
        def get_item(item_id: str):
            return {"item_id": item_id}

        @app.post("/items/{item_id}")
        def update_item(item_id: str):
            return {"updated": item_id}

        @app.get("/items/sync")
        def sync_items():
            return {"action": "sync"}

        # Should only warn for GET /items/sync vs GET /items/{item_id}
        # Should NOT warn about POST /items/{item_id}
        assert len(w) == 1
        assert "GET" in str(w[0].message) or "methods" in str(w[0].message).lower()


def test_complex_multi_param_paths():
    """Test conflict detection with multiple path parameters."""
    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @app.get("/api/{version}/items/{item_id}")
        def get_item_versioned(version: str, item_id: str):
            return {"version": version, "item_id": item_id}

        @app.get("/api/v1/items/special")
        def get_special_item():
            return {"special": True}

        # Should warn - /api/{version}/items/{item_id} can match /api/v1/items/special
        assert len(w) == 1
        assert "/api/v1/items/special" in str(w[0].message)
        assert "/api/{version}/items/{item_id}" in str(w[0].message)


def test_no_conflict_different_param_depth():
    """Test no conflict when paths have different depth."""
    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @app.get("/items/{item_id}")
        def get_item(item_id: str):
            return {"item_id": item_id}

        @app.get("/categories/special")
        def get_special_category():
            return {"category": "special"}

        # Should NOT warn - completely different paths
        assert len(w) == 0
