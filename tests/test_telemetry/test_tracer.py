import warnings
from unittest.mock import Mock

import pytest
from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from .conftest import server_spans


@pytest.mark.parametrize("global_provider", [False, True])
@pytest.mark.parametrize("protocol", ["http", "websocket"])
def test_tracer_lookup_preserves_warning_deduplication(
    telemetry, monkeypatch, global_provider, protocol
):
    config, exporter, _ = telemetry
    provider = config["tracer_provider"]
    get_tracer = Mock(wraps=provider.get_tracer)
    monkeypatch.setattr(provider, "get_tracer", get_tracer)
    if global_provider:
        monkeypatch.setattr(trace, "get_tracer_provider", lambda: provider)
        config["tracer_provider"] = None
    app = FastAPI(telemetry=config)

    @app.get("/")
    def endpoint():
        warnings.warn("Repeated endpoint warning", UserWarning, stacklevel=1)
        return "ok"

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        warnings.warn("Repeated endpoint warning", UserWarning, stacklevel=1)
        await websocket.close()

    get_tracer.assert_not_called()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("default")
        with TestClient(app) as client:
            for _ in range(5):
                if protocol == "http":
                    assert client.get("/").json() == "ok"
                else:
                    with client.websocket_connect("/ws") as websocket:
                        assert websocket.receive()["type"] == "websocket.close"
    assert [str(warning.message) for warning in caught] == ["Repeated endpoint warning"]
    get_tracer.assert_called_once()
    spans = server_spans(exporter)
    assert len(spans) == 5
    assert len({span.context.trace_id for span in spans}) == 5


def test_cached_tracer_follows_provider_changes(telemetry, monkeypatch):
    config, exporter, _ = telemetry
    provider = config["tracer_provider"]
    monkeypatch.setattr(trace, "get_tracer_provider", lambda: provider)
    app = FastAPI()
    client = TestClient(app)
    for _ in range(2):
        assert client.get("/").status_code == 404
    assert len(server_spans(exporter)) == 2

    other_exporter = InMemorySpanExporter()
    other_provider = TracerProvider(shutdown_on_exit=False)
    other_provider.add_span_processor(SimpleSpanProcessor(other_exporter))
    monkeypatch.setattr(trace, "get_tracer_provider", lambda: other_provider)
    try:
        for _ in range(2):
            assert client.get("/").status_code == 404
        assert len(server_spans(other_exporter)) == 2
        assert len(server_spans(exporter)) == 2
    finally:
        other_provider.shutdown()
