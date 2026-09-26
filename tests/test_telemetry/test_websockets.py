import pytest
from fastapi import APIRouter, Depends, FastAPI, WebSocket, WebSocketException
from fastapi.telemetry import get_telemetry_data
from fastapi.testclient import TestClient
from opentelemetry import context
from opentelemetry._logs import SeverityNumber
from opentelemetry.sdk._logs import LogRecordProcessor
from opentelemetry.sdk.trace.sampling import ALWAYS_OFF
from opentelemetry.trace import StatusCode
from starlette.websockets import WebSocketDisconnect

from .conftest import server_spans


@pytest.mark.parametrize("operation_spans", [False, True])
def test_connection_context_route_and_data(telemetry, operation_spans):
    config, exporter, reader = telemetry
    config["operation_spans"] = operation_spans
    app = FastAPI(telemetry=config)
    child = FastAPI(telemetry=config)
    router = APIRouter()
    service = object()
    saved = []

    def dependency(websocket: WebSocket):
        data = get_telemetry_data()
        assert data is not None
        assert data.websocket is websocket
        assert data.request is None
        assert data.body is None
        assert data.values is None
        return service

    @router.websocket("/rooms/{room}")
    async def endpoint(*, websocket: WebSocket, room: int, value=Depends(dependency)):
        data = get_telemetry_data()
        assert data is not None
        assert data.values is not None
        assert data.values["value"] is service
        assert data.values["room"] == room
        assert data.errors == []
        saved.append(context.get_current())
        await websocket.accept()
        for _ in range(2):
            await websocket.send_text(await websocket.receive_text())
        await websocket.close()

    child.include_router(router, prefix="/api")
    app.mount("/tenants/{tenant}", child)
    with TestClient(app).websocket_connect(
        "/tenants/acme/api/rooms/42",
        headers={"traceparent": "00-" + "1" * 32 + "-" + "2" * 16 + "-01"},
    ) as websocket:
        websocket.send_text("private payload")
        assert websocket.receive_text() == "private payload"
        assert not server_spans(exporter)
        websocket.send_text("second message")
        assert websocket.receive_text() == "second message"
    (span,) = server_spans(exporter)
    assert span.name == "WS /tenants/{tenant}/api/rooms/{room}"
    assert span.parent.span_id == int("2" * 16, 16)
    assert span.context.trace_id == int("1" * 32, 16)
    assert span.attributes["network.protocol.name"] == "websocket"
    assert span.attributes["url.scheme"] == "ws"
    assert span.status.status_code == StatusCode.UNSET
    assert not any(key.startswith("http.request.") for key in span.attributes)
    assert "http.response.status_code" not in span.attributes
    assert "network.protocol.version" not in span.attributes
    assert reader.get_metrics_data() is None
    assert len(exporter.get_finished_spans()) == (3 if operation_spans else 1)
    assert "private payload" not in repr(exporter.get_finished_spans())
    assert all(get_telemetry_data(saved_context) is None for saved_context in saved)
    assert get_telemetry_data() is None


@pytest.mark.parametrize("code", [1000, 1001, 1006])
def test_client_disconnect(telemetry, logs, code):
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)

    @app.websocket("/ws")
    async def endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.receive_text()

    with pytest.raises(WebSocketDisconnect) as caught:
        with TestClient(app).websocket_connect("/ws") as websocket:
            websocket.close(code=code)
    assert caught.value.code == code
    (server,) = server_spans(exporter)
    assert server.status.status_code == (
        StatusCode.ERROR if code == 1006 else StatusCode.UNSET
    )
    assert len(logs.get_finished_logs()) == int(code == 1006)
    for span in exporter.get_finished_spans():
        assert not span.events
        assert span.status.status_code == (
            StatusCode.ERROR
            if code == 1006 and span.name != "fastapi.dependencies"
            else StatusCode.UNSET
        )
    assert reader.get_metrics_data() is None


@pytest.mark.parametrize("mode", ["sampled", "unsampled", "logs_only", "logs_disabled"])
@pytest.mark.parametrize("stage", ["dependency", "endpoint", "cleanup"])
def test_unexpected_exception(telemetry, logs, mode, stage):
    config, exporter, reader = telemetry
    if mode == "unsampled":
        config["tracer_provider"].sampler = ALWAYS_OFF
    elif mode == "logs_only":
        config["tracing"] = False
    elif mode == "logs_disabled":
        config["logs"] = False
    app = FastAPI(telemetry=config)
    failure = ValueError("websocket failed")
    saved = []

    async def dependency():
        saved.append(context.get_current())
        if stage == "dependency":
            raise failure
        yield
        if stage == "cleanup":
            raise failure

    @app.websocket("/ws", dependencies=[Depends(dependency)])
    async def endpoint(websocket: WebSocket):
        await websocket.accept()
        if stage == "endpoint":
            raise failure
        await websocket.close()

    with pytest.raises(ValueError, match="websocket failed"):
        with TestClient(app).websocket_connect("/ws"):
            pass  # pragma: no cover
    records = logs.get_finished_logs()
    assert len(records) == int(mode != "logs_disabled")
    if records:
        record = records[0].log_record
        assert record.event_name == "fastapi.websocket.exception"
        assert record.timestamp is not None
        assert record.timestamp <= record.observed_timestamp
        assert record.exception is failure
        assert record.severity_number == SeverityNumber.ERROR
        assert record.body == "Unhandled exception in FastAPI WebSocket connection"
        assert record.attributes["http.route"] == "/ws"
        assert bool(record.trace_id) == (mode != "logs_only")
        assert get_telemetry_data(record.context) is None
    if mode in ("sampled", "logs_disabled"):
        (server,) = server_spans(exporter)
        assert server.status.status_code == StatusCode.ERROR
        assert server.attributes["error.type"] == "ValueError"
        if records:
            assert records[0].log_record.span_id == server.context.span_id
    else:
        assert not exporter.get_finished_spans()
    assert reader.get_metrics_data() is None
    assert all(get_telemetry_data(saved_context) is None for saved_context in saved)


@pytest.mark.parametrize("tracing", [False, True])
def test_validation_data(telemetry, logs, tracing):
    config, exporter, reader = telemetry
    config["tracing"] = tracing
    app = FastAPI(telemetry=config)
    observed = []

    class Observe(LogRecordProcessor):
        def on_emit(self, log_record):
            data = get_telemetry_data(log_record.log_record.context)
            assert data is not None
            assert data.websocket is not None
            assert data.request is None
            assert data.body is None
            assert data.errors is not None
            assert data.errors[0]["input"] == "private-invalid-input"
            observed.append(log_record.log_record.context)

        def shutdown(self):
            pass

        def force_flush(self, timeout_millis=30000):
            return True

    config["logger_provider"].add_log_record_processor(Observe())

    @app.websocket("/ws/{value}")
    async def endpoint(*, websocket: WebSocket, value: int):
        pytest.fail(
            "Validation should fail before the endpoint runs"
        )  # pragma: no cover

    with pytest.raises(WebSocketDisconnect) as caught:
        with TestClient(app).websocket_connect("/ws/private-invalid-input"):
            pass  # pragma: no cover
    assert caught.value.code == 1008
    assert config["logger_provider"].force_flush()
    (record,) = logs.get_finished_logs()
    assert record.log_record.event_name == "fastapi.validation.failed"
    assert record.log_record.severity_number == SeverityNumber.WARN
    assert record.log_record.attributes == {
        "http.route": "/ws/{value}",
        "fastapi.validation.error_count": 1,
    }
    assert record.log_record.exception is None
    assert "private-invalid-input" not in repr(record.log_record.attributes)
    assert len(observed) == 1
    assert get_telemetry_data(observed[0]) is None
    if tracing:
        assert all(
            span.status.status_code == StatusCode.UNSET
            for span in exporter.get_finished_spans()
        )
    assert reader.get_metrics_data() is None


@pytest.mark.parametrize("excluded", [False, True])
def test_disabled_and_excluded_connections(telemetry, logs, excluded):
    config, exporter, reader = telemetry
    if excluded:
        config["exclude"] = lambda scope: scope["type"] == "websocket"
    else:
        config.update(tracing=False, logs=False)
    app = FastAPI(telemetry=config)
    child = FastAPI(telemetry=config)
    app.mount("/child", child)

    @child.websocket("/ws")
    async def endpoint(websocket: WebSocket):
        assert get_telemetry_data() is None
        await websocket.accept()
        await websocket.close()

    with TestClient(app).websocket_connect("/child/ws"):
        pass
    assert not exporter.get_finished_spans()
    assert not logs.get_finished_logs()
    assert reader.get_metrics_data() is None


def test_handled_websocket_exception(telemetry, logs):
    config, exporter, _ = telemetry
    app = FastAPI(telemetry=config)

    @app.websocket("/ws")
    async def endpoint(websocket: WebSocket):
        raise WebSocketException(code=1008)

    with pytest.raises(WebSocketDisconnect) as caught:
        with TestClient(app).websocket_connect("/ws"):
            pass  # pragma: no cover
    assert caught.value.code == 1008
    assert len(server_spans(exporter)) == 1
    assert not logs.get_finished_logs()
    assert all(
        span.status.status_code == StatusCode.UNSET
        for span in exporter.get_finished_spans()
    )


def test_concurrent_connections_keep_local_data_separate(telemetry):
    config, exporter, _ = telemetry
    app = FastAPI(telemetry=config)
    saved = []
    observed = []

    @app.websocket("/ws/{name}")
    async def endpoint(*, websocket: WebSocket, name: str):
        data = get_telemetry_data()
        assert data is not None
        await websocket.accept()
        await websocket.receive_text()
        assert get_telemetry_data() is data
        assert data.values is not None
        assert data.values["name"] == name
        assert data.websocket is websocket
        saved.append(context.get_current())
        observed.append(data)
        await websocket.send_text(name)
        await websocket.close()

    with TestClient(app) as client:
        with client.websocket_connect("/ws/first") as first:
            with client.websocket_connect("/ws/second") as second:
                second.send_text("go")
                assert second.receive_text() == "second"
                first.send_text("go")
                assert first.receive_text() == "first"
    assert observed[0] is not observed[1]
    assert len(server_spans(exporter)) == 2
    assert all(get_telemetry_data(saved_context) is None for saved_context in saved)
