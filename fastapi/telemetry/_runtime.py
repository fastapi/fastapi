import atexit
import os
import threading
from collections.abc import Callable
from typing import Any, cast
from urllib.parse import urlsplit

from anyio.to_thread import run_sync
from fastapi.exceptions import FastAPIError
from fastapi.logger import logger
from fastapi.telemetry._api import TelemetryConfig, _unconfigured
from opentelemetry import _logs, metrics, trace
from starlette.types import ASGIApp, Message, Receive, Scope, Send

_lock = threading.RLock()
_owned: list[Any] = []
_configured: list[tuple[str, Any]] = []


def _flush() -> None:
    for component in tuple(_owned):
        try:
            component.force_flush()
        except Exception:
            logger.exception("FastAPI telemetry cleanup failed")


def _shutdown() -> None:
    with _lock:
        owned = tuple(_owned)
        _owned.clear()
    for component in owned:
        try:
            component.shutdown()
        except Exception:
            logger.exception("FastAPI telemetry cleanup failed")


atexit.register(_shutdown)


def _export_endpoint(signal: str) -> str | None:
    exporter = (os.getenv(f"OTEL_{signal}_EXPORTER") or "otlp").strip().lower()
    endpoint = os.getenv(f"OTEL_EXPORTER_OTLP_{signal}_ENDPOINT")
    if not endpoint:
        endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        if endpoint:
            endpoint = f"{endpoint.removesuffix('/')}/v1/{signal.lower()}"
    if not endpoint or exporter == "none":
        return None
    if exporter != "otlp":
        raise FastAPIError(
            f"FastAPI automatic telemetry supports OTEL_{signal}_EXPORTER=otlp or none. "
            "Configure other exporters explicitly and pass telemetry={'auto_configure': False} to FastAPI()."
        )
    protocol = (
        os.getenv(f"OTEL_EXPORTER_OTLP_{signal}_PROTOCOL")
        or os.getenv("OTEL_EXPORTER_OTLP_PROTOCOL")
        or "http/protobuf"
    )
    if protocol != "http/protobuf":
        raise FastAPIError(
            "FastAPI automatic telemetry requires the OTLP http/protobuf protocol. Configure other transports explicitly and pass telemetry={'auto_configure': False} to FastAPI()."
        )
    parsed = urlsplit(endpoint)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise FastAPIError(
            f"Invalid OTLP {signal.lower()} endpoint. Use an absolute HTTP or HTTPS URL."
        )
    return endpoint


def _registration_provider(provider: Any) -> Any:
    # Older Logfire meter wrappers do not expose add_metric_reader(). Attach
    # the reader to their SDK provider. Measurements still use the original wrapper.
    if (
        type(provider).__module__ == "logfire._internal.metrics"
        and type(provider).__name__ == "ProxyMeterProvider"
        and not hasattr(provider, "add_metric_reader")
    ):
        return provider.provider
    return provider


def _configure_from_environment(config: TelemetryConfig) -> None:
    """Add OTLP exporters from the environment to the selected providers.

    Called automatically before ASGI lifespan startup. Existing providers and
    their exporters are preserved. FastAPI registers its own export components once
    per provider. It does not inspect or deduplicate other components' exporters.
    Pass `telemetry={"auto_configure": False}` to `FastAPI()` when another component
    manages environment export.
    """
    if (
        not config["auto_configure"]
        or os.getenv("OTEL_SDK_DISABLED", "").lower() == "true"
    ):
        return
    with _lock:
        signals = [
            ("TRACES", config["tracing"], config["tracer_provider"]),
            ("METRICS", config["metrics"], config["meter_provider"]),
            ("LOGS", config["logs"], config["logger_provider"]),
        ]
        requested = [
            (signal, provider, endpoint)
            for signal, enabled, provider in signals
            if enabled and (endpoint := _export_endpoint(signal)) is not None
        ]
        if not requested:
            return
        try:
            from opentelemetry.exporter.otlp.proto.http._log_exporter import (
                OTLPLogExporter,
            )
            from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
                OTLPMetricExporter,
            )
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                OTLPSpanExporter,
            )
            from opentelemetry.sdk._logs import LoggerProvider
            from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
            from opentelemetry.sdk.metrics import MeterProvider
            from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
        except ImportError as exc:
            raise FastAPIError(
                "Automatic OpenTelemetry export requires fastapi[opentelemetry] or fastapi[standard]. Install the extra, configure providers yourself, or pass telemetry={'auto_configure': False} to FastAPI()."
            ) from exc
        # The SDK's registration methods also allow vendor wrappers to forward
        # additions. Keep a record of our own registrations, without examining
        # another component's exporters or their destinations.
        providers = {
            "TRACES": ("tracer", trace.get_tracer_provider),
            "METRICS": ("meter", metrics.get_meter_provider),
            "LOGS": ("logger", _logs.get_logger_provider),
        }

        def create_component(*, signal: str, endpoint: str) -> Any:
            if signal == "TRACES":
                return BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
            if signal == "METRICS":
                return PeriodicExportingMetricReader(
                    OTLPMetricExporter(endpoint=endpoint)
                )
            return BatchLogRecordProcessor(OTLPLogExporter(endpoint=endpoint))

        for signal, explicit, endpoint in requested:
            name, get_provider = providers[signal]
            provider = _registration_provider(
                explicit if explicit is not None else get_provider()
            )
            if any(s == signal and p is provider for s, p in _configured):
                continue
            if explicit is None and _unconfigured(provider):
                component = create_component(signal=signal, endpoint=endpoint)
                if signal == "TRACES":
                    provider = TracerProvider(shutdown_on_exit=False)
                    provider.add_span_processor(component)
                    trace.set_tracer_provider(provider)
                elif signal == "METRICS":
                    provider = MeterProvider(
                        metric_readers=[component], shutdown_on_exit=False
                    )
                    metrics.set_meter_provider(provider)
                else:
                    provider = LoggerProvider(shutdown_on_exit=False)
                    provider.add_log_record_processor(component)
                    _logs.set_logger_provider(provider)
                current = get_provider()
                if current is provider:
                    _configured.append((signal, provider))
                    _owned.append(provider)
                    continue
                # Another component configured the global provider concurrently.
                # Close the unused pipeline and attach a new component to theirs.
                provider.shutdown()
                provider = _registration_provider(current)
            # Vendor wrappers can expose the SDK registration methods without
            # inheriting its provider classes. Check each method against its SDK
            # class statically and its availability on the provider at runtime.
            register: Callable[[Any], None] | None
            try:
                if signal == "TRACES":
                    register = cast(TracerProvider, provider).add_span_processor
                elif signal == "METRICS":
                    register = cast(MeterProvider, provider).add_metric_reader
                else:
                    register = cast(LoggerProvider, provider).add_log_record_processor
            except AttributeError:
                register = None
            if not callable(register):
                raise FastAPIError(
                    f"The configured OpenTelemetry {name} provider does not support "
                    "adding an OTLP exporter. Configure environment export through "
                    "that provider and pass telemetry={'auto_configure': False} to FastAPI()."
                )
            component = create_component(signal=signal, endpoint=endpoint)
            try:
                register(component)
            except Exception:
                component.shutdown()
                raise
            _configured.append((signal, provider))
            _owned.append(component)


async def lifespan(
    *, config: TelemetryConfig, app: ASGIApp, scope: Scope, receive: Receive, send: Send
) -> None:
    # Consume startup only inside the wrapper, and preserve ASGI failure events.
    # Initialization exceptions before app(scope) would otherwise look like a
    # server's unsupported-lifespan fallback and silently disable telemetry.
    async def wrapped_receive() -> Message:
        message = await receive()
        if message["type"] == "lifespan.startup":
            try:
                _configure_from_environment(config)
            except Exception as exc:
                await send({"type": "lifespan.startup.failed", "message": str(exc)})
                raise
        return message

    async def wrapped_send(message: Message) -> None:
        if (
            message["type"]
            in {
                "lifespan.shutdown.complete",
                "lifespan.shutdown.failed",
                "lifespan.startup.failed",
            }
            and _owned
        ):
            await run_sync(_flush)
        await send(message)

    await app(scope, wrapped_receive, wrapped_send)
