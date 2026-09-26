import gc
import weakref

import anyio
import pytest
from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket
from fastapi.telemetry import get_telemetry_data
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from opentelemetry import context
from opentelemetry._logs import SeverityNumber
from opentelemetry.sdk._logs import LoggerProvider, LogRecordProcessor
from opentelemetry.sdk._logs.export import (
    InMemoryLogRecordExporter,
    SimpleLogRecordProcessor,
)
from pydantic import BaseModel
from starlette.websockets import WebSocketDisconnect

from ._otlp import otlp_collector


@pytest.mark.anyio
async def test_data_is_local_to_each_request_and_cleared_afterwards(telemetry):
    config, _, _ = telemetry
    child = FastAPI(telemetry=config)
    app = FastAPI(telemetry=config)
    app.mount("/child", child)
    saved_contexts = []
    saved_data = []
    entered = 0
    ready = anyio.Event()
    service = object()

    class Item(BaseModel):
        name: str

    def dependency(request: Request):
        data = get_telemetry_data()
        assert data is not None
        assert data.request is request
        assert data.values is None
        assert data.body == {"name": request.path_params["name"]}
        return service

    @child.post("/{name}")
    async def endpoint(
        *, name: str, item: Item, request: Request, value=Depends(dependency)
    ):
        nonlocal entered
        data = get_telemetry_data()
        assert data is not None
        assert data.request is request
        assert data.values is not None
        assert data.values["item"] is item
        assert data.values["value"] is service
        entered += 1
        if entered == 2:
            ready.set()
        await ready.wait()
        assert get_telemetry_data() is data
        assert data.values["name"] == name
        assert data.errors == []
        saved_contexts.append(context.get_current())
        saved_data.append(data)
        return name

    assert get_telemetry_data() is None
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        results = {}

        async def send(name):
            results[name] = await client.post(f"/child/{name}", json={"name": name})

        async with anyio.create_task_group() as tasks:
            tasks.start_soon(send, "first")
            tasks.start_soon(send, "second")
    assert {name: response.json() for name, response in results.items()} == {
        "first": "first",
        "second": "second",
    }
    assert saved_data[0] is not saved_data[1]
    assert all(get_telemetry_data(ctx) is None for ctx in saved_contexts)
    assert get_telemetry_data() is None


def test_retained_context_does_not_keep_failed_request_alive(telemetry):
    config, _, _ = telemetry
    app = FastAPI(telemetry={**config, "tracing": False, "logs": False})
    saved_contexts = []
    request_refs = []

    @app.post("/")
    async def endpoint(request: Request):
        await request.body()
        saved_contexts.append(context.get_current())
        request_refs.append(weakref.ref(request))
        raise ValueError("endpoint failed")

    with TestClient(app, raise_server_exceptions=False) as client:
        assert client.post("/", json={"name": "request data"}).status_code == 500

    gc.collect()
    assert get_telemetry_data(saved_contexts[0]) is None
    assert request_refs[0]() is None


@pytest.mark.parametrize("invalid_json", [False, True])
@pytest.mark.parametrize("logging", [False, True])
def test_validation_data_without_tracing(invalid_json, logging):
    exporter = InMemoryLogRecordExporter()
    provider = LoggerProvider(shutdown_on_exit=False)
    observed = []

    class Validation(LogRecordProcessor):
        def on_emit(self, log_record):
            record = log_record.log_record
            data = get_telemetry_data(record.context)
            assert data is not None
            assert data.request is not None
            assert data.request.url.path == "/items"
            assert data.errors is not None
            assert data.errors[0]["type"] == (
                "json_invalid" if invalid_json else "int_parsing"
            )
            assert data.body == ("{" if invalid_json else {"amount": "private-input"})
            observed.append(record.context)

        def shutdown(self):
            pass

        def force_flush(self, timeout_millis=30000):
            return True

    provider.add_log_record_processor(Validation())
    provider.add_log_record_processor(SimpleLogRecordProcessor(exporter))
    app = FastAPI(
        telemetry={"logger_provider": provider, "tracing": False, "logs": logging}
    )

    @app.post("/items")
    def endpoint(item: dict[str, int]):
        return item

    try:
        with TestClient(app) as client:
            response = (
                client.post(
                    "/items", content="{", headers={"content-type": "application/json"}
                )
                if invalid_json
                else client.post("/items", json={"amount": "private-input"})
            )
        assert response.status_code == 422
        if not logging:
            assert not exporter.get_finished_logs()
            assert observed == []
            return
        (data,) = exporter.get_finished_logs()
        record = data.log_record
        assert record.severity_number == SeverityNumber.WARN
        assert record.event_name == "fastapi.validation.failed"
        assert record.exception is None
        assert record.attributes == {
            "http.route": "/items",
            "fastapi.validation.error_count": 1,
        }
        assert record.body == "Request validation failed"
        assert len(observed) == 1
        assert get_telemetry_data(observed[0]) is None
        assert get_telemetry_data(record.context) is None
    finally:
        provider.shutdown()


def test_request_objects_are_not_exported():
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import (
        ExportLogsServiceRequest,
    )
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor

    with otlp_collector() as (base, received):
        logger = LoggerProvider(shutdown_on_exit=False)
        logger.add_log_record_processor(
            SimpleLogRecordProcessor(OTLPLogExporter(endpoint=base + "/v1/logs"))
        )
        tracer = TracerProvider(shutdown_on_exit=False)
        tracer.add_span_processor(
            SimpleSpanProcessor(OTLPSpanExporter(endpoint=base + "/v1/traces"))
        )
        app = FastAPI(telemetry={"tracer_provider": tracer, "logger_provider": logger})
        service = object()

        def dependency():
            return service

        @app.post("/items")
        def endpoint(*, item: dict[str, str], count: int, value=Depends(dependency)):
            data = get_telemetry_data()
            assert data is not None
            assert data.values is not None
            assert data.values["value"] is service
            raise ValueError("endpoint failed")

        @app.get("/handled")
        def handled():
            raise HTTPException(503, "private-handled-detail")

        @app.websocket("/ws")
        async def websocket_endpoint(*, websocket: WebSocket, count: int):
            data = get_telemetry_data()
            assert data is not None
            assert data.websocket is websocket
            assert data.body is None
            await websocket.accept()
            await websocket.send_text(await websocket.receive_text())
            await websocket.close()

        try:
            with TestClient(app, raise_server_exceptions=False) as client:
                with client.websocket_connect(
                    "/ws?count=1&query=websocket-search",
                    headers={
                        "authorization": "Bearer authorization-secret",
                        "cookie": "session=session-secret",
                    },
                ) as websocket:
                    websocket.send_text("private-websocket-message")
                    assert websocket.receive_text() == "private-websocket-message"
                with pytest.raises(WebSocketDisconnect):
                    with client.websocket_connect("/ws?count=invalid-websocket-count"):
                        pass
                assert client.get("/handled").status_code == 503
                for count, status in [("1", 500), ("invalid-count", 422)]:
                    response = client.post(
                        "/items",
                        params={"count": count, "query": "search-term"},
                        headers={
                            "authorization": "Bearer authorization-secret",
                            "cookie": "session=session-secret",
                        },
                        json={"name": "private-body"},
                    )
                    assert response.status_code == status
            assert {path for path, _, _ in received} == {"/v1/logs", "/v1/traces"}
            for path, payload, _ in received:
                if path == "/v1/logs":
                    assert b"invalid-count" not in payload
                    assert b"search-term" not in payload
                for uncaptured_value in [
                    b"websocket-search",
                    b"invalid-websocket-count",
                    b"authorization-secret",
                    b"session-secret",
                    b"private-body",
                    b"private-handled-detail",
                    b"private-websocket-message",
                ]:
                    assert uncaptured_value not in payload
            traces = b"".join(
                payload for path, payload, _ in received if path == "/v1/traces"
            )
            assert b"invalid-count" in traces
            assert b"search-term" in traces
            records = [
                record
                for path, payload, _ in received
                if path == "/v1/logs"
                for resource in ExportLogsServiceRequest.FromString(
                    payload
                ).resource_logs
                for scope in resource.scope_logs
                for record in scope.log_records
            ]
            assert len(records) == 3
            assert records[0].event_name == "fastapi.validation.failed"
            assert records[2].event_name == "fastapi.validation.failed"
        finally:
            tracer.shutdown()
            logger.shutdown()
