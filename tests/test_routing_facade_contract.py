from enum import IntEnum

import fastapi.routing as routing
from fastapi.dependencies.utils import get_dependant
from fastapi.routing_handlers import RouteHandlerConfig, get_request_handler
from fastapi.routing_router import APIRouter
from fastapi.routing_routes import APIRoute, APIWebSocketRoute
from fastapi.routing_utils import request_response, websocket_session
from starlette.requests import Request
from starlette.responses import Response
from starlette.testclient import TestClient


def test_routing_facade_exports_expected_symbols() -> None:
    expected = {
        "APIRouter",
        "APIRoute",
        "APIWebSocketRoute",
        "RouteHandlerConfig",
        "get_request_handler",
        "get_websocket_app",
        "request_response",
        "websocket_session",
        "_PING_INTERVAL",
    }
    assert expected.issubset(set(routing.__all__))


def test_routing_facade_re_exports_router_classes() -> None:
    assert routing.APIRouter is APIRouter
    assert routing.APIRoute is APIRoute
    assert routing.APIWebSocketRoute is APIWebSocketRoute


def test_routing_facade_re_exports_handler_contracts() -> None:
    assert routing.RouteHandlerConfig is RouteHandlerConfig
    assert routing.request_response is request_response
    assert routing.websocket_session is websocket_session


def test_routing_ping_constant_compatibility() -> None:
    assert isinstance(routing._PING_INTERVAL, (float, int))


class _CreatedStatus(IntEnum):
    CREATED = 201


def _raw_response_endpoint() -> Response:
    return Response(content="ok")


def test_api_route_defaults_and_intenum_status_paths() -> None:
    raw = _raw_response_endpoint()
    assert raw.body == b"ok"

    route = routing.APIRoute(
        "/raw-response",
        _raw_response_endpoint,
        status_code=_CreatedStatus.CREATED,
    )
    assert route.response_model is None
    assert route.status_code == 201
    assert route.methods == {"GET"}


def test_get_request_handler_supports_legacy_dependant_signature() -> None:
    dependant = get_dependant(path="/legacy", call=_raw_response_endpoint)
    handler = get_request_handler(dependant)
    assert callable(handler)


def test_request_response_wraps_sync_callable() -> None:
    def endpoint(_: Request) -> Response:
        return Response("sync-ok")

    app = request_response(endpoint)
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "sync-ok"


def test_request_response_wraps_async_callable() -> None:
    async def endpoint(_: Request) -> Response:
        return Response("async-ok")

    app = request_response(endpoint)
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "async-ok"
