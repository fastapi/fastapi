import threading
from typing import Annotated

import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from opentelemetry import baggage, trace
from opentelemetry.sdk.trace import SpanProcessor
from opentelemetry.trace import SpanKind, StatusCode


@pytest.mark.parametrize("sync", [False, True])
def test_native_operations_and_worker_context(telemetry, sync):
    config, exporter, reader = telemetry
    started = {}
    executed = {}

    class Processor(SpanProcessor):
        def on_start(self, span, parent_context=None):
            started[span.name] = (threading.get_ident(), span.get_span_context())

    config["tracer_provider"].add_span_processor(Processor())
    app = FastAPI(telemetry=config)

    def dependency():
        executed["dependency"] = trace.get_current_span().get_span_context()
        return "private argument"

    def implementation(value: Annotated[str, Depends(dependency)]):
        executed["endpoint"] = (
            threading.get_ident(),
            trace.get_current_span().get_span_context(),
        )
        assert value == "private argument"
        return baggage.get_baggage("example")

    async def async_endpoint(value: Annotated[str, Depends(dependency)]):
        return implementation(value)

    app.get("/")(implementation if sync else async_endpoint)
    assert (
        TestClient(app).get("/", headers={"baggage": "example=value"}).json() == "value"
    )
    assert started["fastapi.endpoint"] == executed["endpoint"]
    assert started["fastapi.dependencies"][1] == executed["dependency"]
    assert (
        started["fastapi.endpoint"][0] != started["fastapi.dependencies"][0]
    ) == sync
    spans = exporter.get_finished_spans()
    server = next(s for s in spans if s.kind == SpanKind.SERVER)
    children = [s for s in spans if s is not server]
    assert {s.name for s in children} == {
        "fastapi.dependencies",
        "fastapi.endpoint",
        "fastapi.serialization",
    }
    assert all(s.parent.span_id == server.context.span_id for s in children)
    assert all(s.context.trace_id == server.context.trace_id for s in children)
    assert all("code.function.name" in s.attributes for s in children)
    assert "private argument" not in repr([s.attributes for s in spans])
    assert baggage.get_baggage("example") is None
    assert not trace.get_current_span().get_span_context().is_valid


@pytest.mark.parametrize(
    "failure", ["dependency", "endpoint", "serialization", "handled"]
)
def test_operation_errors(telemetry, failure):
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)

    async def dependency():
        if failure == "dependency":
            raise ValueError("dependency failure")

    @app.get("/", dependencies=[Depends(dependency)], response_model=int)
    async def endpoint():
        if failure == "endpoint":
            raise ValueError("endpoint failure")
        if failure == "handled":
            raise HTTPException(400)
        return "not an integer"

    response = TestClient(app, raise_server_exceptions=False).get("/")
    assert response.status_code == (400 if failure == "handled" else 500)
    spans = exporter.get_finished_spans()
    if failure == "handled":
        assert all(s.status.status_code == StatusCode.UNSET for s in spans)
    else:
        name = "dependencies" if failure == "dependency" else failure
        failed = next(s for s in spans if s.name == f"fastapi.{name}")
        assert failed.status.status_code == StatusCode.ERROR
    assert all(not s.events for s in spans)
