from collections.abc import Callable, Iterator, MutableMapping, Sequence
from contextlib import AbstractContextManager, contextmanager, nullcontext
from dataclasses import dataclass, field
from time import time_ns
from typing import Annotated, Any

from annotated_doc import Doc
from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
from opentelemetry import context as otel_context
from opentelemetry._logs import Logger, LoggerProvider, SeverityNumber
from opentelemetry.context import Context
from opentelemetry.metrics import MeterProvider
from opentelemetry.trace import Span, StatusCode, Tracer, TracerProvider
from starlette.exceptions import HTTPException, WebSocketException
from starlette.requests import Request
from starlette.websockets import WebSocket, WebSocketDisconnect
from typing_extensions import TypedDict

_HTTP_METHODS = frozenset(
    {
        "CONNECT",
        "DELETE",
        "GET",
        "HEAD",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
        "QUERY",
        "TRACE",
    }
)


class TelemetryConfig(TypedDict, total=False):
    """Optional settings for `FastAPI(telemetry={...})`.

    Omitted settings keep their defaults. FastAPI preserves existing providers
    and their exporters. Environment setup can add exporters unless `auto_configure`
    is `False`. Providers supplied by the application are never shut down by FastAPI.
    """

    tracer_provider: Annotated[
        TracerProvider | None,
        Doc("Use this provider instead of the global tracer provider."),
    ]
    meter_provider: Annotated[
        MeterProvider | None,
        Doc("Use this provider instead of the global meter provider."),
    ]
    logger_provider: Annotated[
        LoggerProvider | None,
        Doc("Use this provider instead of the global logger provider."),
    ]
    tracing: Annotated[
        bool,
        Doc("Enable HTTP request and WebSocket connection spans. Defaults to `True`."),
    ]
    metrics: Annotated[bool, Doc("Enable HTTP request metrics. Defaults to `True`.")]
    logs: Annotated[
        bool,
        Doc(
            "Record validation failures and unhandled exceptions, including exception messages and stack traces. Defaults to `True`."
        ),
    ]
    operation_spans: Annotated[
        bool,
        Doc(
            "Trace dependency resolution, endpoints, serialization, and background tasks. Defaults to `True`."
        ),
    ]
    auto_configure: Annotated[
        bool,
        Doc("Add OTLP exporters from environment variables. Defaults to `True`."),
    ]
    exclude: Annotated[
        Callable[[MutableMapping[str, Any]], bool] | None,
        Doc(
            "A function that receives the ASGI scope. Return `True` to skip FastAPI telemetry for that request or connection."
        ),
    ]


@dataclass(kw_only=True)
class TelemetryData:
    """Local request or connection data for synchronous OpenTelemetry processors.

    FastAPI populates these fields as it handles the request or connection.
    Integrations should treat the data as read-only and apply their capture and
    redaction settings before exporting any of it.
    """

    request: Annotated[
        Request | None, Doc("The request, available when its route handler starts.")
    ] = None
    websocket: Annotated[
        WebSocket | None,
        Doc("The WebSocket, available when its route handler starts."),
    ] = None
    body: Annotated[
        Any, Doc("The body read by FastAPI, before parameter validation.")
    ] = None
    values: Annotated[
        dict[str, Any] | None,
        Doc("The original parsed arguments, available after dependency resolution."),
    ] = None
    errors: Annotated[
        Sequence[Any] | None,
        Doc("Request validation errors, including the original input values."),
    ] = None


@dataclass(kw_only=True)
class _RequestTelemetry:
    span: Span | None
    span_method: str
    tracer: Tracer | None = None
    logger: Logger | None = None
    route: str | None = None
    status_code: int | None = None
    data: TelemetryData | None = field(default_factory=TelemetryData)
    _mount_prefix: str = ""
    _exceptions: list[BaseException] = field(default_factory=list, repr=False)


_REQUEST_TELEMETRY_KEY = otel_context.create_key("fastapi.request")
_NO_OPERATION = nullcontext()


def _get_request_telemetry(context: Context | None = None) -> _RequestTelemetry | None:
    value = otel_context.get_value(_REQUEST_TELEMETRY_KEY, context)
    return value if isinstance(value, _RequestTelemetry) else None


def get_telemetry_data(context: Context | None = None) -> TelemetryData | None:
    """Read local FastAPI data from an OpenTelemetry context.

    Defaults to the current context. Log processors can pass `record.context`.
    Read the data synchronously while FastAPI handles the request or connection.
    After it finishes, this returns `None`, including for retained contexts.
    This data is not automatically added to exported spans or logs.
    """
    request_telemetry = _get_request_telemetry(context)
    return request_telemetry.data if request_telemetry is not None else None


def _validation_failed(
    exc: RequestValidationError | WebSocketRequestValidationError,
) -> None:
    request_telemetry = _get_request_telemetry()
    if request_telemetry is None:
        return
    if request_telemetry.data is not None:
        if isinstance(exc, RequestValidationError):
            request_telemetry.data.body = exc.body
        request_telemetry.data.errors = exc.errors()
    if request_telemetry.logger is not None:
        attributes: dict[str, Any] = {
            "fastapi.validation.error_count": len(exc.errors())
        }
        if request_telemetry.route is not None:
            attributes["http.route"] = request_telemetry.route
        request_telemetry.logger.emit(
            event_name="fastapi.validation.failed",
            timestamp=time_ns(),
            severity_number=SeverityNumber.WARN,
            severity_text="WARN",
            body="Request validation failed",
            attributes=attributes,
        )


def _exception_type(exc: BaseException) -> str:
    cls = type(exc)
    return (
        f"{cls.__module__}.{cls.__qualname__}"
        if cls.__module__ != "builtins"
        else cls.__qualname__
    )


def _normal_websocket_disconnect(exc: BaseException) -> bool:
    return isinstance(exc, WebSocketDisconnect) and exc.code in (1000, 1001)


def _operation(
    *, name: str, function: Callable[..., Any] | None = None
) -> AbstractContextManager[None]:
    request_telemetry = _get_request_telemetry()
    if request_telemetry is None or request_telemetry.tracer is None:
        return _NO_OPERATION
    return _traced_operation(
        request_telemetry=request_telemetry, name=name, function=function
    )


@contextmanager
def _traced_operation(
    *,
    request_telemetry: _RequestTelemetry,
    name: str,
    function: Callable[..., Any] | None,
) -> Iterator[None]:
    assert request_telemetry.tracer is not None
    attributes = {}
    if function is not None:
        module = getattr(function, "__module__", type(function).__module__)
        qualname = getattr(function, "__qualname__", type(function).__qualname__)
        attributes["code.function.name"] = f"{module}.{qualname}"
    with request_telemetry.tracer.start_as_current_span(
        f"fastapi.{name}",
        attributes=attributes,
        record_exception=False,
        set_status_on_exception=False,
    ) as span:
        try:
            yield
        except Exception as exc:
            if name == "background_task" or (
                not isinstance(
                    exc,
                    (
                        HTTPException,
                        RequestValidationError,
                        WebSocketException,
                        WebSocketRequestValidationError,
                    ),
                )
                and not _normal_websocket_disconnect(exc)
            ):
                span.set_attribute("error.type", _exception_type(exc))
                span.set_status(StatusCode.ERROR)
            raise


def _run_sync_endpoint(
    *, function: Callable[..., Any], arguments: dict[str, Any]
) -> Any:
    with _operation(name="endpoint", function=function):
        return function(**arguments)


def _route_selected(
    *, scope: MutableMapping[str, Any], path: str | None, mount: bool = False
) -> None:
    request_telemetry = scope.get("fastapi.telemetry")
    if not isinstance(request_telemetry, _RequestTelemetry) or path is None:
        return
    # Mount's path_format ends in /{path}. The child contributes its own path.
    if mount:
        path = path.removesuffix("/{path}")
        request_telemetry._mount_prefix += path
        request_telemetry.route = request_telemetry._mount_prefix + "/{path}"
    else:
        request_telemetry.route = request_telemetry._mount_prefix + path
    if request_telemetry.span is not None:
        request_telemetry.span.set_attribute("http.route", request_telemetry.route)
        request_telemetry.span.update_name(
            f"{request_telemetry.span_method} {request_telemetry.route}"
        )


_DEFERRED_PROVIDERS = frozenset(
    {
        ("opentelemetry.trace", "ProxyTracerProvider"),
        ("opentelemetry.metrics._internal", "_ProxyMeterProvider"),
        ("opentelemetry._logs._internal", "ProxyLoggerProvider"),
    }
)


def _unconfigured(provider: Any) -> bool:
    # Python's API has no public "is configured" query. Limit this bridge to its
    # known deferred providers, never SDK implementations or vendor proxies.
    cls = type(provider)
    return (cls.__module__, cls.__name__) in _DEFERRED_PROVIDERS
