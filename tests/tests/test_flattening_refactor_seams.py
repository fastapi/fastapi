from fastapi import Depends, FastAPI, Header, Security
from fastapi.security import SecurityScopes


def test_shared_body_dependency_across_websocket_route_embeds_correctly():
    """WebSocket routes go through the same _build_dependant_with_
    parameterless_dependencies -> _get_flat_body_params path as HTTP
    routes. A body-declaring dependency referenced more than once should
    still resolve to a single embed decision, matching HTTP route
    behavior, rather than the websocket path silently diverging."""
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str

    def get_item(item: Item) -> Item:
        return item

    app = FastAPI()

    @app.websocket("/ws")
    async def endpoint(
        websocket,
        first: Item = Depends(get_item),
        second: Item = Depends(get_item),
    ):
        pass

    route = app.routes[-1]
    # Only one distinct top-level body field should be embedded, even
    # though the dependency is referenced twice.
    assert route._embed_body_fields is False


def test_same_dependency_different_scopes_yields_single_openapi_param():
    """The same dependency, used twice via Security() with different
    required scopes, produces two distinct cache entries internally
    (scope-aware cache key), but must still resolve to a single
    parameter in the final OpenAPI schema -- the underlying HTTP header
    is the same regardless of which scopes are being checked."""
    from fastapi.dependencies.utils import get_flat_params

    def get_user(security_scopes: SecurityScopes, x_token: str = Header()):
        return {"scopes": security_scopes.scopes, "token": x_token}

    app = FastAPI()

    @app.get("/test")
    def endpoint(
        reader=Security(get_user, scopes=["read"]),
        writer=Security(get_user, scopes=["write"]),
    ):
        return {"reader": reader, "writer": writer}

    schema = app.openapi()
    op_params = schema["paths"]["/test"]["get"].get("parameters", [])
    param_names = [p["name"] for p in op_params]

    assert param_names.count("x-token") == 1, (
        f"expected x-token to appear exactly once in the OpenAPI schema "
        f"regardless of how many differently-scoped Security() uses "
        f"share the dependency, got: {param_names}"
    )
