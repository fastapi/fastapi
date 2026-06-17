from typing import Annotated, cast

import pytest
from fastapi import APIRouter, Body, Depends, FastAPI, Request, Security
from fastapi.exceptions import FastAPIError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.routing import (
    APIRoute,
    RouteContext,
    _IncludedRouter,
    _iter_included_route_candidates,
    _restore_fastapi_scope_key,
    iter_route_contexts,
)
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette.routing import BaseRoute, Host, Match, Mount, NoMatchFound, Route, Router


def dependency_a():
    return "a"


def dependency_b():
    return "b"


def dependency_c():
    return "c"


def unique_id_b(route: APIRoute) -> str:
    return f"b_{route.name}"


def test_iter_route_contexts_returns_direct_route_context():
    router = APIRouter()

    @router.get("/items/{item_id}")
    def read_item(item_id: str):
        return {"item_id": item_id}

    contexts = list(iter_route_contexts(router.routes))

    assert len(contexts) == 1
    assert isinstance(contexts[0], RouteContext)
    assert contexts[0].original_route is router.routes[0]
    assert contexts[0].path == "/items/{item_id}"
    assert contexts[0].path_format == "/items/{item_id}"
    assert contexts[0].methods == {"GET"}
    assert contexts[0].endpoint is read_item


def test_iter_route_contexts_supports_nested_conflict_detection():
    existing_router = APIRouter()
    nested_router = APIRouter()

    @nested_router.get("/{username}")
    def read_user(username: str):
        return {"username": username}

    existing_router.include_router(nested_router, prefix="/auth/user")

    new_router = APIRouter()

    @new_router.get("/auth/user/{username}")
    def read_user_again(username: str):
        return {"username": username}

    existing_paths = {
        context.path for context in iter_route_contexts(existing_router.routes)
    }
    new_paths = {context.path for context in iter_route_contexts(new_router.routes)}

    assert existing_paths & new_paths == {"/auth/user/{username}"}


def test_get_openapi_accepts_filtered_route_contexts_with_effective_paths():
    router = APIRouter()
    bearer_scheme = HTTPBearer()

    @router.get("/public", tags=["public"])
    def read_public(token: Annotated[str, Security(bearer_scheme)]):
        return {"public": True}

    @router.get("/private", tags=["private"])
    def read_private():
        return {"private": True}

    app = FastAPI()
    app.include_router(router, prefix="/api")

    public_routes = [
        context
        for context in iter_route_contexts(app.routes)
        if "public" in getattr(context, "tags", [])
    ]
    schema = get_openapi(
        title="Public API",
        version="1.0.0",
        routes=public_routes,
    )

    assert set(schema["paths"]) == {"/api/public"}
    assert "HTTPBearer" in schema["components"]["securitySchemes"]


def test_get_openapi_accepts_webhook_route_contexts():
    app = FastAPI()
    bearer_scheme = HTTPBearer()

    class Subscription(BaseModel):
        username: str

    @app.webhooks.post("new-subscription")
    def new_subscription(
        body: Subscription, token: Annotated[str, Security(bearer_scheme)]
    ):
        return None

    webhook_contexts = list(iter_route_contexts(app.webhooks.routes))
    schema = get_openapi(
        title="Webhook API",
        version="1.0.0",
        routes=[],
        webhooks=webhook_contexts,
    )

    assert set(schema["webhooks"]) == {"new-subscription"}
    assert "HTTPBearer" in schema["components"]["securitySchemes"]
    assert "Subscription" in schema["components"]["schemas"]


def test_router_include_context_matches_flattened_include_metadata():
    callback_router = APIRouter()

    @callback_router.post("/callback")
    def callback():  # pragma: no cover
        return {"ok": True}

    callback_route = callback_router.routes[0]

    parent_router = APIRouter()
    included_router = APIRouter(
        prefix="/items",
        tags=["router"],
        dependencies=[Depends(dependency_a)],
        responses={401: {"description": "Unauthorized"}},
        callbacks=[callback_route],
        default_response_class=HTMLResponse,
        strict_content_type=False,
    )

    @included_router.get(
        "/{item_id}",
        tags=["route"],
        dependencies=[Depends(dependency_b)],
        responses={404: {"description": "Missing"}},
        callbacks=[callback_route],
        generate_unique_id_function=unique_id_b,
    )
    def read_item(item_id: str, request: Request):
        context = request.scope["fastapi"]["effective_route_context"]
        return JSONResponse(
            {
                "path": context.path,
                "tags": context.tags,
                "dependency_count": len(context.dependencies),
                "response_codes": sorted(context.responses),
                "callback_count": len(context.callbacks or []),
                "deprecated": context.deprecated,
                "include_in_schema": context.include_in_schema,
                "response_class": context.response_class.__name__,
                "generate_unique_id": context.generate_unique_id_function(context),
                "strict_content_type": context.strict_content_type,
                "has_dependency_overrides_provider": (
                    context.dependency_overrides_provider
                    is app.router.dependency_overrides_provider
                ),
            }
        )

    parent_router.include_router(
        included_router,
        prefix="/api",
        tags=["include"],
        dependencies=[Depends(dependency_c)],
        responses={400: {"description": "Bad request"}},
        callbacks=[callback_route],
        deprecated=True,
        include_in_schema=False,
    )

    app = FastAPI()
    app.include_router(parent_router)
    response = TestClient(app).get("/api/items/foo")

    assert response.status_code == 200
    assert response.json() == {
        "path": "/api/items/{item_id}",
        "tags": ["include", "router", "route"],
        "dependency_count": 3,
        "response_codes": [400, 401, 404],
        "callback_count": 3,
        "deprecated": True,
        "include_in_schema": False,
        "response_class": "HTMLResponse",
        "generate_unique_id": "b_read_item",
        "strict_content_type": False,
        "has_dependency_overrides_provider": True,
    }


def test_live_route_addition_uses_include_metadata_for_runtime_and_openapi():
    calls: list[str] = []

    def included_dependency():
        calls.append("dependency")

    router = APIRouter()
    app = FastAPI()
    app.include_router(
        router,
        prefix="/api",
        tags=["included"],
        dependencies=[Depends(included_dependency)],
        responses={418: {"description": "Teapot"}},
    )

    @router.get("/later")
    def read_later():
        return {"later": True}

    client = TestClient(app)
    response = client.get("/api/later")

    assert response.status_code == 200
    assert response.json() == {"later": True}
    assert calls == ["dependency"]
    operation = client.get("/openapi.json").json()["paths"]["/api/later"]["get"]
    assert operation["tags"] == ["included"]
    assert operation["responses"]["418"] == {"description": "Teapot"}


def test_openapi_cache_updates_after_live_route_addition():
    router = APIRouter()
    app = FastAPI()
    app.include_router(router, prefix="/api")
    client = TestClient(app)

    first_schema = client.get("/openapi.json").json()
    assert "/api/later" not in first_schema["paths"]

    @router.get("/later")
    def read_later():  # pragma: no cover
        return {"later": True}

    second_schema = client.get("/openapi.json").json()
    assert "/api/later" in second_schema["paths"]


def test_nested_router_added_after_parent_inclusion_is_live():
    parent_router = APIRouter()
    child_router = APIRouter()
    app = FastAPI()
    app.include_router(parent_router, prefix="/api")
    parent_router.include_router(child_router, prefix="/child", tags=["child"])

    @child_router.get("/items")
    def read_items():
        return ["item"]

    client = TestClient(app)
    response = client.get("/api/child/items")

    assert response.status_code == 200
    assert response.json() == ["item"]
    operation = client.get("/openapi.json").json()["paths"]["/api/child/items"]["get"]
    assert operation["tags"] == ["child"]


def test_repeated_deep_inclusions_handle_all_concrete_paths():
    shared_router = APIRouter()

    @shared_router.get("/items")
    def read_items():
        return []

    parent_router = APIRouter()
    parent_router.include_router(shared_router, prefix="/a")
    parent_router.include_router(shared_router, prefix="/b")

    app = FastAPI()
    app.include_router(parent_router, prefix="/v1")
    app.include_router(parent_router, prefix="/v2")

    client = TestClient(app)
    paths = ["/v1/a/items", "/v1/b/items", "/v2/a/items", "/v2/b/items"]
    for path in paths:
        response = client.get(path)
        assert response.status_code == 200
        assert response.json() == []
    assert set(client.get("/openapi.json").json()["paths"]) == set(paths)


def test_url_path_for_uses_effective_context_for_live_included_route():
    router = APIRouter()
    app = FastAPI()
    app.include_router(router, prefix="/api")

    @router.get("/items/{item_id}", name="read_item")
    def read_item(item_id: str):  # pragma: no cover
        return {"item_id": item_id}

    assert app.url_path_for("read_item", item_id="abc") == "/api/items/abc"


def test_url_path_for_uses_distinct_repeated_inclusion_contexts():
    router = APIRouter()

    @router.get("/items/{item_id}", name="read_item")
    def read_item(item_id: str):  # pragma: no cover
        return {"item_id": item_id}

    parent_router = APIRouter()
    parent_router.include_router(router, prefix="/v1")
    parent_router.include_router(router, prefix="/v2")

    assert parent_router.url_path_for("read_item", item_id="abc") == "/v1/items/abc"
    assert (
        parent_router.routes[1].url_path_for("read_item", item_id="abc")
        == "/v2/items/abc"
    )


def test_indirect_router_inclusion_cycles_are_rejected():
    parent_router = APIRouter()
    child_router = APIRouter()

    parent_router.include_router(child_router, prefix="/child")

    with pytest.raises(AssertionError, match="already includes this router"):
        child_router.include_router(parent_router, prefix="/parent")

    parent_router = APIRouter()
    child_router = APIRouter()
    grandchild_router = APIRouter()

    parent_router.include_router(child_router, prefix="/child")
    child_router.include_router(grandchild_router, prefix="/grandchild")

    with pytest.raises(AssertionError, match="already includes this router"):
        grandchild_router.include_router(parent_router, prefix="/parent")


def test_original_api_route_subclass_instance_is_called_after_inclusion():
    class TrackingRoute(APIRoute):
        calls = 0

        async def handle(self, scope, receive, send):
            self.calls += 1
            await super().handle(scope, receive, send)

    router = APIRouter(route_class=TrackingRoute)

    @router.get("/items")
    def read_items():
        return []

    original_route = router.routes[0]
    assert isinstance(original_route, TrackingRoute)

    app = FastAPI()
    app.include_router(router, prefix="/api")

    response = TestClient(app).get("/api/items")

    assert response.status_code == 200
    assert original_route.calls == 1


def test_original_api_route_get_route_handler_is_called_after_inclusion():
    class TrackingRoute(APIRoute):
        calls = 0

        def get_route_handler(self):
            handler = super().get_route_handler()

            async def custom_handler(request):
                self.calls += 1
                return await handler(request)

            return custom_handler

    router = APIRouter(route_class=TrackingRoute)

    @router.get("/items")
    def read_items():
        return []

    original_route = router.routes[0]
    assert isinstance(original_route, TrackingRoute)
    original_route.calls = 0

    app = FastAPI()
    app.include_router(router, prefix="/api")

    response = TestClient(app).get("/api/items")

    assert response.status_code == 200
    assert original_route.calls == 1


def test_original_api_route_matches_is_called_after_inclusion():
    class HeaderRoute(APIRoute):
        calls = 0

        def matches(self, scope):
            self.calls += 1
            headers = dict(scope.get("headers", []))
            if headers.get(b"x-match") != b"yes":
                return Match.NONE, {}
            return super().matches(scope)

    router = APIRouter(route_class=HeaderRoute)

    @router.get("/items")
    def read_items():
        return []

    original_route = router.routes[0]
    assert isinstance(original_route, HeaderRoute)
    original_route.calls = 0

    app = FastAPI()
    app.include_router(router, prefix="/api")
    client = TestClient(app)

    assert client.get("/api/items").status_code == 404
    assert client.get("/api/items", headers={"x-match": "yes"}).status_code == 200
    assert original_route.calls >= 2


def test_effective_route_context_is_available_in_scope_during_request():
    router = APIRouter()

    @router.get("/items")
    def read_items(request: Request):
        fastapi_scope = request.scope.get("fastapi")
        assert isinstance(fastapi_scope, dict)
        return {
            "has_context": "effective_route_context" in fastapi_scope,
            "path": fastapi_scope["effective_route_context"].path,
        }

    app = FastAPI()
    app.include_router(router, prefix="/api")

    response = TestClient(app).get("/api/items")

    assert response.status_code == 200
    assert response.json() == {"has_context": True, "path": "/api/items"}


def test_original_api_router_matches_is_called_after_inclusion():
    class HeaderRouter(APIRouter):
        calls = 0

        def matches(self, scope):
            self.calls += 1
            headers = dict(scope.get("headers", []))
            if headers.get(b"x-router-match") != b"yes":
                return Match.NONE, {}
            return super().matches(scope)

    router = HeaderRouter()

    @router.get("/items")
    def read_items():
        return []

    app = FastAPI()
    app.include_router(router, prefix="/api")
    client = TestClient(app)

    assert client.get("/api/items").status_code == 404
    assert (
        client.get("/api/items", headers={"x-router-match": "yes"}).status_code == 200
    )
    assert router.calls >= 2


def test_original_nested_api_router_subclasses_are_called_after_inclusion():
    class TrackingRouter(APIRouter):
        calls = 0

        async def handle(self, scope, receive, send):
            self.calls += 1
            await super().handle(scope, receive, send)

    parent_router = TrackingRouter()
    child_router = TrackingRouter()

    @child_router.get("/items")
    def read_items():
        return []

    parent_router.include_router(child_router, prefix="/child")
    app = FastAPI()
    app.include_router(parent_router, prefix="/api")

    response = TestClient(app).get("/api/child/items")

    assert response.status_code == 200
    assert parent_router.calls == 1
    assert child_router.calls == 1


def test_router_and_include_prefix_path_params_reach_endpoint_and_openapi():
    router = APIRouter(prefix="/tenants/{tenant_id}")

    @router.get("/items/{item_id}")
    def read_item(version: int, tenant_id: int, item_id: int):
        return {"version": version, "tenant_id": tenant_id, "item_id": item_id}

    app = FastAPI()
    app.include_router(router, prefix="/api/{version}")

    client = TestClient(app)
    response = client.get("/api/1/tenants/2/items/3")

    assert response.status_code == 200
    assert response.json() == {"version": 1, "tenant_id": 2, "item_id": 3}

    operation = client.get("/openapi.json").json()["paths"][
        "/api/{version}/tenants/{tenant_id}/items/{item_id}"
    ]["get"]
    assert {parameter["name"] for parameter in operation["parameters"]} == {
        "version",
        "tenant_id",
        "item_id",
    }


def test_effective_body_fields_from_app_router_include_and_route_match_openapi():
    def app_body_dependency(app_body: Annotated[str, Body()]):
        return app_body

    def router_body_dependency(router_body: Annotated[int, Body()]):
        return router_body

    def include_body_dependency(include_body: Annotated[bool, Body()]):
        return include_body

    app = FastAPI(dependencies=[Depends(app_body_dependency)])
    router = APIRouter(dependencies=[Depends(router_body_dependency)])

    @router.post("/items")
    def create_item(route_body: Annotated[float, Body()]):
        return {"route_body": route_body}

    app.include_router(
        router,
        prefix="/api",
        dependencies=[Depends(include_body_dependency)],
    )

    client = TestClient(app)
    response = client.post(
        "/api/items",
        json={
            "app_body": "app",
            "router_body": 1,
            "include_body": True,
            "route_body": 2.5,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"route_body": 2.5}

    schema = client.get("/openapi.json").json()
    request_body_schema = schema["paths"]["/api/items"]["post"]["requestBody"][
        "content"
    ]["application/json"]["schema"]
    body_ref = request_body_schema["$ref"].removeprefix("#/components/schemas/")
    body_schema = schema["components"]["schemas"][body_ref]
    assert set(body_schema["required"]) == {
        "app_body",
        "router_body",
        "include_body",
        "route_body",
    }
    assert set(body_schema["properties"]) == {
        "app_body",
        "router_body",
        "include_body",
        "route_body",
    }


def test_later_full_match_wins_over_earlier_included_partial_match():
    get_router = APIRouter()
    post_router = APIRouter()

    @get_router.get("/items")
    def read_items():  # pragma: no cover
        return {"method": "get"}

    @post_router.post("/items")
    def create_item():
        return {"method": "post"}

    app = FastAPI()
    app.include_router(get_router, prefix="/api")
    app.include_router(post_router, prefix="/api")

    response = TestClient(app).post("/api/items")

    assert response.status_code == 200
    assert response.json() == {"method": "post"}


def test_included_partial_match_returns_405_when_no_later_full_match_exists():
    router = APIRouter()

    @router.get("/items")
    def read_items():  # pragma: no cover
        return []

    app = FastAPI()
    app.include_router(router, prefix="/api")

    response = TestClient(app).post("/api/items")

    assert response.status_code == 405
    assert response.headers["allow"] == "GET"


def test_included_slash_redirect_does_not_block_later_exact_match():
    redirect_router = APIRouter()
    exact_router = APIRouter()

    @redirect_router.get("/items/")
    def read_items_with_slash():  # pragma: no cover
        return {"path": "slash"}

    @exact_router.get("/items")
    def read_items_without_slash():
        return {"path": "exact"}

    app = FastAPI()
    app.include_router(redirect_router, prefix="/api")
    app.include_router(exact_router, prefix="/api")

    response = TestClient(app).get("/api/items", follow_redirects=False)

    assert response.status_code == 200
    assert response.json() == {"path": "exact"}


def test_failed_included_match_does_not_leak_effective_context_to_later_route():
    class RejectingRoute(APIRoute):
        def matches(self, scope):
            return Match.NONE, {}

    rejecting_router = APIRouter(route_class=RejectingRoute)
    fallback_router = APIRouter()

    @rejecting_router.get("/items")
    def rejected_item():  # pragma: no cover
        return {"source": "rejected"}

    @fallback_router.get("/items")
    def fallback_item(request: Request):
        fastapi_scope = request.scope.get("fastapi", {})
        context = fastapi_scope.get("effective_route_context")
        return {
            "source": "fallback",
            "context_path": getattr(context, "path", None),
        }

    app = FastAPI()
    app.include_router(rejecting_router, prefix="/api")
    app.include_router(fallback_router, prefix="/api")

    response = TestClient(app).get("/api/items")

    assert response.status_code == 200
    assert response.json() == {"source": "fallback", "context_path": "/api/items"}


def test_included_starlette_mount_keeps_prefix_runtime_and_url_path_for():
    def mounted_endpoint(request):
        return PlainTextResponse("mounted")

    router = APIRouter(
        routes=[
            Mount(
                "/mounted",
                routes=[Route("/items/{item_id}", mounted_endpoint, name="read_item")],
                name="mounted",
            )
        ]
    )
    app = FastAPI()
    app.include_router(router, prefix="/api")

    client = TestClient(app)
    response = client.get("/api/mounted/items/abc")

    assert response.status_code == 200
    assert response.text == "mounted"
    assert (
        app.url_path_for("mounted:read_item", item_id="abc") == "/api/mounted/items/abc"
    )


def test_included_starlette_host_keeps_prefix_runtime_and_url_path_for():
    def hosted_endpoint(request):
        return PlainTextResponse("hosted")

    hosted_app = Router(
        routes=[Route("/items/{item_id}", hosted_endpoint, name="read_item")]
    )
    router = APIRouter(
        routes=[Host("{subdomain}.example.com", hosted_app, name="hosted")]
    )
    app = FastAPI()
    app.include_router(router, prefix="/api")

    client = TestClient(app, base_url="http://api.example.com")
    response = client.get("/api/items/abc")

    assert response.status_code == 200
    assert response.text == "hosted"
    url = app.url_path_for("hosted:read_item", subdomain="api", item_id="abc")
    assert str(url) == "/api/items/abc"
    assert url.host == "api.example.com"


def test_restore_fastapi_scope_key_ignores_non_dict_fastapi_scope():
    scope = {"fastapi": "not-a-dict"}

    _restore_fastapi_scope_key(scope, "effective_route_context", object())

    assert scope == {"fastapi": "not-a-dict"}


@pytest.mark.anyio
async def test_included_api_route_without_app_scope_returns_405_response():
    router = APIRouter()

    @router.get("/items")
    def read_items():  # pragma: no cover
        return {"items": []}

    app = FastAPI()
    app.include_router(router, prefix="/api")
    included_router = cast(_IncludedRouter, app.router.routes[-1])
    effective_context = next(included_router.effective_route_contexts())
    route = effective_context.original_route
    messages = []

    async def receive():  # pragma: no cover
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": "/api/items",
        "raw_path": b"/api/items",
        "root_path": "",
        "scheme": "http",
        "query_string": b"",
        "headers": [],
        "fastapi": {"effective_route_context": effective_context},
    }

    await route.handle(scope, receive, send)

    assert messages[0]["type"] == "http.response.start"
    assert messages[0]["status"] == 405
    assert dict(messages[0]["headers"])[b"allow"] == b"GET"


def test_effective_api_route_context_does_not_match_websocket_scope():
    router = APIRouter()

    @router.get("/items")
    def read_items():  # pragma: no cover
        return {"items": []}

    app = FastAPI()
    app.include_router(router, prefix="/api")
    included_router = cast(_IncludedRouter, app.router.routes[-1])
    effective_context = next(included_router.effective_route_contexts())

    match, child_scope = effective_context.matches(
        {
            "type": "websocket",
            "path": "/api/items",
            "root_path": "",
        }
    )

    assert match == Match.NONE
    assert child_scope == {}


def test_effective_api_route_context_url_path_for_no_match():
    router = APIRouter()

    @router.get("/items/{item_id}")
    def read_item(item_id: str):  # pragma: no cover
        return {"item_id": item_id}

    app = FastAPI()
    app.include_router(router, prefix="/api")
    included_router = cast(_IncludedRouter, app.router.routes[-1])
    effective_context = next(included_router.effective_route_contexts())

    with pytest.raises(NoMatchFound):
        effective_context.url_path_for("missing", item_id="abc")

    with pytest.raises(NoMatchFound):
        included_router.url_path_for("missing", item_id="abc")


def test_included_starlette_host_without_prefix_keeps_original_app():
    def hosted_endpoint(request):
        return PlainTextResponse("hosted")

    hosted_app = Router(
        routes=[Route("/items/{item_id}", hosted_endpoint, name="read_item")]
    )
    router = APIRouter(
        routes=[Host("{subdomain}.example.com", hosted_app, name="hosted")]
    )
    app = FastAPI()
    app.include_router(router)

    client = TestClient(app, base_url="http://api.example.com")
    response = client.get("/items/abc")

    assert response.status_code == 200
    assert response.text == "hosted"


class UnknownRoute(BaseRoute):
    def matches(self, scope):  # pragma: no cover
        return Match.NONE, {}

    async def handle(self, scope, receive, send):  # pragma: no cover
        raise AssertionError("UnknownRoute should not be handled")

    def url_path_for(self, name, /, **path_params):  # pragma: no cover
        raise NoMatchFound(name, path_params)


@pytest.mark.anyio
async def test_included_unknown_route_is_ignored_and_can_return_default_404():
    router = APIRouter(routes=[UnknownRoute()])
    app = FastAPI()
    app.include_router(router, prefix="/api")
    included_router = cast(_IncludedRouter, app.router.routes[-1])

    assert included_router.effective_candidates() == []

    messages = []

    async def receive():  # pragma: no cover
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        messages.append(message)

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/api/missing",
        "raw_path": b"/api/missing",
        "root_path": "",
        "scheme": "http",
        "query_string": b"",
        "headers": [],
        "fastapi": {},
    }

    await included_router._handle_selected(scope, receive, send)

    assert messages[0]["type"] == "http.response.start"
    assert messages[0]["status"] == 404


def test_no_prefix_include_validation_sees_effective_starlette_route_candidates():
    def endpoint(request):  # pragma: no cover
        return PlainTextResponse("ok")

    child_router = APIRouter(routes=[Route("/items", endpoint, name="read_items")])
    parent_router = APIRouter()
    parent_router.include_router(child_router, prefix="/child")

    candidates = list(_iter_included_route_candidates(parent_router.routes))

    assert cast(Route, candidates[0]).path == "/child/items"


def test_no_prefix_include_validation_sees_effective_api_route_path():
    leaf_router = APIRouter()

    @leaf_router.get("")
    def read_items():
        return []

    parent_router = APIRouter()
    parent_router.include_router(leaf_router, prefix="/items")

    # for coverage
    candidates = list(_iter_included_route_candidates(parent_router.routes))
    assert cast(APIRoute, candidates[0]).path == ""

    app = FastAPI()
    app.include_router(parent_router)
    client = TestClient(app)

    response = client.get("/items")

    assert response.status_code == 200, response.text
    assert response.json() == []


def test_no_prefix_include_validation_sees_effective_starlette_route_path():
    def endpoint(request):
        return PlainTextResponse("ok")

    child_router = APIRouter(routes=[Route("/items", endpoint, name="read_items")])
    parent_router = APIRouter()
    parent_router.include_router(child_router, prefix="/child")

    app = FastAPI()
    app.include_router(parent_router)
    client = TestClient(app)

    response = client.get("/child/items")

    assert response.status_code == 200, response.text
    assert response.text == "ok"


def test_no_prefix_include_validation_rejects_empty_effective_api_route_path():
    router = APIRouter()

    @router.get("")
    def read_items():  # pragma: no cover
        return []

    app = FastAPI()
    with pytest.raises(FastAPIError):
        app.include_router(router)


def test_apirouter_matches_fallback_without_include_context():
    router = APIRouter()

    def read_items(request):  # pragma: no cover
        return PlainTextResponse("items")

    router.add_route("/items", read_items)

    assert router.matches({"type": "http", "path": "/items", "root_path": ""}) == (
        Match.NONE,
        {},
    )


@pytest.mark.anyio
async def test_apirouter_handle_fallback_without_include_context():
    router = APIRouter()

    def read_items(request):
        return PlainTextResponse("items")

    router.add_route("/items", read_items)
    messages = []

    async def receive():  # pragma: no cover
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        messages.append(message)

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/items",
        "raw_path": b"/items",
        "root_path": "",
        "scheme": "http",
        "query_string": b"",
        "headers": [],
    }

    await router.handle(scope, receive, send)

    assert messages[0]["type"] == "http.response.start"
    assert messages[0]["status"] == 200
    assert messages[1]["body"] == b"items"
