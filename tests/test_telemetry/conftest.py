import os

import pytest
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import (
    InMemoryLogRecordExporter,
    SimpleLogRecordProcessor,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    remove_export_environment(monkeypatch)


def remove_export_environment(monkeypatch):
    for name in os.environ:
        if name.startswith(("OTEL_", "LOGFIRE_", "SENTRY_")):
            monkeypatch.delenv(name)


@pytest.fixture
def telemetry():
    exporter = InMemorySpanExporter()
    tracer = TracerProvider(shutdown_on_exit=False)
    tracer.add_span_processor(SimpleSpanProcessor(exporter))
    reader = InMemoryMetricReader()
    meter = MeterProvider(metric_readers=[reader], shutdown_on_exit=False)
    yield {"tracer_provider": tracer, "meter_provider": meter}, exporter, reader
    tracer.shutdown()
    meter.shutdown()


@pytest.fixture
def logs(telemetry):
    config, _, _ = telemetry
    exporter = InMemoryLogRecordExporter()
    provider = LoggerProvider(shutdown_on_exit=False)
    provider.add_log_record_processor(SimpleLogRecordProcessor(exporter))
    config["logger_provider"] = provider
    yield exporter
    provider.shutdown()


def metric_points(*, reader, name="http.server.request.duration"):
    data = reader.get_metrics_data()
    if data is None:
        return []
    return [
        point
        for resource in data.resource_metrics
        for scope in resource.scope_metrics
        for metric in scope.metrics
        if metric.name == name
        for point in metric.data.data_points
    ]


def server_spans(exporter):
    from opentelemetry.trace import SpanKind

    return [
        span for span in exporter.get_finished_spans() if span.kind == SpanKind.SERVER
    ]
