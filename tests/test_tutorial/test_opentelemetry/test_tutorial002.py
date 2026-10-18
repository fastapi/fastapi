import json
from io import StringIO

from fastapi.testclient import TestClient


def test_console_provider_example(monkeypatch):
    from opentelemetry.sdk.trace import export

    output = StringIO()
    exporter = export.ConsoleSpanExporter(
        out=output, formatter=lambda span: span.to_json(indent=None) + "\n"
    )
    monkeypatch.setattr(export, "ConsoleSpanExporter", lambda: exporter)
    from docs_src.opentelemetry.tutorial002_py310 import app, tracer_provider

    try:
        with TestClient(app) as client:
            assert client.get("/items/2").json() == {"item_id": 2}
        assert tracer_provider.force_flush()
        spans = [json.loads(line) for line in output.getvalue().splitlines()]
        assert len(spans) == 4
        span = next(span for span in spans if span["kind"] == "SpanKind.SERVER")
        assert span["name"] == "GET /items/{item_id}"
        assert span["kind"] == "SpanKind.SERVER"
        assert span["attributes"]["http.route"] == "/items/{item_id}"
    finally:
        tracer_provider.shutdown()
