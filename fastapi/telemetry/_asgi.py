import os
from contextlib import nullcontext
from time import perf_counter, time_ns
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit

from fastapi import __version__
from fastapi.telemetry._api import (
    _HTTP_METHODS,
    _REQUEST_TELEMETRY_KEY,
    TelemetryConfig,
    _exception_type,
    _normal_websocket_disconnect,
    _RequestTelemetry,
    _unconfigured,
)
from opentelemetry import _logs, metrics, propagate, trace
from opentelemetry import context as otel_context
from opentelemetry._logs import SeverityNumber
from opentelemetry.metrics import Histogram, UpDownCounter
from opentelemetry.propagators.textmap import Getter
from opentelemetry.trace import SpanKind, StatusCode
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send

_DURATION_BUCKETS = (
    0.005,
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.25,
    0.5,
    0.75,
    1.0,
    2.5,
    5.0,
    7.5,
    10.0,
)
_SCHEMA_URL = "https://opentelemetry.io/schemas/1.44.0"
# https://opentelemetry.io/docs/specs/semconv/http/http-spans/#http-server-span
_SENSITIVE_QUERY_PARAMETERS = frozenset(
    {
        "X-Amz-Signature",
        "X-Amz-Credential",
        "X-Amz-Security-Token",
        "sig",
        "X-Goog-Signature",
    }
)


class _HeadersGetter(Getter[Headers]):
    def get(self, carrier: Headers, key: str) -> list[str] | None:
        values = carrier.getlist(key)
        if not values:
            return None
        if key.lower() == "baggage":
            # The baggage propagator reads only the first value.
            return [",".join(values)]
        return values

    def keys(self, carrier: Headers) -> list[str]:
        return carrier.keys()


_HEADERS_GETTER = _HeadersGetter()


def _legacy_otel(stack: Any) -> bool:
    # Test the built stack, not contrib's flag: that flag also exists when its
    # stack patch failed, or when instrument_app was called after stack creation.
    seen: set[int] = set()
    while stack is not None and id(stack) not in seen:
        seen.add(id(stack))
        if (
            type(stack).__module__ == "opentelemetry.instrumentation.asgi"
            and type(stack).__name__ == "OpenTelemetryMiddleware"
        ):
            return True
        stack = getattr(stack, "app", None)
    return False


def _exception(*, scope: Scope, exc: BaseException) -> None:
    if scope["type"] == "websocket" and _normal_websocket_disconnect(exc):
        return
    request_telemetry = scope.get("fastapi.telemetry")
    if isinstance(request_telemetry, _RequestTelemetry):
        seen = request_telemetry._exceptions
        if not any(previous is exc for previous in seen):
            seen.append(exc)
            if request_telemetry.logger is not None and isinstance(exc, Exception):
                attributes = (
                    {"http.route": request_telemetry.route}
                    if request_telemetry.route
                    else None
                )
                request_telemetry.logger.emit(
                    exception=exc,
                    event_name="fastapi.websocket.exception"
                    if scope["type"] == "websocket"
                    else "http.server.request.exception",
                    timestamp=time_ns(),
                    severity_number=SeverityNumber.ERROR,
                    severity_text="ERROR",
                    body="Unhandled exception in FastAPI WebSocket connection"
                    if scope["type"] == "websocket"
                    else "Unhandled exception in FastAPI request",
                    attributes=attributes,
                )


def _server_attributes(scope: Scope) -> dict[str, Any]:
    # ASGI exposes HTTP/2 and HTTP/3 authority as Host. Proxy normalization is
    # handled by the server or middleware, as it is for the request URL.
    authority = Headers(scope=scope).get("host")
    if authority is not None:
        try:
            url = urlsplit("//" + authority)
            address, port = url.hostname, url.port
        except ValueError:
            # Malformed authority must not prevent handling the request.
            return {}
        if url.username is not None or url.path or url.query or url.fragment:
            return {}
        if port is None:
            port = {"http": 80, "https": 443, "ws": 80, "wss": 443}.get(
                scope.get("scheme", "http")
            )
    else:
        address, port = scope.get("server") or (None, None)
    if address is None:
        return {}
    attributes: dict[str, Any] = {"server.address": address}
    if port is not None:
        attributes["server.port"] = port
    return attributes


class ExceptionTelemetryMiddleware:
    """Observe exceptions before error handlers send and complete a response."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            _exception(scope=scope, exc=exc)
            raise


class NativeTelemetry:
    def __init__(self, config: TelemetryConfig) -> None:
        self.config = config
        known_methods = os.getenv("OTEL_INSTRUMENTATION_HTTP_KNOWN_METHODS", "").strip()
        self._known_methods = (
            frozenset(
                method.strip() for method in known_methods.split(",") if method.strip()
            )
            if known_methods
            else _HTTP_METHODS
        )
        self._provider: metrics.MeterProvider | None = None
        self._duration: Histogram | None = None
        self._active: UpDownCounter | None = None

    def enabled(self) -> bool:
        config = self.config
        return bool(
            (
                config["tracing"]
                and (
                    config["tracer_provider"] is not None
                    or not _unconfigured(trace.get_tracer_provider())
                )
            )
            or (
                config["metrics"]
                and (
                    config["meter_provider"] is not None
                    or not _unconfigured(metrics.get_meter_provider())
                )
            )
            or (
                config["logs"]
                and (
                    config["logger_provider"] is not None
                    or not _unconfigured(_logs.get_logger_provider())
                )
            )
        )

    def _instruments(self) -> tuple[Histogram, UpDownCounter]:
        provider = self.config["meter_provider"] or metrics.get_meter_provider()
        if provider is not self._provider:
            meter = provider.get_meter("fastapi", __version__, schema_url=_SCHEMA_URL)
            self._duration = meter.create_histogram(
                "http.server.request.duration",
                unit="s",
                description="Duration of HTTP server requests.",
                explicit_bucket_boundaries_advisory=_DURATION_BUCKETS,
            )
            self._active = meter.create_up_down_counter(
                "http.server.active_requests",
                unit="{request}",
                description="Number of active HTTP server requests.",
            )
            self._provider = provider
        assert self._duration is not None and self._active is not None
        return self._duration, self._active

    async def __call__(
        self,
        *,
        app: ASGIApp,
        scope: Scope,
        receive: Receive,
        send: Send,
        legacy_otel: bool = False,
    ) -> None:
        config = self.config
        if config["exclude"] is not None and config["exclude"](scope):
            # Keep mounted FastAPI apps from observing this excluded request.
            scope["fastapi.telemetry"] = None
            try:
                await app(scope, receive, send)
            finally:
                scope.pop("fastapi.telemetry", None)
            return
        tracing = config["tracing"] and not legacy_otel
        logging = config["logs"] and not legacy_otel
        if logging:
            logger_provider = config["logger_provider"] or _logs.get_logger_provider()
            logging = not (
                (config["logger_provider"] is None and _unconfigured(logger_provider))
                or isinstance(logger_provider, _logs.NoOpLoggerProvider)
            )
        is_websocket = scope["type"] == "websocket"
        metering = config["metrics"] and not legacy_otel and not is_websocket
        if tracing:
            provider = config["tracer_provider"] or trace.get_tracer_provider()
            tracing = not (
                (config["tracer_provider"] is None and _unconfigured(provider))
                or isinstance(provider, trace.NoOpTracerProvider)
            )
        if metering:
            meter_provider = config["meter_provider"] or metrics.get_meter_provider()
            metering = not (
                (config["meter_provider"] is None and _unconfigured(meter_provider))
                or isinstance(meter_provider, metrics.NoOpMeterProvider)
            )
        if not tracing and not metering and not logging:
            await app(scope, receive, send)
            return
        original_method = scope.get("method", "")
        method = original_method if original_method in self._known_methods else "_OTHER"
        span_method = "WS" if is_websocket else "HTTP" if method == "_OTHER" else method
        attributes: dict[str, Any] = {
            "url.scheme": scope.get("scheme", "ws" if is_websocket else "http"),
        }
        if is_websocket:
            attributes["network.protocol.name"] = "websocket"
        else:
            attributes["http.request.method"] = method
            if scope.get("http_version"):
                attributes["network.protocol.version"] = scope["http_version"]
        duration, active = self._instruments() if metering else (None, None)
        active_attributes = {
            k: v for k, v in attributes.items() if k != "network.protocol.version"
        }
        if active is not None:
            active.add(1, active_attributes)
        started = perf_counter()
        span = None
        tracer = None
        parent_token = None
        if tracing:
            parent = propagate.extract(Headers(scope=scope), getter=_HEADERS_GETTER)
            parent_token = otel_context.attach(parent)
            tracer = trace.get_tracer(
                "fastapi",
                __version__,
                config["tracer_provider"],
                schema_url=_SCHEMA_URL,
            )
            span_attributes = {**attributes, **_server_attributes(scope)}
            if not is_websocket:
                span_attributes["url.path"] = scope["path"]
                if scope.get("query_string"):
                    span_attributes["url.query"] = urlencode(
                        [
                            (
                                key,
                                "REDACTED"
                                if key in _SENSITIVE_QUERY_PARAMETERS
                                else value,
                            )
                            for key, value in parse_qsl(
                                scope["query_string"].decode("latin-1"),
                                keep_blank_values=True,
                            )
                        ]
                    )
                if original_method != method:
                    span_attributes["http.request.method_original"] = original_method
            span = tracer.start_span(
                span_method,
                context=parent,
                kind=SpanKind.SERVER,
                attributes=span_attributes,
            )
        request_telemetry = _RequestTelemetry(
            span=span,
            span_method=span_method,
            tracer=tracer if config["operation_spans"] else None,
            logger=_logs.get_logger(
                "fastapi",
                __version__,
                config["logger_provider"],
                schema_url=_SCHEMA_URL,
            )
            if logging
            else None,
            _mount_prefix=scope.get("app_root_path", scope.get("root_path", "")).rstrip(
                "/"
            ),
        )
        scope["fastapi.telemetry"] = request_telemetry
        token = otel_context.attach(
            otel_context.set_value(_REQUEST_TELEMETRY_KEY, request_telemetry)
        )
        finished = False
        trailers = False
        disconnected = False

        def finish(error: BaseException | None = None) -> None:
            nonlocal finished
            if finished:
                return
            finished = True
            if request_telemetry.route is not None:
                attributes["http.route"] = request_telemetry.route
            if request_telemetry.status_code is not None:
                attributes["http.response.status_code"] = request_telemetry.status_code
            failed = (
                error is not None
                or not is_websocket
                and (
                    request_telemetry.status_code is None
                    or request_telemetry.status_code >= 500
                )
            )
            if failed:
                errors = request_telemetry._exceptions
                failure = error or (errors[-1] if errors else None)
                attributes["error.type"] = (
                    _exception_type(failure)
                    if failure
                    else str(request_telemetry.status_code or "incomplete_response")
                )
            if span is not None:
                span.set_attributes(attributes)
                if failed:
                    span.set_status(StatusCode.ERROR)
            # Record while the span is current, so exemplars can correlate it.
            if duration is not None:
                duration.record(max(0, perf_counter() - started), attributes)
            if active is not None:
                active.add(-1, active_attributes)
            if span is not None:
                span.end()

        async def wrapped_send(message: Message) -> None:
            nonlocal trailers
            if message["type"] == "http.response.start":
                request_telemetry.status_code = message["status"]
                trailers = message.get("trailers", False)
            await send(message)
            if (
                (
                    message["type"] == "http.response.body"
                    and not message.get("more_body", False)
                    and not trailers
                )
                or (
                    message["type"] == "http.response.trailers"
                    and not message.get("more_trailers", False)
                )
                or message["type"] == "http.response.pathsend"
            ):
                finish()

        async def wrapped_receive() -> Message:
            nonlocal disconnected
            message = await receive()
            if message["type"] == "http.disconnect":
                disconnected = True
            return message

        context = (
            trace.use_span(
                span,
                end_on_exit=False,
                record_exception=False,
                set_status_on_exception=False,
            )
            if span is not None
            else nullcontext()
        )
        try:
            with context:
                try:
                    await app(
                        scope,
                        receive if is_websocket else wrapped_receive,
                        send if is_websocket else wrapped_send,
                    )
                except BaseException as exc:
                    _exception(scope=scope, exc=exc)
                    finish(
                        None
                        if is_websocket and _normal_websocket_disconnect(exc)
                        else exc
                    )
                    raise
                finally:
                    if not finished:
                        finish(
                            None
                            if is_websocket
                            else ConnectionError("Client disconnected")
                            if disconnected
                            else RuntimeError("Incomplete ASGI response")
                        )
        finally:
            request_telemetry.data = None
            request_telemetry._exceptions.clear()
            otel_context.detach(token)
            scope.pop("fastapi.telemetry", None)
            if parent_token is not None:
                otel_context.detach(parent_token)
