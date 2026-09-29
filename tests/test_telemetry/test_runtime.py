import asyncio
import threading
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.exceptions import FastAPIError
from fastapi.telemetry import _runtime as runtime
from fastapi.testclient import TestClient

from ._otlp import otlp_collector
from ._subprocess import run_in_subprocess


def test_otlp_collector_does_not_resolve_hostname(monkeypatch):
    # Reverse DNS during HTTPServer binding caused macOS CI timeouts.
    lookup = Mock()
    monkeypatch.setattr("socket.getfqdn", lookup)
    with otlp_collector():
        pass
    lookup.assert_not_called()


@pytest.mark.parametrize("base_path", ["", "/collector/"])
@run_in_subprocess
def test_real_otlp_export_and_repeated_lifespans(base_path):
    import os
    from contextlib import asynccontextmanager

    from fastapi import FastAPI
    from fastapi.telemetry import _runtime
    from fastapi.testclient import TestClient
    from opentelemetry import _logs, trace
    from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import (
        ExportLogsServiceRequest,
    )
    from opentelemetry.proto.collector.metrics.v1.metrics_service_pb2 import (
        ExportMetricsServiceRequest,
    )
    from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
        ExportTraceServiceRequest,
    )
    from opentelemetry.proto.trace.v1.trace_pb2 import Span

    with otlp_collector() as (base, received):
        prefix = base_path.rstrip("/")
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = base + base_path
        os.environ["OTEL_SERVICE_NAME"] = "native-test"
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = "x-test=value"
        os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "test.resource=example"
        os.environ["OTEL_BSP_SCHEDULE_DELAY"] = "60000"
        os.environ["OTEL_BLRP_SCHEDULE_DELAY"] = "60000"
        os.environ["OTEL_METRIC_EXPORT_INTERVAL"] = "60000"
        seen = []

        @asynccontextmanager
        async def lifespan(app):
            seen.append(trace.get_tracer_provider())
            yield

        app = FastAPI(lifespan=lifespan)

        @app.get("/items/{value}")
        def endpoint(value: int):
            _logs.get_logger("test").emit(body="request processed")
            return value

        try:
            for _ in range(2):
                with TestClient(app) as client:
                    assert client.get("/items/3").json() == 3
            assert len(_runtime._owned) == 3
            assert seen[0] is seen[1]
            assert all(headers.get("x-test") == "value" for _, _, headers in received)
            traces = [
                ExportTraceServiceRequest.FromString(body)
                for path, body, _ in received
                if path == prefix + "/v1/traces"
            ]
            spans = [
                span
                for request in traces
                for resource in request.resource_spans
                for scope in resource.scope_spans
                for span in scope.spans
            ]
            assert len(spans) == 8
            servers = [span for span in spans if span.kind == Span.SPAN_KIND_SERVER]
            assert len(servers) == 2
            assert all(span.name == "GET /items/{value}" for span in servers)
            metric_requests = [
                ExportMetricsServiceRequest.FromString(body)
                for path, body, _ in received
                if path == prefix + "/v1/metrics"
            ]
            assert metric_requests
            resources = metric_requests[-1].resource_metrics
            resource_attributes = {
                a.key: a.value.string_value for a in resources[0].resource.attributes
            }
            assert resource_attributes["service.name"] == "native-test"
            assert resource_attributes["test.resource"] == "example"
            histograms = [
                metric.histogram
                for resource in resources
                for scope in resource.scope_metrics
                for metric in scope.metrics
                if metric.name == "http.server.request.duration"
            ]
            assert histograms[0].data_points[0].count == 2
            log_requests = [
                ExportLogsServiceRequest.FromString(body)
                for path, body, _ in received
                if path == prefix + "/v1/logs"
            ]
            records = [
                record
                for request in log_requests
                for resource in request.resource_logs
                for scope in resource.scope_logs
                for record in scope.log_records
            ]
            assert len(records) == 2
            assert all(
                record.body.string_value == "request processed" for record in records
            )
        finally:
            _runtime._shutdown()


@pytest.mark.parametrize(
    "env",
    [
        {
            "OTEL_TRACES_EXPORTER": "",
            "OTEL_METRICS_EXPORTER": "",
            "OTEL_LOGS_EXPORTER": "",
            "OTEL_EXPORTER_OTLP_PROTOCOL": "",
            "OTEL_EXPORTER_OTLP_TRACES_PROTOCOL": "",
            "OTEL_EXPORTER_OTLP_METRICS_PROTOCOL": "",
            "OTEL_EXPORTER_OTLP_LOGS_PROTOCOL": "",
        },
        {
            "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT": "",
            "OTEL_EXPORTER_OTLP_METRICS_ENDPOINT": "",
            "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT": "",
        },
    ],
)
def test_empty_environment_uses_defaults(monkeypatch, env):
    monkeypatch.setenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:4318/collector/"
    )
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    for signal in ("TRACES", "METRICS", "LOGS"):
        assert runtime._export_endpoint(signal) == (
            f"http://127.0.0.1:4318/collector/v1/{signal.lower()}"
        )


@pytest.mark.parametrize("protocol", ["http/protobuf", "grpc"])
def test_empty_signal_protocol_uses_general_protocol(monkeypatch, protocol):
    monkeypatch.setenv(
        "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", "http://127.0.0.1:4318/v1/traces"
    )
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_PROTOCOL", protocol)
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_TRACES_PROTOCOL", "")
    if protocol == "http/protobuf":
        assert runtime._export_endpoint("TRACES") == "http://127.0.0.1:4318/v1/traces"
    else:
        with pytest.raises(FastAPIError, match="http/protobuf"):
            runtime._export_endpoint("TRACES")


@pytest.mark.parametrize("signal", ["TRACES", "METRICS", "LOGS"])
def test_signal_endpoint_overrides_general_endpoint(monkeypatch, signal):
    endpoint = "http://127.0.0.1:4318/custom/"
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "invalid")
    monkeypatch.setenv(f"OTEL_EXPORTER_OTLP_{signal}_ENDPOINT", endpoint)
    assert runtime._export_endpoint(signal) == endpoint


@pytest.mark.parametrize(
    "env,message",
    [
        ({"OTEL_EXPORTER_OTLP_ENDPOINT": "not-a-url"}, "absolute HTTP"),
        (
            {
                "OTEL_EXPORTER_OTLP_ENDPOINT": "http://127.0.0.1:1",
                "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
            },
            "http/protobuf",
        ),
        (
            {
                "OTEL_EXPORTER_OTLP_ENDPOINT": "http://127.0.0.1:1",
                "OTEL_TRACES_EXPORTER": "console",
            },
            "otlp or none",
        ),
    ],
)
@run_in_subprocess
def test_invalid_configuration_reports_startup_failure(env, message):
    import os

    os.environ.update(env)

    import asyncio

    from fastapi import FastAPI
    from fastapi.exceptions import FastAPIError

    messages = []

    async def receive():
        return {"type": "lifespan.startup"}

    async def send(message):
        messages.append(message)

    async def run():
        with pytest.raises(FastAPIError) as exc_info:
            await FastAPI()({"type": "lifespan", "state": {}}, receive, send)
        assert message in str(exc_info.value)

    asyncio.run(run())
    assert len(messages) == 1, messages
    assert messages[0]["type"] == "lifespan.startup.failed"


@pytest.mark.parametrize(
    "env",
    [
        {},
        {"OTEL_SERVICE_NAME": "no-endpoint"},
        {"OTEL_TRACES_EXPORTER": "otlp", "OTEL_METRICS_EXPORTER": "otlp"},
        {
            "OTEL_EXPORTER_OTLP_ENDPOINT": "http://127.0.0.1:1",
            "OTEL_TRACES_EXPORTER": "none",
            "OTEL_METRICS_EXPORTER": "none",
            "OTEL_LOGS_EXPORTER": "none",
        },
        {
            "OTEL_EXPORTER_OTLP_ENDPOINT": "http://127.0.0.1:1",
            "OTEL_SDK_DISABLED": "true",
        },
    ],
)
@run_in_subprocess
def test_no_implicit_export(env):
    import os

    os.environ.update(env)

    from fastapi import FastAPI
    from fastapi.telemetry import _runtime
    from fastapi.testclient import TestClient

    with TestClient(FastAPI()) as client:
        assert client.get("/").status_code == 404
    assert _runtime._owned == []


@run_in_subprocess
def test_missing_sdk_diagnostic():
    import os

    os.environ.update(
        {"OTEL_EXPORTER_OTLP_METRICS_ENDPOINT": "http://127.0.0.1:1/metrics"}
    )

    import sys
    from importlib.abc import MetaPathFinder

    class BlockSDK(MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            if fullname.startswith(("opentelemetry.sdk", "opentelemetry.exporter")):
                raise ImportError("SDK absent")

    sys.meta_path.insert(0, BlockSDK())
    from fastapi import FastAPI
    from fastapi.exceptions import FastAPIError
    from fastapi.testclient import TestClient

    with pytest.raises(FastAPIError) as exc_info:
        with TestClient(FastAPI()):
            pass  # pragma: no cover
    assert "fastapi[opentelemetry]" in str(exc_info.value)


@run_in_subprocess
def test_external_globals_are_unchanged_when_auto_configuration_is_disabled():
    import os

    os.environ.update({"OTEL_EXPORTER_OTLP_ENDPOINT": "http://127.0.0.1:1"})

    from fastapi import FastAPI
    from fastapi.telemetry import _runtime
    from fastapi.testclient import TestClient
    from opentelemetry import _logs, metrics, trace
    from opentelemetry.sdk._logs import LoggerProvider
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    exporter = InMemorySpanExporter()
    tp = TracerProvider()
    tp.add_span_processor(SimpleSpanProcessor(exporter))
    mp = MeterProvider()
    lp = LoggerProvider()
    _logs.set_logger_provider(lp)
    trace.set_tracer_provider(tp)
    metrics.set_meter_provider(mp)
    for _ in range(2):
        with TestClient(FastAPI(telemetry={"auto_configure": False})) as client:
            client.get("/")
    assert trace.get_tracer_provider() is tp
    assert metrics.get_meter_provider() is mp
    assert _logs.get_logger_provider() is lp
    assert not _runtime._owned
    assert len(exporter.get_finished_spans()) == 2


def test_auto_configuration_opt_out(monkeypatch):
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "invalid")
    with TestClient(FastAPI(telemetry={"auto_configure": False})) as client:
        assert client.get("/").status_code == 404


def test_owned_flush_failure_does_not_break_shutdown(monkeypatch, caplog):
    calls = []

    class FailingProvider:
        def force_flush(self):
            raise RuntimeError("flush failed")

        def shutdown(self):
            raise RuntimeError("shutdown failed")

    class Provider:
        def force_flush(self):
            calls.append("flush")

        def shutdown(self):
            calls.append("shutdown")

    monkeypatch.setattr(runtime, "_owned", [FailingProvider(), Provider()])
    with TestClient(FastAPI()) as client:
        assert client.get("/").status_code == 404
    runtime._shutdown()
    runtime._shutdown()
    assert calls == ["flush", "shutdown"]
    assert caplog.text.count("FastAPI telemetry cleanup failed") == 2


@pytest.mark.parametrize(
    "message_type",
    [
        "lifespan.startup.failed",
        "lifespan.shutdown.failed",
        "lifespan.shutdown.complete",
    ],
)
def test_lifespan_flush_runs_off_event_loop(monkeypatch, message_type):
    calls = []
    flush_threads = []
    event_loop_thread = threading.get_ident()

    class Provider:
        def force_flush(self):
            flush_threads.append(threading.get_ident())
            calls.append("flush")

        def shutdown(self):
            calls.append("shutdown")

    monkeypatch.setattr(runtime, "_owned", [Provider()])

    async def app(scope, receive, send):
        assert await receive() == {"type": "lifespan.startup"}
        await send({"type": message_type})

    async def receive():
        return {"type": "lifespan.startup"}

    async def send(message):
        calls.append(message["type"])

    asyncio.run(
        runtime.lifespan(
            config=FastAPI()._telemetry, app=app, scope={}, receive=receive, send=send
        )
    )
    assert calls == ["flush", message_type]
    assert len(flush_threads) == 1
    assert flush_threads[0] != event_loop_thread
    runtime._shutdown()
    runtime._shutdown()
    assert calls == ["flush", message_type, "shutdown"]


def test_registration_provider_prefers_public_metric_reader(monkeypatch):
    from logfire._internal.metrics import ProxyMeterProvider
    from opentelemetry.metrics import NoOpMeterProvider

    provider = NoOpMeterProvider()
    proxy = ProxyMeterProvider(provider=provider)
    assert runtime._registration_provider(proxy) is provider

    monkeypatch.setattr(proxy, "add_metric_reader", lambda reader: None, raising=False)
    assert runtime._registration_provider(proxy) is proxy


@pytest.mark.parametrize("wrapped_meter", [False, True])
def test_concurrent_provider_owner_wins(monkeypatch, wrapped_meter):
    from opentelemetry import _logs, metrics, trace
    from opentelemetry.sdk import _logs as sdk_logs
    from opentelemetry.sdk import metrics as sdk_metrics
    from opentelemetry.sdk import trace as sdk_trace

    stopped = []
    winners = []
    for name, api, sdk, cls_name in [
        ("tracer", trace, sdk_trace, "TracerProvider"),
        ("meter", metrics, sdk_metrics, "MeterProvider"),
        ("logger", _logs, sdk_logs, "LoggerProvider"),
    ]:
        original = getattr(sdk, cls_name)
        winner = original(shutdown_on_exit=False)
        winners.append(winner)

        class Provider(original):
            def shutdown(self, _name=name):
                stopped.append(_name)
                super().shutdown()

        if wrapped_meter and name == "meter":
            from logfire._internal.metrics import ProxyMeterProvider

            winner = ProxyMeterProvider(winner)
        current = [getattr(api, f"get_{name}_provider")()]
        monkeypatch.setattr(sdk, cls_name, Provider)
        monkeypatch.setattr(api, f"get_{name}_provider", lambda c=current: c[0])
        monkeypatch.setattr(
            api,
            f"set_{name}_provider",
            lambda provider, c=current, w=winner: c.__setitem__(0, w),
        )
    monkeypatch.setattr(runtime, "_owned", [])
    monkeypatch.setattr(runtime, "_configured", [])
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:1")
    runtime._configure_from_environment(FastAPI()._telemetry)
    assert stopped == ["tracer", "meter", "logger"]
    assert [provider for _, provider in runtime._configured] == winners
    assert len(runtime._owned) == 3
    assert all(component not in winners for component in runtime._owned)
    runtime._shutdown()
    for winner in winners:
        winner.shutdown()


@pytest.mark.skipif(
    not hasattr(__import__("os"), "fork"), reason="POSIX worker lifecycle"
)
@run_in_subprocess
def test_environment_export_initializes_after_fork():
    import os
    import threading
    from http.server import BaseHTTPRequestHandler

    from fastapi import FastAPI
    from fastapi.telemetry import _runtime
    from fastapi.testclient import TestClient

    from tests.test_telemetry._otlp import _CollectorServer

    received = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            self.rfile.read(int(self.headers["Content-Length"]))
            received.append(self.path)
            self.send_response(200)
            self.end_headers()

        def log_message(self, format, *args):
            pass

    server = _CollectorServer(("127.0.0.1", 0), Handler)
    os.environ["OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"] = (
        f"http://127.0.0.1:{server.server_port}/traces"
    )
    # Importing and constructing before fork must not create providers.
    app = FastAPI()
    assert not _runtime._owned
    pid = os.fork()
    if pid == 0:
        try:
            with TestClient(app) as client:
                assert client.get("/").status_code == 404
            assert len(_runtime._owned) == 1
            _runtime._shutdown()
        except BaseException:  # pragma: no cover
            os._exit(1)
        os._exit(0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    _, status = os.waitpid(pid, 0)
    assert status == 0, status
    assert received == ["/traces"], received
    assert not _runtime._owned
    server.shutdown()
    server.server_close()


@run_in_subprocess
def test_real_otlp_exception_export_without_traces_or_metrics():
    import os

    from fastapi import FastAPI
    from fastapi.telemetry import _runtime
    from fastapi.testclient import TestClient
    from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import (
        ExportLogsServiceRequest,
    )

    with otlp_collector() as (base, received):
        os.environ["OTEL_EXPORTER_OTLP_LOGS_ENDPOINT"] = base + "/logs"
        os.environ["OTEL_SERVICE_NAME"] = "errors-only"
        app = FastAPI()

        @app.get("/items/{item_id}")
        def endpoint(item_id: int):
            raise ValueError("exported exception")

        try:
            for _ in range(2):
                with TestClient(app, raise_server_exceptions=False) as client:
                    assert client.get("/items/1").status_code == 500
            assert len(_runtime._owned) == 1
            assert all(path == "/logs" for path, _, _ in received)
            requests = [
                ExportLogsServiceRequest.FromString(body) for _, body, _ in received
            ]
            records = [
                record
                for request in requests
                for resource in request.resource_logs
                for scope in resource.scope_logs
                for record in scope.log_records
            ]
            assert len(records) == 2
            for record in records:
                attributes = {a.key: a.value.string_value for a in record.attributes}
                assert attributes["exception.type"] == "ValueError"
                assert attributes["exception.message"] == "exported exception"
                assert attributes["http.route"] == "/items/{item_id}"
                assert "in endpoint" in attributes["exception.stacktrace"]
                assert (
                    "ValueError: exported exception"
                    in attributes["exception.stacktrace"]
                )
        finally:
            _runtime._shutdown()


@pytest.mark.parametrize("name", ["tracer", "meter", "logger"])
def test_unsupported_provider_reports_configuration_error(monkeypatch, name):
    signal = {"tracer": "TRACES", "meter": "METRICS", "logger": "LOGS"}[name]
    monkeypatch.setenv(f"OTEL_EXPORTER_OTLP_{signal}_ENDPOINT", "http://127.0.0.1:1")
    app = FastAPI(telemetry={f"{name}_provider": object()})
    with pytest.raises(FastAPIError, match="does not support.*auto_configure"):
        with TestClient(app):
            pass  # pragma: no cover


@pytest.mark.parametrize("error_type", [ValueError, AttributeError])
def test_failed_registration_closes_new_exporter(monkeypatch, error_type):
    from opentelemetry.exporter.otlp.proto.http import trace_exporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    stopped = []

    class Exporter(InMemorySpanExporter):
        def __init__(self, *, endpoint):
            super().__init__()

        def shutdown(self):
            stopped.append(True)
            super().shutdown()

    provider = TracerProvider(shutdown_on_exit=False)

    def fail(component):
        raise error_type("registration failed")

    monkeypatch.setattr(provider, "add_span_processor", fail)
    monkeypatch.setattr(trace_exporter, "OTLPSpanExporter", Exporter)
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", "http://127.0.0.1:1")
    app = FastAPI(telemetry={"tracer_provider": provider})
    with pytest.raises(error_type, match="registration failed"):
        with TestClient(app):
            pass  # pragma: no cover
    assert stopped == [True]
    provider.shutdown()
