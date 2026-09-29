import pytest
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.testclient import TestClient
from opentelemetry import trace
from opentelemetry._logs import NoOpLoggerProvider, SeverityNumber
from opentelemetry.sdk.trace.sampling import ALWAYS_OFF

from .conftest import metric_points, server_spans


@pytest.mark.parametrize("sampled", [True, False])
def test_exception_is_logged_once_with_trace_context(telemetry, logs, sampled):
    config, spans, reader = telemetry
    if not sampled:
        config["tracer_provider"].sampler = ALWAYS_OFF
    app = FastAPI(telemetry=config)
    contexts = []
    error = ValueError("test failure")

    @app.get("/items/{item_id}")
    def endpoint(item_id: int):
        contexts.append(trace.get_current_span().get_span_context())
        raise error

    assert (
        TestClient(app, raise_server_exceptions=False).get("/items/1").status_code
        == 500
    )
    (data,) = logs.get_finished_logs()
    record = data.log_record
    assert record.event_name == "http.server.request.exception"
    assert record.timestamp is not None
    assert record.timestamp <= record.observed_timestamp
    assert (
        data.instrumentation_scope.schema_url
        == "https://opentelemetry.io/schemas/1.44.0"
    )
    assert record.exception is error
    assert record.trace_id == contexts[0].trace_id
    assert record.span_id != 0
    if sampled:
        (server,) = server_spans(spans)
        assert record.span_id == server.context.span_id
    assert record.severity_number == SeverityNumber.ERROR
    assert record.attributes["http.route"] == "/items/{item_id}"
    assert record.attributes["exception.type"] == "ValueError"
    assert record.attributes["exception.message"] == "test failure"
    assert "raise error" in record.attributes["exception.stacktrace"]
    assert len(server_spans(spans)) == int(sampled)


@pytest.mark.parametrize("raises", [False, True])
def test_exclusion_applies_to_mounted_apps(telemetry, logs, raises):
    config, spans, reader = telemetry
    scopes = []
    child = FastAPI(telemetry=config)

    @child.get("/{name}")
    def endpoint(*, request: Request, name: str):
        scopes.append(request.scope)
        if name == "excluded" and raises:
            raise ValueError("excluded error")
        return name

    parent = FastAPI(
        telemetry={
            **config,
            "exclude": lambda scope: scope["path"] == "/child/excluded",
        }
    )
    parent.mount("/child", child)
    client = TestClient(parent, raise_server_exceptions=False)
    assert client.get("/child/excluded").status_code == (500 if raises else 200)
    assert not spans.get_finished_spans()
    assert not logs.get_finished_logs()
    assert not metric_points(reader=reader)
    assert "fastapi.telemetry" not in scopes[0]
    assert client.get("/child/included").json() == "included"
    (span,) = server_spans(spans)
    assert span.attributes["http.route"] == "/child/{name}"
    assert metric_points(reader=reader)[0].count == 1


def test_handled_exceptions_and_validation_are_not_error_logs(telemetry, logs):
    config, spans, reader = telemetry
    app = FastAPI(telemetry=config)

    @app.exception_handler(ValueError)
    async def handled(request, exc):
        return JSONResponse({"detail": "handled"}, status_code=400)

    @app.get("/items/{value}")
    def endpoint(value: int):
        if value == 1:
            raise HTTPException(404)
        raise ValueError("handled by application")

    client = TestClient(app)
    assert client.get("/items/no").status_code == 422
    assert client.get("/items/1").status_code == 404
    assert client.get("/items/2").status_code == 400
    assert client.get("/missing").status_code == 404
    (validation,) = logs.get_finished_logs()
    assert validation.log_record.severity_number == SeverityNumber.WARN
    assert validation.log_record.event_name == "fastapi.validation.failed"
    assert validation.log_record.timestamp is not None
    assert validation.log_record.timestamp <= validation.log_record.observed_timestamp
    assert validation.log_record.exception is None


@pytest.mark.parametrize("stage", ["stream", "cleanup"])
def test_errors_after_response_started_are_logged(telemetry, logs, stage):
    from fastapi import Depends

    config, spans, reader = telemetry
    app = FastAPI(telemetry=config)

    def fail():
        raise ValueError("after response started")

    async def dependency():
        yield
        if stage == "cleanup":
            fail()

    @app.get("/", dependencies=[Depends(dependency)])
    async def endpoint():
        if stage == "stream":

            async def stream():
                yield "start"
                fail()

            return StreamingResponse(stream())
        return "ok"

    assert TestClient(app, raise_server_exceptions=False).get("/").status_code == 200
    (data,) = logs.get_finished_logs()
    (span,) = server_spans(spans)
    assert data.log_record.trace_id == span.context.trace_id
    assert (
        "after response started" in data.log_record.attributes["exception.stacktrace"]
    )


@pytest.mark.parametrize("mode", ["logs_only", "disabled", "noop", "excluded"])
def test_independent_log_configuration(telemetry, logs, mode):
    config, spans, reader = telemetry
    if mode == "logs_only":
        config.update(tracing=False, metrics=False)
    elif mode == "disabled":
        config["logs"] = False
    elif mode == "noop":
        config["logger_provider"] = NoOpLoggerProvider()
    else:
        config["exclude"] = lambda scope: True
    app = FastAPI(telemetry=config)

    @app.get("/")
    def endpoint():
        raise ValueError("test")

    assert TestClient(app, raise_server_exceptions=False).get("/").status_code == 500
    records = logs.get_finished_logs()
    assert len(records) == int(mode == "logs_only")
    if records:
        assert records[0].log_record.trace_id == 0


@pytest.mark.parametrize("status", [404, 503])
@pytest.mark.parametrize("sampled", [False, True])
def test_http_exception_records_status_without_exception_telemetry(
    telemetry, logs, status, sampled
):
    from opentelemetry.trace import StatusCode

    config, spans, reader = telemetry
    if not sampled:
        config["tracer_provider"].sampler = ALWAYS_OFF
    app = FastAPI(telemetry=config)

    @app.get("/items/{item_id}")
    def endpoint(item_id: int):
        raise HTTPException(status, "private exception detail")

    response = TestClient(app).get("/items/1")
    assert response.status_code == status
    assert response.json() == {"detail": "private exception detail"}
    assert not logs.get_finished_logs()
    (point,) = metric_points(reader=reader)
    assert point.count == 1
    assert point.attributes["http.response.status_code"] == status
    assert point.attributes["http.route"] == "/items/{item_id}"
    assert point.attributes.get("error.type") == ("503" if status == 503 else None)
    finished = spans.get_finished_spans()
    assert all(not span.events for span in finished)
    if sampled:
        (server,) = server_spans(spans)
        assert server.attributes["http.response.status_code"] == status
        assert server.status.status_code == (
            StatusCode.ERROR if status == 503 else StatusCode.UNSET
        )
    else:
        assert not finished


def test_exception_handler_failure_is_logged_once_as_unhandled(telemetry, logs):
    config, _, _ = telemetry
    failure = RuntimeError("handler failed")
    app = FastAPI(telemetry=config)

    @app.exception_handler(HTTPException)
    async def handler(request, exc):
        raise failure

    @app.get("/")
    async def endpoint():
        raise HTTPException(404, "original")

    assert TestClient(app, raise_server_exceptions=False).get("/").status_code == 500
    (data,) = logs.get_finished_logs()
    assert data.log_record.exception is failure
    assert data.log_record.body == "Unhandled exception in FastAPI request"


class ApplicationError(Exception):
    pass


def test_exception_type_matches_spans_metrics_and_logs(telemetry, logs):
    config, spans, reader = telemetry
    app = FastAPI(telemetry=config)

    @app.get("/")
    async def endpoint():
        raise ApplicationError("failed")

    assert TestClient(app, raise_server_exceptions=False).get("/").status_code == 500
    (record,) = logs.get_finished_logs()
    expected = f"{__name__}.ApplicationError"
    assert record.log_record.attributes["exception.type"] == expected
    failed_spans = [
        span for span in spans.get_finished_spans() if span.status.is_ok is False
    ]
    assert {span.name for span in failed_spans} == {"GET /", "fastapi.endpoint"}
    assert all(span.attributes["error.type"] == expected for span in failed_spans)
    (point,) = metric_points(reader=reader)
    assert point.attributes["error.type"] == expected
