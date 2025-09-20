import pytest
from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute


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

    # Dynamic routes
    @router.get("/users/{user_id}")
    def user(user_id: str):
        return {"route": f"user-{user_id}"}

    app.include_router(router)
    return app


def test_route_sort_key_direct(app_with_routes):
    """
    Test FastAPI._route_sort_key directly on app routes.

    Verifies that static routes have lower dynamic segment counts
    than dynamic routes, and that static segment counts are
    correctly considered in the sort key.

    Args:
        app_with_routes: FastAPI fixture with pre-registered routes.

    Asserts:
        - Static routes have dyn_count 0
        - Dynamic routes have dyn_count >= 1
        - Static segment ordering is correct for comparison
    """
    app = app_with_routes
    # Assume _route_sort_key is added to app instance
    sort_key = app._route_sort_key

    # Grab the routes
    routes = [r for r in app.router.routes if isinstance(r, APIRoute)]

    keys = [sort_key(r) for r in routes]

    # The static /users and /users/admin should have smaller dyn count than dynamic /users/{user_id}
    dyn_counts = [k[0] for k in keys]
    assert dyn_counts[0] == 0
    assert dyn_counts[1] == 0
    assert dyn_counts[2] == 1  # /users/{user_id} has 1 dynamic segment

    # Check the static segments count ordering
    static_counts = [-k[1] for k in keys]
    assert static_counts[0] == 1  # /users
    assert static_counts[1] == 2  # /users/admin
    assert static_counts[2] == 1  # /users/{user_id}
