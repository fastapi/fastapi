from collections.abc import Sequence
from typing import Any

from fastapi import routing
from fastapi.encoders import jsonable_encoder
from starlette.routing import BaseRoute


def get_asyncapi_channel(
    *,
    route: routing.APIWebSocketRoute,
) -> dict[str, Any]:
    """Generate AsyncAPI channel definition for a WebSocket route."""
    channel: dict[str, Any] = {}

    # WebSocket channels typically have subscribe operation
    # (client subscribes to receive messages from server)
    operation: dict[str, Any] = {
        "operationId": route.name or f"websocket_{route.path_format}",
    }

    # Basic message schema - can be enhanced later with actual message types
    # For WebSockets, messages can be sent in both directions
    message: dict[str, Any] = {
        "contentType": "application/json",
    }

    operation["message"] = message
    channel["subscribe"] = operation

    # WebSockets are bidirectional, so we also include publish
    # (client can publish messages to server)
    publish_operation: dict[str, Any] = {
        "operationId": f"{route.name or f'websocket_{route.path_format}'}_publish",
        "message": message,
    }
    channel["publish"] = publish_operation

    return channel


def get_asyncapi(
    *,
    title: str,
    version: str,
    asyncapi_version: str = "2.6.0",
    summary: str | None = None,
    description: str | None = None,
    routes: Sequence[BaseRoute],
    servers: list[dict[str, str | Any]] | None = None,
    terms_of_service: str | None = None,
    contact: dict[str, str | Any] | None = None,
    license_info: dict[str, str | Any] | None = None,
    external_docs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Generate AsyncAPI schema from FastAPI application routes.

    Filters for WebSocket routes and generates AsyncAPI 2.6.0 compliant schema.
    """
    info: dict[str, Any] = {"title": title, "version": version}
    if summary:
        info["summary"] = summary
    if description:
        info["description"] = description
    if terms_of_service:
        info["termsOfService"] = terms_of_service
    if contact:
        info["contact"] = contact
    if license_info:
        info["license"] = license_info

    output: dict[str, Any] = {"asyncapi": asyncapi_version, "info": info}

    # Add default WebSocket server if no servers provided and we have WebSocket routes
    websocket_routes = [
        route for route in routes or [] if isinstance(route, routing.APIWebSocketRoute)
    ]
    if websocket_routes and not servers:
        # Default WebSocket server - can be overridden by providing servers parameter
        output["servers"] = [
            {
                "url": "ws://localhost:8000",
                "protocol": "ws",
                "description": "WebSocket server",
            }
        ]
    elif servers:
        output["servers"] = servers

    channels: dict[str, dict[str, Any]] = {}

    # Filter routes to only include WebSocket routes
    for route in routes or []:
        if isinstance(route, routing.APIWebSocketRoute):
            channel = get_asyncapi_channel(route=route)
            if channel:
                channels[route.path_format] = channel

    output["channels"] = channels

    if external_docs:
        output["externalDocs"] = external_docs

    return jsonable_encoder(output, by_alias=True, exclude_none=True)

