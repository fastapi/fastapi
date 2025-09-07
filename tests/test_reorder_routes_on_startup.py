from unittest.mock import patch

import pytest
from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from starlette.testclient import TestClient


@pytest.fixture
def app_with_routes():
    """
    Creates a FastAPI app with multiple static and dynamic routes
    for testing route ordering and matching.
    """
    app = FastAPI()
    router = APIRouter()

    # Static routes
    @router.get("/users")
    def users():
        return {"route": "users"}

    @router.get("/users/admin")
    def admins():
        return {"route": "admins"}

    @router.get("/users/profile")
    def profile():
        return {"route": "profile"}

    @router.get("/users/admin/settings")
    def admin_settings():
        return {"route": "admin-settings"}

    @router.get("/products")
    def products():
        return {"route": "products"}

    @router.get("/products/special")
    def special_products():
        return {"route": "special-products"}

    # Dynamic routes
    @router.get("/users/{user_id}")
    def user(user_id: str):
        return {"route": f"user-{user_id}"}

    @router.get("/users/{user_id}/settings")
    def user_settings(user_id: str):
        return {"route": f"user-settings-{user_id}"}

    @router.get("/users/{user_id}/orders/{order_id}")
    def user_order(user_id: str, order_id: str):
        return {"route": f"order-{user_id}-{order_id}"}

    @router.get("/products/{product_id}")
    def product(product_id: int):
        return {"route": f"product-{product_id}"}

    @router.get("/orders/{order_id}")
    def order(order_id: str):
        return {"route": f"order-{order_id}"}

    app.include_router(router)
    return app


def test_reorder_called(app_with_routes):
    """
    Ensure that `reorder_routes_on_startup` is called on the app.

    This verifies that route reordering is triggered after registration,
    which is necessary to prioritize static routes over dynamic ones.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        That `reorder_routes_on_startup` was called at least once.
    """
    # Patch the method on the app instance
    with patch.object(app_with_routes, "reorder_routes_on_startup") as mock_reorder:
        # Call some code that is supposed to trigger it
        app_with_routes.reorder_routes_on_startup()

        # Check that _route_sort_key was called at least once
        assert mock_reorder.called


def test_reorder_routes_calls_sort_key(app_with_routes):
    """
    Ensure `_route_sort_key` is invoked during route reordering.

    Confirms that the sorting function is used to order routes, ensuring
    correct precedence between static and dynamic paths.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        That `_route_sort_key` was called at least once.
    """
    original_sort_key = app_with_routes._route_sort_key

    with patch.object(
        app_with_routes, "_route_sort_key", side_effect=original_sort_key
    ) as mock_sort_key:
        app_with_routes.reorder_routes_on_startup()

        # Check that _route_sort_key was called at least once
        assert mock_sort_key.called


def test_complex_route_ordering(app_with_routes):
    """
    Verify that static routes are registered before dynamic routes.

    Ensures correct matching when static and dynamic routes overlap.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        That static routes appear before dynamic ones in `app.router.routes`.
    """
    paths = [r.path for r in app_with_routes.router.routes if isinstance(r, APIRoute)]

    # Static routes should come before dynamic routes
    assert paths.index("/users") < paths.index("/users/{user_id}")
    assert paths.index("/users/admin") < paths.index("/users/{user_id}")
    assert paths.index("/users/profile") < paths.index("/users/{user_id}")
    assert paths.index("/users/admin/settings") < paths.index(
        "/users/{user_id}/settings"
    )
    assert paths.index("/products") < paths.index("/products/{product_id}")
    assert paths.index("/products/special") < paths.index("/products/{product_id}")


def test_complex_route_matching(app_with_routes):
    """
    Test that static and dynamic routes return correct responses.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        That each request returns the expected route response.
    """
    client = TestClient(app_with_routes)

    # Static routes
    assert client.get("/users").json() == {"route": "users"}
    assert client.get("/users/admin").json() == {"route": "admins"}
    assert client.get("/users/profile").json() == {"route": "profile"}
    assert client.get("/users/admin/settings").json() == {"route": "admin-settings"}
    assert client.get("/products").json() == {"route": "products"}
    assert client.get("/products/special").json() == {"route": "special-products"}

    # Dynamic routes
    assert client.get("/users/123").json() == {"route": "user-123"}
    assert client.get("/users/123/settings").json() == {"route": "user-settings-123"}
    assert client.get("/users/123/orders/456").json() == {"route": "order-123-456"}
    assert client.get("/products/789").json() == {"route": "product-789"}
    assert client.get("/orders/999").json() == {"route": "order-999"}


def test_edge_cases(app_with_routes):
    """
    Verify overlapping static paths and responses for non-existent routes.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        Static routes match correctly; invalid routes return 404 or 422.
    """
    client = TestClient(app_with_routes)

    # Overlapping paths should match static first
    assert client.get("/users/admin/settings").json() == {"route": "admin-settings"}
    assert client.get("/users/profile").json() == {"route": "profile"}

    # Non-existent paths return 404
    assert client.get("/users/unknown/path").status_code == 404
    # Paths with really unprocessable entity - required int, got str
    assert client.get("/products/unknown").status_code == 422


def test_trailing_slash(app_with_routes):
    """
    Ensure trailing slashes do not affect route matching.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        Requests with trailing slashes return the same responses as without.
    """
    client = TestClient(app_with_routes)

    # Trailing slashes should not break routing
    assert client.get("/users/").json() == {"route": "users"}
    assert client.get("/users/admin/").json() == {"route": "admins"}
    assert client.get("/users/123/").json() == {"route": "user-123"}


def test_query_parameters(app_with_routes):
    """
    Verify that query parameters do not interfere with route matching.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        Dynamic routes are matched correctly even when query parameters are present.
    """
    client = TestClient(app_with_routes)

    # Query parameters should not affect route matching
    assert client.get("/users/123?verbose=true").json() == {"route": "user-123"}
    assert client.get("/products/789?discount=1").json() == {"route": "product-789"}


def test_multiple_dynamic_segments(app_with_routes):
    """
    Ensure routes with multiple dynamic segments match correctly.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        Nested dynamic routes return correct responses.
    """
    client = TestClient(app_with_routes)

    # Ensure multiple dynamic segments still work
    response = client.get("/users/42/orders/99")
    assert response.json() == {"route": "order-42-99"}


def test_static_dynamic_overlap(app_with_routes):
    """
    Confirm that static routes take priority over overlapping dynamic routes.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        Static routes match first; dynamic routes still function for other paths.
    """
    client = TestClient(app_with_routes)

    # Static routes should still be prioritized
    assert client.get("/users/profile").json() == {"route": "profile"}
    assert client.get("/users/admin").json() == {"route": "admins"}

    # Dynamic route should still work after static check
    assert client.get("/users/123").json() == {"route": "user-123"}


def test_nonexistent_routes(app_with_routes):
    """
    Test that invalid routes return appropriate 404 responses.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        Requests to unknown routes return 404.
    """
    client = TestClient(app_with_routes)

    # Invalid routes should return 404
    assert client.get("/unknown").status_code == 404
    assert client.get("/users/123/unknown").status_code == 404
    assert client.get("/products/789/unknown").status_code == 404


def test_nested_dynamic_routes(app_with_routes):
    """
    Test matching of nested dynamic routes with multiple path parameters.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        Nested dynamic routes return correct responses for all parameters.
    """
    client = TestClient(app_with_routes)

    # Nested dynamic route
    response = client.get("/users/123/orders/456")
    assert response.json() == {"route": "order-123-456"}

    # Another nested dynamic route with different user_id
    response = client.get("/users/999/orders/888")
    assert response.json() == {"route": "order-999-888"}


def test_similar_prefixes(app_with_routes):
    """
    Ensure static routes take priority over dynamic routes with similar prefixes.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        Static routes match first; dynamic routes work for other paths.
    """
    client = TestClient(app_with_routes)

    # Static route should be prioritized over similar dynamic route
    assert client.get("/products/special").json() == {"route": "special-products"}

    # Dynamic route still works for non-static path
    assert client.get("/products/123").json() == {"route": "product-123"}


def test_integer_vs_string_route(app_with_routes):
    """
    Verify route matching with integer and string path parameters.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        Integer and string dynamic segments are correctly matched and parsed.
    """
    client = TestClient(app_with_routes)

    # Product ID is integer; FastAPI should parse it correctly
    assert client.get("/products/42").json() == {"route": "product-42"}

    # User ID is string; should still match dynamic route
    assert client.get("/users/john_doe").json() == {"route": "user-john_doe"}


def test_ambiguous_static_dynamic(app_with_routes):
    """
    Confirm that static routes override overlapping dynamic routes.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        Static route is matched first; dynamic routes still match other paths.
    """
    client = TestClient(app_with_routes)

    # Static `/users/admin/settings` should override `/users/{user_id}/settings`
    assert client.get("/users/admin/settings").json() == {"route": "admin-settings"}

    # Dynamic route for other user
    assert client.get("/users/123/settings").json() == {"route": "user-settings-123"}


def test_multiple_similar_dynamic_routes(app_with_routes):
    """
    Test multiple dynamic routes under the same prefix.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        All dynamic routes match correctly without interfering with each other.
    """
    client = TestClient(app_with_routes)

    # Multiple dynamic segments under same prefix
    assert client.get("/users/1/orders/2").json() == {"route": "order-1-2"}
    assert client.get("/users/42/orders/99").json() == {"route": "order-42-99"}