import fastapi.routing as routing
from fastapi.routing_handlers import RouteHandlerConfig
from fastapi.routing_router import APIRouter
from fastapi.routing_routes import APIRoute, APIWebSocketRoute
from fastapi.routing_utils import request_response, websocket_session


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
