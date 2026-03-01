from collections.abc import Sequence
from typing import Any

from fastapi import routing
from fastapi.asyncapi.constants import ASYNCAPI_VERSION, REF_PREFIX
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.routing import BaseRoute


def get_asyncapi_channel(
    *,
    route: routing.APIWebSocketRoute,
    subscribe_payload_schema: dict[str, Any] | None = None,
    publish_payload_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate AsyncAPI channel definition for a WebSocket route."""
    channel: dict[str, Any] = {}

    # WebSocket channels typically have subscribe operation
    # (client subscribes to receive messages from server)
    operation: dict[str, Any] = {
        "operationId": route.name or f"websocket_{route.path_format}",
    }

    # Message schema: contentType and optional payload (schema for message body)
    subscribe_message: dict[str, Any] = {
        "contentType": "application/json",
    }
    if subscribe_payload_schema:
        subscribe_message["payload"] = subscribe_payload_schema

    operation["message"] = subscribe_message
    channel["subscribe"] = operation

    # WebSockets are bidirectional, so we also include publish
    # (client can publish messages to server)
    publish_operation: dict[str, Any] = {
        "operationId": f"{route.name or f'websocket_{route.path_format}'}_publish",
        "message": {
            "contentType": "application/json",
            **({"payload": publish_payload_schema} if publish_payload_schema else {}),
        },
    }
    channel["publish"] = publish_operation

    return channel


def _get_fields_from_websocket_routes(
    routes: Sequence[BaseRoute],
) -> list[Any]:
    """Collect body (ModelField) params from WebSocket routes for schema generation."""
    from fastapi._compat import ModelField
    from fastapi.dependencies.utils import get_flat_dependant
    from pydantic.fields import FieldInfo

    fields: list[Any] = []
    seen_models: set[type[BaseModel]] = set()
    for route in routes or []:
        if not isinstance(route, routing.APIWebSocketRoute):
            continue
        flat_dependant = get_flat_dependant(route.dependant, skip_repeats=True)
        fields.extend(flat_dependant.body_params)
        # Add explicit subscribe_schema / publish_schema as ModelFields so they get definitions
        for model in (
            getattr(route, "subscribe_schema", None),
            getattr(route, "publish_schema", None),
        ):
            if (
                model is not None
                and isinstance(model, type)
                and issubclass(model, BaseModel)
                and model not in seen_models
            ):
                seen_models.add(model)
                fields.append(
                    ModelField(
                        field_info=FieldInfo(annotation=model),
                        name=model.__name__,
                        mode="validation",
                    )
                )
    return fields


def get_asyncapi(
    *,
    title: str,
    version: str,
    asyncapi_version: str = ASYNCAPI_VERSION,
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
    Includes components/schemas for message payloads when WebSocket routes use
    Pydantic models (e.g. via Body() in dependencies).
    """
    from fastapi._compat import (
        ModelField,
        get_definitions,
        get_flat_models_from_fields,
        get_model_name_map,
        get_schema_from_model_field,
    )

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

    # Build components/schemas from WebSocket body params and explicit subscribe/publish_schema
    ws_fields = _get_fields_from_websocket_routes(routes or [])
    components: dict[str, Any] = {}
    route_subscribe_schemas: dict[str, dict[str, Any] | None] = {}
    route_publish_schemas: dict[str, dict[str, Any] | None] = {}
    if ws_fields:
        flat_models = get_flat_models_from_fields(ws_fields, known_models=set())
        model_name_map = get_model_name_map(flat_models)
        field_mapping, definitions = get_definitions(
            fields=ws_fields,
            model_name_map=model_name_map,
            separate_input_output_schemas=True,
        )
        if definitions:
            components["schemas"] = {k: definitions[k] for k in sorted(definitions)}
        # For each WebSocket route, resolve subscribe and publish payload schemas
        for route in routes or []:
            if not isinstance(route, routing.APIWebSocketRoute):
                continue
            sub_schema: dict[str, Any] | None = None
            pub_schema: dict[str, Any] | None = None
            # Explicit subscribe_schema / publish_schema (e.g. when route has no Body() in Depends)
            subscribe_model = getattr(route, "subscribe_schema", None)
            publish_model = getattr(route, "publish_schema", None)
            if (
                subscribe_model is not None
                and isinstance(subscribe_model, type)
                and issubclass(subscribe_model, BaseModel)
            ):
                sub_schema = {"$ref": f"{REF_PREFIX}{subscribe_model.__name__}"}
            if (
                publish_model is not None
                and isinstance(publish_model, type)
                and issubclass(publish_model, BaseModel)
            ):
                pub_schema = {"$ref": f"{REF_PREFIX}{publish_model.__name__}"}
            # Fall back to first body param (Depends with Body()) for both if not set
            if sub_schema is None or pub_schema is None:
                flat_dependant = route._flat_dependant
                if flat_dependant.body_params:
                    first_body = flat_dependant.body_params[0]
                    if isinstance(first_body, ModelField):
                        body_schema = get_schema_from_model_field(
                            field=first_body,
                            model_name_map=model_name_map,
                            field_mapping=field_mapping,
                            separate_input_output_schemas=True,
                        )
                        # Use only $ref for channel payload when schema is in components
                        if "$ref" in body_schema and body_schema["$ref"].startswith(
                            REF_PREFIX
                        ):
                            body_schema = {"$ref": body_schema["$ref"]}
                        if sub_schema is None:
                            sub_schema = body_schema
                        if pub_schema is None:
                            pub_schema = body_schema
            route_subscribe_schemas[route.path_format] = sub_schema
            route_publish_schemas[route.path_format] = pub_schema
    else:
        for route in routes or []:
            if not isinstance(route, routing.APIWebSocketRoute):
                continue
            route_subscribe_schemas[route.path_format] = None
            route_publish_schemas[route.path_format] = None

    channels: dict[str, dict[str, Any]] = {}

    # Filter routes to only include WebSocket routes
    for route in routes or []:
        if isinstance(route, routing.APIWebSocketRoute):
            sub_schema = route_subscribe_schemas.get(route.path_format)
            pub_schema = route_publish_schemas.get(route.path_format)
            channel = get_asyncapi_channel(
                route=route,
                subscribe_payload_schema=sub_schema,
                publish_payload_schema=pub_schema,
            )
            if channel:
                channels[route.path_format] = channel

    output["channels"] = channels

    if components:
        output["components"] = components

    if external_docs:
        output["externalDocs"] = external_docs

    return jsonable_encoder(output, by_alias=True, exclude_none=True)  # type: ignore
