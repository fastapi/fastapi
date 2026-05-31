"""
WebSocket support for FastAPI.

Re-exports Starlette's WebSocket classes for use in FastAPI applications,
providing a consistent import path for WebSocket, WebSocketDisconnect, and
WebSocketState.
"""

from starlette.websockets import WebSocket as WebSocket  # noqa
from starlette.websockets import WebSocketDisconnect as WebSocketDisconnect  # noqa
from starlette.websockets import WebSocketState as WebSocketState  # noqa
