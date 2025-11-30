import warnings

from fastapi import FastAPI
from fastapi.routing import APIRouter, _detect_route_conflicts
from fastapi.testclient import TestClient
from starlette.routing import Mount


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

        # Add the exact same route path again - FastAPI will overwrite it
        @app.get("/items/sync")
        def sync_items_v2():
            return {"version": 2}

    # Should have 0 warnings - identical paths are explicitly excluded from conflict detection
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


def test_no_conflict_with_websocket_routes():
    """Test that WebSocket routes don't trigger conflict warnings."""
    from fastapi import WebSocket

    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # WebSocket route with dynamic path
        @app.websocket("/ws/{client_id}")
        async def websocket_endpoint(websocket: WebSocket, client_id: str):
            await websocket.accept()
            await websocket.close()

        # Regular API route that could conflict if both were APIRoute
        @app.get("/ws/test")
        def get_ws_test():
            return {"test": "ok"}

        # Should NOT warn - WebSocket routes are not APIRoute instances
        assert len(w) == 0


def test_no_conflict_with_mount():
    """Test that Mount routes don't trigger conflict warnings."""
    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # Add a regular route first
        @app.get("/static/test")
        def get_static_test():
            return {"test": "ok"}

        # Add a Mount - this should not trigger warnings
        # Mounting another FastAPI app creates a Mount route
        sub_app = FastAPI()
        app.mount("/static", sub_app)

        # Should NOT warn - Mount is not an APIRoute
        route_conflict_warnings = [
            warning for warning in w if "shadow" in str(warning.message).lower()
        ]
        assert len(route_conflict_warnings) == 0


def test_detect_route_conflicts_with_non_apiroute():
    """Test _detect_route_conflicts directly with non-APIRoute as new_route."""
    app = FastAPI()

    @app.get("/test")
    def test_route():
        return {"test": "ok"}

    # Create a Mount route (not an APIRoute)
    mount_route = Mount("/static", app=FastAPI(), name="static")

    # Call _detect_route_conflicts directly with a non-APIRoute
    conflicts = _detect_route_conflicts(mount_route, app.routes)  # type: ignore

    assert conflicts == []


def test_websocket_conflict_detection():
    """Test that WebSocket routes can also be checked for conflicts."""
    from fastapi import WebSocket

    app = FastAPI()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        @app.websocket("/ws/{client_id}")
        async def websocket_dynamic(websocket: WebSocket, client_id: str):
            await websocket.accept()
            await websocket.close()

        @app.websocket("/ws/test")
        async def websocket_static(websocket: WebSocket):
            await websocket.accept()
            await websocket.close()

        # WebSocket routes are not checked yet (would need to call _detect_route_conflicts)
        # For now, no warnings since it's not called during app.websocket()
        assert len(w) == 0


def test_route_type_isolation():
    """Test that only routes of the same type are compared for conflicts."""
    from fastapi import WebSocket

    app = FastAPI()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        # Add routes of different types with overlapping paths
        @app.get("/test/{id}")
        def get_test(id: str):
            return {"id": id}

        @app.websocket("/test/ws")
        async def ws_test(websocket: WebSocket):
            await websocket.accept()
            await websocket.close()

        @app.get("/test/static")
        def get_static():
            return {"static": True}

    # Get the routes
    api_routes = [r for r in app.routes if type(r).__name__ == "APIRoute"]
    ws_routes = [r for r in app.routes if type(r).__name__ == "APIWebSocketRoute"]

    # Test that APIRoute conflicts are detected within same type
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        conflicts = _detect_route_conflicts(api_routes[-1], api_routes[:-1])  # type: ignore
        assert len(conflicts) == 1  # /test/static vs /test/{id}

    # Test that WebSocket routes don't interfere with API routes
    # Call with WebSocket route against API routes
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        ws_conflicts = _detect_route_conflicts(ws_routes[0], api_routes)  # type: ignore
        assert len(ws_conflicts) == 0  # Different types, no conflicts

    # Test with API route against WebSocket routes
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        api_conflicts = _detect_route_conflicts(api_routes[0], ws_routes)  # type: ignore
        assert len(api_conflicts) == 0  # Different types, no conflicts


def test_mount_route_without_path_regex():
    """Test that Mount routes (which lack path_regex) are handled safely."""
    from starlette.routing import Mount

    sub_app = FastAPI()
    mount = Mount("/static", app=sub_app, name="static")

    app = FastAPI()

    @app.get("/test")
    def test_route():
        return {"test": "ok"}

    conflicts = _detect_route_conflicts(mount, app.routes)  # type: ignore
    assert conflicts == []


def test_api_route_against_mount_routes():
    """Test that API routes skip Mount routes during conflict detection."""
    from starlette.routing import Mount

    app = FastAPI()

    @app.get("/api/{resource}")
    def get_resource(resource: str):
        return {"resource": resource}

    # Add a Mount route
    sub_app = FastAPI()
    mount = Mount("/api/static", app=sub_app, name="static")

    # Get the API route
    api_routes = [r for r in app.routes if type(r).__name__ == "APIRoute"]
    new_route = api_routes[0]

    conflicts = _detect_route_conflicts(new_route, [mount])  # type: ignore
    assert conflicts == []


def test_websocket_route_without_methods():
    """Test that WebSocket routes (which have no methods attribute) can be checked for conflicts."""
    from fastapi import WebSocket

    app = FastAPI()

    @app.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: str):
        await websocket.accept()
        await websocket.close()

    @app.websocket("/ws/special")
    async def websocket_special(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    # Get WebSocket routes
    ws_routes = [r for r in app.routes if type(r).__name__ == "APIWebSocketRoute"]

    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        conflicts = _detect_route_conflicts(ws_routes[-1], ws_routes[:-1])  # type: ignore

        # Should detect conflict even without methods attribute
        assert len(conflicts) == 1
        assert "/ws/special" in conflicts[0]
        assert "/ws/{client_id}" in conflicts[0]


def test_route_without_path_regex_attribute():
    """Test defensive code for routes that truly lack path_regex attribute."""
    from starlette.routing import BaseRoute

    class CustomRouteWithoutPathRegex(BaseRoute):
        """Custom route class without path_regex attribute."""

        def __init__(self):
            self.path = "/custom"

    custom_route = CustomRouteWithoutPathRegex()

    app = FastAPI()

    @app.get("/test")
    def test_route():
        return {"test": "ok"}

    conflicts = _detect_route_conflicts(custom_route, app.routes)  # type: ignore
    assert conflicts == []


def test_route_with_path_regex_but_no_path():
    """Test defensive code for routes with path_regex but path is None."""
    import re

    from starlette.routing import BaseRoute

    class CustomRouteWithoutPath(BaseRoute):
        """Custom route class with path_regex but no path."""

        def __init__(self):
            self.path_regex = re.compile(r"/custom")
            self.methods = {"GET"}
            self.path = None

    custom_route = CustomRouteWithoutPath()

    app = FastAPI()

    @app.get("/test")
    def test_route():
        return {"test": "ok"}

    conflicts = _detect_route_conflicts(custom_route, app.routes)  # type: ignore
    assert conflicts == []


def test_existing_route_without_path_regex_in_loop():
    """Test that existing routes without path_regex are skipped in the loop."""
    from starlette.routing import BaseRoute

    class CustomExistingRouteWithoutPathRegex(BaseRoute):
        """Custom route without path_regex."""

        def __init__(self):
            self.path = "/existing"

    app = FastAPI()

    @app.get("/test/{id}")
    def test_route(id: str):
        return {"id": id}

    api_routes = [r for r in app.routes if type(r).__name__ == "APIRoute"]
    new_route = api_routes[0]

    custom_existing = CustomExistingRouteWithoutPathRegex()
    custom_existing.__class__ = type(new_route)

    conflicts = _detect_route_conflicts(new_route, [custom_existing])  # type: ignore
    assert conflicts == []


def test_existing_route_with_none_path_in_loop():
    """Test that existing routes with None path are skipped in the loop."""
    import re

    from starlette.routing import BaseRoute

    class CustomExistingRouteWithNonePath(BaseRoute):
        """Custom route with path_regex but path is None."""

        def __init__(self):
            self.path_regex = re.compile(r"/existing")
            self.path = None
            self.methods = {"GET"}

    app = FastAPI()

    @app.get("/test/{id}")
    def test_route(id: str):
        return {"id": id}

    api_routes = [r for r in app.routes if type(r).__name__ == "APIRoute"]
    new_route = api_routes[0]

    custom_existing = CustomExistingRouteWithNonePath()
    custom_existing.__class__ = type(new_route)

    conflicts = _detect_route_conflicts(new_route, [custom_existing])  # type: ignore
    assert conflicts == []
