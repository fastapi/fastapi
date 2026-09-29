import threading
from functools import partial

import anyio
import pytest
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.telemetry import get_telemetry_data
from fastapi.testclient import TestClient
from opentelemetry import trace
from opentelemetry.sdk.trace import Span
from opentelemetry.sdk.trace.sampling import ALWAYS_OFF
from opentelemetry.trace import SpanKind, StatusCode
from starlette.background import BackgroundTask

from ._subprocess import run_in_subprocess
from .conftest import metric_points, server_spans


@pytest.mark.parametrize("backend", ["asyncio", "trio"])
@pytest.mark.parametrize("sync", [False, True])
def test_background_task_spans(telemetry, backend, sync):
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)
    executed = []
    endpoint_thread = []

    def execute(number, *, value):
        span = trace.get_current_span()
        assert isinstance(span, Span)
        assert span.is_recording()
        assert span.name == "fastapi.background_task"
        data = get_telemetry_data()
        assert data is not None
        assert data.request is not None
        assert data.request.url.path == "/items/42"
        assert len(server_spans(exporter)) == 1
        executed.append((number, value, threading.get_ident(), span.get_span_context()))

    async def async_task(number, *, value):
        execute(number, value=value)

    task = execute if sync else async_task

    async def dependency(background: BackgroundTasks):
        background.add_task(task, 1, value="private dependency value")

    @app.get("/items/{item_id}", dependencies=[Depends(dependency)])
    async def endpoint(background: BackgroundTasks, item_id: int):
        endpoint_thread.append(threading.get_ident())
        background.add_task(task, 2, value="private endpoint value")
        return {"item_id": item_id}

    assert TestClient(app, backend=backend).get("/items/42").json() == {"item_id": 42}
    assert [(number, value) for number, value, _, _ in executed] == [
        (1, "private dependency value"),
        (2, "private endpoint value"),
    ]
    spans = exporter.get_finished_spans()
    (server,) = server_spans(exporter)
    tasks = [span for span in spans if span.name == "fastapi.background_task"]
    assert len(tasks) == 2
    for span, (_, _, thread_id, context) in zip(tasks, executed, strict=True):
        assert span.kind == SpanKind.INTERNAL
        assert span.parent.span_id == server.context.span_id
        assert context.trace_id == server.context.trace_id
        assert context.span_id == span.context.span_id
        assert span.start_time >= server.end_time
        assert span.status.status_code == StatusCode.UNSET
        assert span.attributes == {
            "code.function.name": f"{task.__module__}.{task.__qualname__}"
        }
        assert (thread_id != endpoint_thread[0]) == sync
    assert metric_points(reader=reader)[0].count == 1
    assert get_telemetry_data() is None


def test_background_task_objects(telemetry):
    config, exporter, _ = telemetry
    app = FastAPI(telemetry=config)
    executed = []

    def record(value):
        span = trace.get_current_span()
        assert isinstance(span, Span)
        executed.append((value, span.name))

    class AsyncTask:
        async def __call__(self, *, value):
            record(value)

    class CustomTask(BackgroundTask):
        async def __call__(self):
            record("before")
            await super().__call__()
            record("after")

    original = CustomTask(record, "custom")
    background = BackgroundTasks([original])
    background.add_task(partial(record, "partial"))
    background.add_task(AsyncTask(), value="async callable")

    @app.get("/")
    async def endpoint():
        return JSONResponse("ok", background=background)

    assert TestClient(app).get("/").json() == "ok"
    assert background.tasks[0] is original
    assert executed == [
        (value, "fastapi.background_task")
        for value in ("before", "custom", "after", "partial", "async callable")
    ]
    assert (
        len(
            [
                s
                for s in exporter.get_finished_spans()
                if s.name == "fastapi.background_task"
            ]
        )
        == 3
    )


@pytest.mark.parametrize("sync", [False, True])
@pytest.mark.parametrize("http_error", [False, True])
def test_background_task_failure(telemetry, logs, sync, http_error):
    config, exporter, _ = telemetry
    app = FastAPI(telemetry=config)
    error = HTTPException(503) if http_error else ValueError("background failure")
    executed = []

    def fail():
        executed.append("first")
        raise error

    async def async_fail():
        fail()

    @app.get("/")
    async def endpoint(background: BackgroundTasks):
        background.add_task(fail if sync else async_fail)
        background.add_task(executed.append, "second")
        return "ok"

    assert TestClient(app, raise_server_exceptions=False).get("/").status_code == 200
    assert executed == ["first"]
    (task,) = [
        s for s in exporter.get_finished_spans() if s.name == "fastapi.background_task"
    ]
    assert task.status.status_code == StatusCode.ERROR
    assert task.attributes["error.type"] == (
        "fastapi.exceptions.HTTPException" if http_error else "ValueError"
    )
    assert not task.events
    (server,) = server_spans(exporter)
    assert server.attributes["http.response.status_code"] == 200
    assert server.status.status_code == StatusCode.UNSET
    (record,) = logs.get_finished_logs()
    assert (
        record.log_record.trace_id == task.context.trace_id == server.context.trace_id
    )
    assert "raise error" in record.log_record.attributes["exception.stacktrace"]
    assert record.log_record.exception is not None
    if http_error:
        assert record.log_record.exception.__cause__ is error
    else:
        assert record.log_record.exception is error


@pytest.mark.parametrize(
    "mode", ["operations_disabled", "tracing_disabled", "excluded", "unsampled"]
)
def test_background_task_settings(telemetry, mode):
    config, exporter, _ = telemetry
    if mode == "operations_disabled":
        config["operation_spans"] = False
    elif mode == "tracing_disabled":
        config["tracing"] = False
    elif mode == "excluded":
        config["exclude"] = lambda scope: True
    else:
        config["tracer_provider"].sampler = ALWAYS_OFF
    app = FastAPI(telemetry=config)
    executed = []

    @app.get("/")
    async def endpoint(background: BackgroundTasks):
        background.add_task(executed.append, "done")
        return "ok"

    assert TestClient(app).get("/").json() == "ok"
    assert executed == ["done"]
    assert not any(
        s.name == "fastapi.background_task" for s in exporter.get_finished_spans()
    )


def test_background_tasks_outside_request():
    executed = []
    background = BackgroundTasks()
    background.add_task(executed.append, "done")
    anyio.run(background)
    assert executed == ["done"]
    assert get_telemetry_data() is None


@pytest.mark.parametrize("integration", ["contrib", "logfire", "native_logfire"])
@run_in_subprocess
def test_background_task_integrations(integration):
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    native = InMemorySpanExporter()
    legacy = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(native))
    app = FastAPI(
        telemetry={
            "tracer_provider": None if integration == "native_logfire" else provider
        }
    )
    executed = []

    def sync_task():
        executed.append(trace.get_current_span().get_span_context())

    async def async_task():
        executed.append(trace.get_current_span().get_span_context())

    @app.get("/")
    async def endpoint(background: BackgroundTasks):
        background.add_task(sync_task)
        background.add_task(async_task)
        return "ok"

    if integration == "contrib":
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        legacy_provider = TracerProvider()
        legacy_provider.add_span_processor(SimpleSpanProcessor(legacy))
        FastAPIInstrumentor.instrument_app(app, tracer_provider=legacy_provider)
    else:
        import logfire

        logfire.configure(
            send_to_logfire=False,
            console=False,
            metrics=False,
            additional_span_processors=[SimpleSpanProcessor(legacy)],
        )
        if integration == "logfire":
            logfire.instrument_fastapi(app)
    assert TestClient(app).get("/").json() == "ok"
    assert not native.get_finished_spans()
    tasks = [
        span
        for span in legacy.get_finished_spans()
        if (
            span.name.startswith("BackgroundTask ")
            or span.name == "fastapi.background_task"
        )
        and not (
            span.attributes
            and span.attributes.get("logfire.span_type") == "pending_span"
        )
    ]
    assert [span.name for span in tasks] == (
        ["fastapi.background_task", "fastapi.background_task"]
        if integration == "native_logfire"
        else ["BackgroundTask sync_task", "BackgroundTask async_task"]
    )
    assert [span.context for span in tasks] == executed
