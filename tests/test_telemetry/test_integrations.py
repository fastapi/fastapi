"""Published integration compatibility, isolated because SDKs patch globals."""

import os

import pytest

from ._subprocess import run_in_subprocess


@pytest.mark.parametrize("mode", ["app", "global", "late", "uninstrument"])
@run_in_subprocess
def test_current_contrib(mode):
    import os

    os.environ.update({"OTEL_SEMCONV_STABILITY_OPT_IN": "http"})

    import fastapi
    from fastapi.testclient import TestClient
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import InMemoryMetricReader
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )
    from opentelemetry.trace import SpanKind

    native = InMemorySpanExporter()
    legacy = InMemorySpanExporter()
    p1, p2 = TracerProvider(), TracerProvider()
    p1.add_span_processor(SimpleSpanProcessor(native))
    p2.add_span_processor(SimpleSpanProcessor(legacy))
    r1, r2 = InMemoryMetricReader(), InMemoryMetricReader()
    m1, m2 = MeterProvider(metric_readers=[r1]), MeterProvider(metric_readers=[r2])
    hooks = []

    def server_request_hook(span, scope):
        hooks.append(scope["path"])

    if mode == "global":
        FastAPIInstrumentor().instrument(
            tracer_provider=p2,
            meter_provider=m2,
            server_request_hook=server_request_hook,
            exclude_spans=["send", "receive"],
        )
    app = fastapi.FastAPI(telemetry={"tracer_provider": p1, "meter_provider": m1})

    @app.get("/items/{value}")
    def endpoint(value: int):
        return value

    client = TestClient(app)
    if mode == "late":
        assert client.get("/items/1").json() == 1
    if mode != "global":
        FastAPIInstrumentor.instrument_app(
            app,
            tracer_provider=p2,
            meter_provider=m2,
            server_request_hook=server_request_hook,
            exclude_spans=["send", "receive"],
        )
    assert client.get("/items/2").json() == 2
    if mode == "late":
        # Current contrib cannot replace an already-built stack. Native remains live.
        assert len(native.get_finished_spans()) == 8
        assert not legacy.get_finished_spans()
    else:
        assert not native.get_finished_spans()
        assert (
            len([s for s in legacy.get_finished_spans() if s.kind == SpanKind.SERVER])
            == 1
        )
        assert hooks == ["/items/2"]
        assert r1.get_metrics_data() is None
    if mode == "uninstrument":
        FastAPIInstrumentor.uninstrument_app(app)
        assert client.get("/items/3").json() == 3
        assert len(native.get_finished_spans()) == 4

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: fastapi.WebSocket):
        await websocket.accept()
        await websocket.close()

    native.clear()
    legacy.clear()
    with client.websocket_connect("/ws"):
        pass
    if mode in ("late", "uninstrument"):
        assert len(native.get_finished_spans()) == 3
        assert not legacy.get_finished_spans()
    else:
        assert not native.get_finished_spans()
        assert (
            len(
                [
                    span
                    for span in legacy.get_finished_spans()
                    if span.kind == SpanKind.SERVER
                ]
            )
            == 1
        )
        assert hooks[-1] == "/ws"


@pytest.mark.parametrize("order", ["before", "after"])
@run_in_subprocess
def test_current_logfire(order):
    import logfire
    from fastapi import FastAPI, WebSocket
    from fastapi.testclient import TestClient
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )
    from opentelemetry.trace import SpanKind

    legacy, native = InMemorySpanExporter(), InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(native))

    def configure():
        logfire.configure(
            send_to_logfire=False,
            console=False,
            metrics=False,
            additional_span_processors=[SimpleSpanProcessor(legacy)],
        )

    if order == "before":
        configure()
    app = FastAPI(telemetry={"tracer_provider": provider})
    if order == "after":
        configure()

    @app.get("/items/{value}")
    def endpoint(value: int):
        return value

    mapped = []

    def mapper(request, attributes):
        mapped.append(request.url.path)
        return attributes

    logfire.instrument_fastapi(app, request_attributes_mapper=mapper, extra_spans=True)
    assert TestClient(app).get("/items/5").json() == 5
    spans = legacy.get_finished_spans()
    assert len([s for s in spans if s.kind == SpanKind.SERVER]) == 1, spans
    assert any("arguments" in s.name for s in spans)
    assert any(
        s.attributes is not None
        and s.attributes.get("code.function")
        in (endpoint.__name__, endpoint.__qualname__)
        for s in spans
    )
    assert mapped == ["/items/5"]
    assert not native.get_finished_spans()

    @app.websocket("/ws/{value}")
    async def websocket_endpoint(*, websocket: WebSocket, value: int):
        await websocket.accept()
        await websocket.close()

    legacy.clear()
    with TestClient(app).websocket_connect("/ws/5"):
        pass
    assert not native.get_finished_spans()
    assert (
        len(
            [
                span
                for span in legacy.get_finished_spans()
                if span.kind == SpanKind.SERVER
            ]
        )
        == 1
    )
    assert mapped[-1] == "/ws/5"


@pytest.mark.parametrize("sampling", [0.0, 1.0])
@run_in_subprocess
def test_current_sentry(sampling):
    import sentry_sdk
    from fastapi import FastAPI, HTTPException, WebSocket
    from fastapi.testclient import TestClient
    from opentelemetry.sdk._logs import LoggerProvider
    from opentelemetry.sdk._logs.export import (
        InMemoryLogRecordExporter,
        SimpleLogRecordProcessor,
    )
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.starlette import StarletteIntegration
    from sentry_sdk.transport import Transport

    items = []

    class LocalTransport(Transport):
        def capture_envelope(self, envelope):
            items.extend(item.type for item in envelope.items)

    sentry_sdk.init(
        dsn="https://public@example.invalid/1",
        transport=LocalTransport,
        default_integrations=False,
        auto_enabling_integrations=False,
        integrations=[StarletteIntegration(), FastApiIntegration()],
        traces_sample_rate=sampling,
        send_client_reports=False,
    )
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    logs = InMemoryLogRecordExporter()
    logger = LoggerProvider()
    logger.add_log_record_processor(SimpleLogRecordProcessor(logs))
    app = FastAPI(telemetry={"tracer_provider": provider, "logger_provider": logger})

    @app.get("/items/{value}")
    def endpoint(value: int):
        if value == 2:
            raise ValueError("test")
        if value == 3:
            raise HTTPException(503, "handled")
        return value

    client = TestClient(app, raise_server_exceptions=False)
    assert client.get("/items/1").status_code == 200
    assert client.get("/items/2").status_code == 500
    assert client.get("/items/3").status_code == 503
    sentry_sdk.flush()
    assert items.count("event") == 2, items
    (unhandled,) = logs.get_finished_logs()
    assert isinstance(unhandled.log_record.exception, ValueError)
    assert items.count("transaction") == (3 if sampling else 0), items
    assert len(exporter.get_finished_spans()) == 10

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        raise ValueError("websocket failed")

    with pytest.raises(ValueError, match="websocket failed"):
        with client.websocket_connect("/ws") as websocket:
            websocket.receive()
    sentry_sdk.flush()
    assert items.count("event") == 3, items
    assert items.count("transaction") == (4 if sampling else 0), items
    assert len(exporter.get_finished_spans()) == 13
    assert len(logs.get_finished_logs()) == 2


@run_in_subprocess
def test_api_only_and_no_implicit_sdk_import():
    import sys
    from importlib.abc import MetaPathFinder

    class BlockSDK(MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            if fullname.startswith(("opentelemetry.sdk", "opentelemetry.exporter")):
                raise AssertionError(f"Unexpected optional import: {fullname}")

    sys.meta_path.insert(0, BlockSDK())
    from fastapi import FastAPI, WebSocket
    from fastapi.testclient import TestClient

    app = FastAPI()

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    with TestClient(app) as client:
        assert client.get("/").status_code == 404
        with client.websocket_connect("/ws"):
            pass
    assert not any(name.startswith("opentelemetry.sdk") for name in sys.modules)


def test_inactive_sentry_does_not_disable_native(telemetry):
    import sentry_sdk
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    config, exporter, reader = telemetry
    assert sentry_sdk.get_client().get_integration("fastapi") is None
    assert TestClient(FastAPI(telemetry=config)).get("/").status_code == 404
    assert len(exporter.get_finished_spans()) == 1


@run_in_subprocess
def test_logfire_global_provider_without_fastapi_instrumentor():
    import logfire
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    exporter = InMemorySpanExporter()
    logfire.configure(
        send_to_logfire=False,
        console=False,
        metrics=False,
        additional_span_processors=[SimpleSpanProcessor(exporter)],
    )
    app = FastAPI()

    @app.get("/")
    def endpoint():
        return "ok"

    assert TestClient(app).get("/").json() == "ok"
    spans = exporter.get_finished_spans()
    assert {span.name for span in spans} == {
        "GET /",
        "fastapi.dependencies",
        "fastapi.endpoint",
        "fastapi.serialization",
    }
    assert all(
        span.instrumentation_scope is not None
        and span.instrumentation_scope.name == "fastapi"
        for span in spans
    )


def test_environment_isolation_removes_export_credentials(monkeypatch):
    from .conftest import remove_export_environment

    for name in ["OTEL_EXPORTER_OTLP_HEADERS", "LOGFIRE_TOKEN", "SENTRY_DSN"]:
        monkeypatch.setenv(name, "test-only")
    remove_export_environment(monkeypatch)
    assert not any(
        name.startswith(("OTEL_", "LOGFIRE_", "SENTRY_")) for name in os.environ
    )
