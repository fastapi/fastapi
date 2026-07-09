from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient


def test_static_route_caching():
    app = FastAPI()
    router = APIRouter()

    @router.get("/static")
    def read_static():
        return {"status": "ok"}

    @router.get("/users/{user_id}")
    def read_user(user_id: int):
        return {"user_id": user_id}

    app.include_router(router)
    client = TestClient(app)

    # First request: Cache miss, resolves normally
    response = client.get("/static")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    # Check cache size (should be 1)
    cache = app.router._route_cache
    assert len(cache) == 1
    cache_key = ("http", "GET", "/static")
    assert cache_key in cache

    # Second request: Cache hit, resolves via cache
    response = client.get("/static")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert len(cache) == 1

    # Dynamic request: matches but should not be cached
    response = client.get("/users/123")
    assert response.status_code == 200
    assert response.json() == {"user_id": 123}
    assert cache_key in cache
    # Verify dynamic path is not added to the cache
    assert len(cache) == 1
    assert ("http", "GET", "/users/123") not in cache


def test_cache_invalidation():
    app = FastAPI()
    router = APIRouter()

    @router.get("/health")
    def health():
        return {"status": "healthy"}

    app.include_router(router)
    client = TestClient(app)

    # First request
    response = client.get("/health")
    assert response.status_code == 200
    assert len(app.router._route_cache) == 1

    # Invalidate by adding a new route dynamically
    @app.get("/new-route")
    def new_route():
        return {"new": "yes"}

    # Cache should be cleared
    assert len(app.router._route_cache) == 0

    # Request new route and health route to populate cache again
    client.get("/new-route")
    client.get("/health")
    assert len(app.router._route_cache) == 2
