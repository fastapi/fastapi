"""
Routing compatibility facade.

Public imports remain stable from `fastapi.routing` while implementations are
split across internal modules:
- `fastapi.routing_router`
- `fastapi.routing_routes`
- `fastapi.routing_handlers`
- `fastapi.routing_utils`
"""

from starlette.routing import Mount as Mount

from fastapi.routing_handlers import (
    RouteHandlerConfig as RouteHandlerConfig,
)
from fastapi.routing_handlers import get_request_handler as get_request_handler
from fastapi.routing_handlers import get_websocket_app as get_websocket_app
from fastapi.routing_router import APIRouter as APIRouter
from fastapi.routing_routes import APIRoute as APIRoute
from fastapi.routing_routes import APIWebSocketRoute as APIWebSocketRoute
from fastapi.routing_utils import _DefaultLifespan as _DefaultLifespan
from fastapi.routing_utils import _merge_lifespan_context as _merge_lifespan_context
from fastapi.routing_utils import _wrap_gen_lifespan_context as _wrap_gen_lifespan_context
from fastapi.routing_utils import build_response_args as _build_response_args
from fastapi.routing_utils import extract_endpoint_context as _extract_endpoint_context
from fastapi.routing_utils import request_response as request_response
from fastapi.routing_utils import run_endpoint_function as run_endpoint_function
from fastapi.routing_utils import serialize_response as serialize_response
from fastapi.routing_utils import websocket_session as websocket_session
from fastapi.sse import _PING_INTERVAL as _PING_INTERVAL
from fastapi.sse import KEEPALIVE_COMMENT as KEEPALIVE_COMMENT
from fastapi.sse import EventSourceResponse as EventSourceResponse
from fastapi.sse import ServerSentEvent as ServerSentEvent
from fastapi.sse import format_sse_event as format_sse_event

__all__ = [
    "Mount",
    "APIRouter",
    "APIRoute",
    "APIWebSocketRoute",
    "RouteHandlerConfig",
    "get_request_handler",
    "get_websocket_app",
    "request_response",
    "websocket_session",
    "serialize_response",
    "run_endpoint_function",
    "_DefaultLifespan",
    "_wrap_gen_lifespan_context",
    "_merge_lifespan_context",
    "_extract_endpoint_context",
    "_build_response_args",
    "_PING_INTERVAL",
    "KEEPALIVE_COMMENT",
    "EventSourceResponse",
    "ServerSentEvent",
    "format_sse_event",
]
