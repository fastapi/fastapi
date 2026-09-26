"""Integration prototypes using standard OpenTelemetry SDK extension points."""

import pytest

from ._subprocess import run_in_subprocess


@run_in_subprocess
def test_logfire_native_spans_and_exception_logs():
    import logfire
    from fastapi import Depends, FastAPI, WebSocket, routing
    from fastapi.telemetry import get_telemetry_data
    from fastapi.testclient import TestClient
    from opentelemetry import trace
    from opentelemetry.sdk._logs import LogRecordProcessor
    from opentelemetry.sdk._logs.export import (
        InMemoryLogRecordExporter,
        SimpleLogRecordProcessor,
    )
    from opentelemetry.sdk.trace import SpanProcessor
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    original = (
        routing.get_websocket_app,
        routing.get_request_handler,
        routing.run_endpoint_function,
        routing.solve_dependencies,
    )
    spans = InMemorySpanExporter()
    logs = InMemoryLogRecordExporter()
    dependency_value = object()
    observed = []

    class Arguments(SpanProcessor):
        def on_start(self, span, parent_context=None):
            if span.name != "fastapi.endpoint":
                return
            data = get_telemetry_data(parent_context)
            assert data is not None
            connection = data.request or data.websocket
            assert connection is not None
            assert data.values is not None
            if connection.url.path in ("/error", "/ws/error"):
                return
            assert data.values["service"] is dependency_value
            assert data.values["item_id"] == 42
            observed.append(connection.url.path)
            span.set_attribute("test.item_id", data.values["item_id"])

    class Validation(LogRecordProcessor):
        def on_emit(self, log_record):
            record = log_record.log_record
            if record.event_name != "fastapi.validation.failed":
                return
            data = get_telemetry_data(record.context)
            assert data is not None
            connection = data.request or data.websocket
            assert connection is not None
            assert data.errors is not None
            assert data.errors[0]["input"] == "invalid-item-id"
            observed.append(connection.url.path)
            record.attributes["test.error_types"] = tuple(
                error["type"] for error in data.errors
            )

        def shutdown(self):
            pass

        def force_flush(self, timeout_millis=30000):
            return True

    logfire.configure(
        send_to_logfire=False,
        console=False,
        metrics=False,
        additional_span_processors=[Arguments(), SimpleSpanProcessor(spans)],
        advanced=logfire.AdvancedOptions(
            log_record_processors=[Validation(), SimpleLogRecordProcessor(logs)]
        ),
    )
    app = FastAPI()
    contexts = []

    def dependency():
        assert trace.get_current_span().get_span_context().is_valid
        return dependency_value

    @app.get("/sync")
    def sync_endpoint(*, item_id: int, service=Depends(dependency)):
        return "ok"

    @app.get("/async")
    async def async_endpoint(*, item_id: int, service=Depends(dependency)):
        return "ok"

    @app.get("/error")
    async def error_endpoint():
        contexts.append(trace.get_current_span().get_span_context())
        raise ValueError("native error")

    @app.websocket("/ws")
    async def websocket_endpoint(
        *, websocket: WebSocket, item_id: int, service=Depends(dependency)
    ):
        await websocket.accept()
        await websocket.send_text("ok")
        await websocket.close()

    @app.websocket("/ws/error")
    async def websocket_error(websocket: WebSocket):
        contexts.append(trace.get_current_span().get_span_context())
        await websocket.accept()
        raise ValueError("native error")

    client = TestClient(app, raise_server_exceptions=False)
    assert client.get("/sync?item_id=42").json() == "ok"
    assert client.get("/async?item_id=42").json() == "ok"
    assert client.get("/error").status_code == 500
    assert client.get("/async?item_id=invalid-item-id").status_code == 422
    from starlette.websockets import WebSocketDisconnect

    with client.websocket_connect("/ws?item_id=42") as websocket:
        assert websocket.receive_text() == "ok"
    with pytest.raises(ValueError, match="native error"):
        with client.websocket_connect("/ws/error") as websocket:
            websocket.receive()
    with pytest.raises(WebSocketDisconnect) as caught:
        with client.websocket_connect("/ws?item_id=invalid-item-id"):
            pass
    assert caught.value.code == 1008
    logfire.force_flush()
    finished = spans.get_finished_spans()
    assert len([s for s in finished if s.kind == trace.SpanKind.SERVER]) == 7
    assert (
        len(
            [
                s
                for s in finished
                if s.name == "fastapi.endpoint"
                and s.attributes is not None
                and s.attributes.get("logfire.span_type") != "pending_span"
            ]
        )
        == 5
    )
    data, validation, websocket_error_log, websocket_validation = (
        logs.get_finished_logs()
    )
    assert websocket_error_log.log_record.exception is not None
    assert websocket_error_log.log_record.trace_id == contexts[1].trace_id
    assert websocket_validation.log_record.event_name == "fastapi.validation.failed"
    assert websocket_validation.log_record.attributes is not None
    assert "test.error_types" in websocket_validation.log_record.attributes
    assert len([span for span in finished if span.name == "WS /ws"]) == 2
    assert validation.log_record.event_name == "fastapi.validation.failed"
    assert validation.log_record.attributes is not None
    assert "test.error_types" in validation.log_record.attributes
    assert observed == ["/sync", "/async", "/async", "/ws", "/ws"]
    arguments = [s for s in finished if s.attributes and "test.item_id" in s.attributes]
    assert arguments
    assert all(s.attributes and s.attributes["test.item_id"] == 42 for s in arguments)
    assert get_telemetry_data() is None

    assert data.log_record.attributes is not None
    assert data.log_record.attributes["exception.message"] == "native error"
    assert data.log_record.trace_id == contexts[0].trace_id
    assert original == (
        routing.get_websocket_app,
        routing.get_request_handler,
        routing.run_endpoint_function,
        routing.solve_dependencies,
    )


@pytest.mark.parametrize("sampled", [True, False])
@run_in_subprocess
def test_sentry_standard_log_processor(sampled):
    import sentry_sdk
    from fastapi import FastAPI, WebSocket, routing
    from fastapi.telemetry import get_telemetry_data
    from fastapi.testclient import TestClient
    from opentelemetry import trace
    from opentelemetry.sdk._logs import LoggerProvider, LogRecordProcessor
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )
    from opentelemetry.sdk.trace.sampling import ALWAYS_OFF, ALWAYS_ON
    from sentry_sdk.integrations.otlp import OTLPIntegration
    from sentry_sdk.transport import Transport

    original = (
        routing.get_websocket_app,
        routing.get_request_handler,
        routing.run_endpoint_function,
        routing.solve_dependencies,
    )
    items = []

    class LocalTransport(Transport):
        def capture_envelope(self, envelope):
            items.extend(
                item.payload.json for item in envelope.items if item.type == "event"
            )

    class SentryErrors(LogRecordProcessor):
        def on_emit(self, log_record):
            if (
                log_record.instrumentation_scope.name == "fastapi"
                and log_record.log_record.exception is not None
            ):
                data = get_telemetry_data(log_record.log_record.context)
                assert data is not None
                connection = data.request or data.websocket
                assert connection is not None
                assert data.values is not None

                def enrich(event, hint):
                    event["request"] = {
                        "url": str(connection.url.replace(query=None)),
                        "query_string": str(connection.query_params),
                        "data": data.body,
                    }
                    if data.request is not None:
                        event["request"]["method"] = data.request.method
                    return event

                with sentry_sdk.new_scope() as scope:
                    scope.add_event_processor(enrich)
                    sentry_sdk.capture_exception(log_record.log_record.exception)

        def shutdown(self):
            pass

        def force_flush(self, timeout_millis=30000):
            return True

    sentry_sdk.init(
        dsn="https://public@example.invalid/1",
        transport=LocalTransport,
        default_integrations=False,
        auto_enabling_integrations=False,
        integrations=[
            OTLPIntegration(setup_otlp_traces_exporter=False, setup_propagator=False)
        ],
        send_client_reports=False,
    )
    logger = LoggerProvider()
    logger.add_log_record_processor(SentryErrors())
    tracer = TracerProvider(sampler=ALWAYS_ON if sampled else ALWAYS_OFF)
    exporter = InMemorySpanExporter()
    tracer.add_span_processor(SimpleSpanProcessor(exporter))
    app = FastAPI(telemetry={"tracer_provider": tracer, "logger_provider": logger})
    contexts = []

    @app.post("/sync")
    def sync_endpoint(payload: dict):
        contexts.append(trace.get_current_span().get_span_context())
        raise ValueError("sync error")

    @app.post("/async")
    async def async_endpoint(payload: dict):
        contexts.append(trace.get_current_span().get_span_context())
        raise ValueError("async error")

    @app.websocket("/ws")
    async def websocket_endpoint(*, websocket: WebSocket, item_id: int):
        contexts.append(trace.get_current_span().get_span_context())
        await websocket.accept()
        raise ValueError("websocket error")

    client = TestClient(app, raise_server_exceptions=False)
    assert client.post("/sync?item_id=1", json={"value": "sync"}).status_code == 500
    assert client.post("/async?item_id=2", json={"value": "async"}).status_code == 500
    with pytest.raises(ValueError, match="websocket error"):
        with client.websocket_connect("/ws?item_id=3") as websocket:
            websocket.receive()
    sentry_sdk.flush()
    assert len(items) == 3
    assert [item["request"] for item in items] == [
        {
            "method": "POST",
            "url": "http://testserver/sync",
            "query_string": "item_id=1",
            "data": {"value": "sync"},
        },
        {
            "method": "POST",
            "url": "http://testserver/async",
            "query_string": "item_id=2",
            "data": {"value": "async"},
        },
        {
            "url": "ws://testserver/ws",
            "query_string": "item_id=3",
            "data": None,
        },
    ]
    assert [item["contexts"]["trace"]["trace_id"] for item in items] == [
        format(ctx.trace_id, "032x") for ctx in contexts
    ]
    assert all(item["exception"]["values"][0]["stacktrace"]["frames"] for item in items)
    assert bool(exporter.get_finished_spans()) == sampled
    assert original == (
        routing.get_websocket_app,
        routing.get_request_handler,
        routing.run_endpoint_function,
        routing.solve_dependencies,
    )
    logger.shutdown()
    tracer.shutdown()
