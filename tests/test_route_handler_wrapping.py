from functools import wraps

import pytest
from fastapi import APIRouter, Depends, FastAPI, routing
from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient


@pytest.mark.parametrize("include_router", [False, True], ids=["direct", "included"])
def test_endpoint_wrapper_does_not_accumulate_across_requests(
    monkeypatch, include_router
):
    original_get_request_handler = routing.get_request_handler
    wrapper_calls = 0

    def get_request_handler_with_endpoint_wrapper(*args, **kwargs):
        # Older Sentry SDKs wrap dependant.call each time a handler is built.
        # Accumulating these wrappers eventually exhausts the recursion limit.
        dependant = kwargs["dependant"]
        original_call = dependant.call

        @wraps(original_call)
        def wrapped_endpoint(*args, **kwargs):
            nonlocal wrapper_calls
            wrapper_calls += 1
            return original_call(*args, **kwargs)

        dependant.call = wrapped_endpoint
        return original_get_request_handler(*args, **kwargs)

    monkeypatch.setattr(
        routing, "get_request_handler", get_request_handler_with_endpoint_wrapper
    )

    app = FastAPI()
    router = APIRouter() if include_router else app.router

    @router.get("/items/{item_id}")
    def read_item(item_id: str):
        return {"item_id": item_id}

    if include_router:
        app.include_router(router)

    calls_per_request = []
    with TestClient(app) as client:
        for item_id in ("first", "second", "third"):
            wrapper_calls = 0
            response = client.get(f"/items/{item_id}")
            assert response.status_code == 200
            assert response.json() == {"item_id": item_id}
            calls_per_request.append(wrapper_calls)

    assert calls_per_request == [1, 1, 1]


def test_custom_handlers_are_cached_separately_for_nested_inclusions():
    built_handlers = []

    class CustomRoute(routing.APIRoute):
        def get_route_handler(self):
            handler = super().get_route_handler()
            built_handlers.append(handler)
            handler_id = str(len(built_handlers))

            async def custom_handler(request):
                response = await handler(request)
                response.headers["x-handler-id"] = handler_id
                return response

            return custom_handler

    router = APIRouter(route_class=CustomRoute)

    @router.get("/{item_id}")
    def read_item(item_id: str):
        return item_id

    parent = APIRouter()
    parent.include_router(router, prefix="/json")
    parent.include_router(
        router, prefix="/text", default_response_class=PlainTextResponse
    )
    app = FastAPI()
    app.include_router(parent, prefix="/api")

    with TestClient(app) as client:
        first_json = client.get("/api/json/first")
        first_text = client.get("/api/text/first")
        json_handler_id = first_json.headers["x-handler-id"]
        text_handler_id = first_text.headers["x-handler-id"]
        assert json_handler_id != text_handler_id
        built_count = len(built_handlers)

        for item_id in ("second", "third"):
            json_response = client.get(f"/api/json/{item_id}")
            assert json_response.status_code == 200
            assert json_response.json() == item_id
            assert json_response.headers["x-handler-id"] == json_handler_id
            text_response = client.get(f"/api/text/{item_id}")
            assert text_response.status_code == 200
            assert text_response.text == item_id
            assert text_response.headers["x-handler-id"] == text_handler_id

    assert len(built_handlers) == built_count


def test_cached_handler_uses_live_dependency_overrides_and_route_additions():
    router = APIRouter()

    def dependency():
        return "original"

    @router.get("/items")
    def read_items(value: str = Depends(dependency)):
        return value

    app = FastAPI()
    app.include_router(router, prefix="/api")

    with TestClient(app) as client:
        assert client.get("/api/items").json() == "original"
        app.dependency_overrides[dependency] = lambda: "overridden"
        assert client.get("/api/items").json() == "overridden"

        @router.get("/later")
        def read_later(value: str = Depends(dependency)):
            return value

        assert client.get("/api/items").json() == "overridden"
        assert client.get("/api/later").json() == "overridden"
        app.dependency_overrides.clear()
        assert client.get("/api/items").json() == "original"
        assert client.get("/api/later").json() == "original"


def test_failed_handler_construction_restores_context_and_can_retry():
    fail = False

    class CustomRoute(routing.APIRoute):
        def get_route_handler(self):
            if fail:
                raise RuntimeError("handler construction failed")
            return super().get_route_handler()

    router = APIRouter(route_class=CustomRoute)

    @router.get("/items")
    def read_items():
        return ["item"]

    app = FastAPI()
    app.include_router(router, prefix="/api")
    fail = True
    assert routing._effective_route_context_var.get() is None
    with pytest.raises(RuntimeError, match="handler construction failed"):
        app.openapi()
    assert routing._effective_route_context_var.get() is None

    fail = False
    assert "/api/items" in app.openapi()["paths"]
    assert routing._effective_route_context_var.get() is None
    with TestClient(app) as client:
        assert client.get("/api/items").json() == ["item"]
