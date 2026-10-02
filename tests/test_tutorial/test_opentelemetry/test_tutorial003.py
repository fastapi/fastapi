from fastapi.testclient import TestClient
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter


def test_disable_operation_spans_example(monkeypatch):
    exporter = InMemorySpanExporter()
    provider = TracerProvider(shutdown_on_exit=False)
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    monkeypatch.setattr(trace, "get_tracer_provider", lambda: provider)
    from docs_src.opentelemetry.tutorial003_py310 import app

    try:
        with TestClient(app) as client:
            assert client.get("/items/3").json() == {"item_id": 3}
        (span,) = exporter.get_finished_spans()
        assert span.kind == trace.SpanKind.SERVER
        assert span.name == "GET /items/{item_id}"
    finally:
        provider.shutdown()
