"""Environment export remains active alongside independently configured SDKs."""

import pytest

from ._otlp import otlp_collector
from ._subprocess import run_in_subprocess


@pytest.mark.parametrize(
    "mode",
    [
        "global",
        "explicit",
        "sentry-first",
        "fastapi-first",
        "sentry-classic",
        "logfire",
        "logfire-opt-out",
    ],
)
@run_in_subprocess
def test_environment_export_with_existing_integrations(mode):
    import os

    from fastapi import FastAPI
    from fastapi.telemetry import TelemetryConfig, _runtime
    from fastapi.testclient import TestClient
    from opentelemetry import _logs, metrics, trace
    from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import (
        ExportLogsServiceRequest,
    )
    from opentelemetry.proto.collector.metrics.v1.metrics_service_pb2 import (
        ExportMetricsServiceRequest,
    )
    from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
        ExportTraceServiceRequest,
    )
    from opentelemetry.proto.trace.v1.trace_pb2 import Span
    from opentelemetry.sdk._logs import LoggerProvider
    from opentelemetry.sdk._logs.export import (
        InMemoryLogRecordExporter,
        SimpleLogRecordProcessor,
    )
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import InMemoryMetricReader
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    with otlp_collector() as (base, received):
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = base + "/environment"
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = "x-cloud=preserved"
        os.environ["OTEL_BSP_SCHEDULE_DELAY"] = "60000"
        os.environ["OTEL_BLRP_SCHEDULE_DELAY"] = "60000"
        os.environ["OTEL_METRIC_EXPORT_INTERVAL"] = "60000"
        settings: TelemetryConfig = {}
        original_spans = InMemorySpanExporter()
        original_logs = InMemoryLogRecordExporter()
        original_metrics = InMemoryMetricReader()
        if mode in ("global", "explicit"):
            tp = TracerProvider(shutdown_on_exit=False)
            tp.add_span_processor(SimpleSpanProcessor(original_spans))
            mp = MeterProvider(
                metric_readers=[original_metrics], shutdown_on_exit=False
            )
            lp = LoggerProvider(shutdown_on_exit=False)
            lp.add_log_record_processor(SimpleLogRecordProcessor(original_logs))
            if mode == "global":
                trace.set_tracer_provider(tp)
                metrics.set_meter_provider(mp)
                _logs.set_logger_provider(lp)
            else:
                settings = {
                    "tracer_provider": tp,
                    "meter_provider": mp,
                    "logger_provider": lp,
                }
        elif mode.startswith("logfire"):
            import logfire

            logfire.configure(
                send_to_logfire=False,
                console=False,
                additional_span_processors=[SimpleSpanProcessor(original_spans)],
                metrics=logfire.MetricsOptions(additional_readers=[original_metrics]),
                advanced=logfire.AdvancedOptions(
                    log_record_processors=[SimpleLogRecordProcessor(original_logs)]
                ),
            )
            settings["auto_configure"] = mode != "logfire-opt-out"
        else:
            import sentry_sdk
            from sentry_sdk.integrations.fastapi import FastApiIntegration
            from sentry_sdk.integrations.otlp import OTLPIntegration
            from sentry_sdk.integrations.starlette import StarletteIntegration
            from sentry_sdk.transport import Transport

            items = []

            class LocalTransport(Transport):
                def capture_envelope(self, envelope):
                    items.extend(item.type for item in envelope.items)

            if mode == "fastapi-first":
                with TestClient(FastAPI()):
                    pass
            integrations = (
                [StarletteIntegration(), FastApiIntegration()]
                if mode == "sentry-classic"
                else [
                    OTLPIntegration(
                        collector_url=base + "/sentry/traces", setup_propagator=False
                    )
                ]
            )
            sentry_sdk.init(
                dsn="https://public@example.invalid/1",
                transport=LocalTransport,
                default_integrations=False,
                auto_enabling_integrations=False,
                integrations=integrations,
                traces_sample_rate=1.0,
                send_client_reports=False,
            )

        app = FastAPI(telemetry=settings)

        @app.get("/items/{item_id}")
        def endpoint(item_id: int):
            raise ValueError("environment export")

        try:
            for _ in range(2):
                with TestClient(app, raise_server_exceptions=False) as client:
                    assert client.get("/items/1").status_code == 500
            if mode.startswith("logfire"):
                logfire.force_flush()
            elif mode.startswith("sentry") or mode == "fastapi-first":
                tracer_provider = trace.get_tracer_provider()
                assert isinstance(tracer_provider, TracerProvider)
                tracer_provider.force_flush()
                sentry_sdk.flush()

            def spans_at(path):
                requests = [
                    ExportTraceServiceRequest.FromString(body)
                    for url, body, _ in received
                    if url == path
                ]
                return [
                    span
                    for request in requests
                    for resource in request.resource_spans
                    for scope in resource.scope_spans
                    for span in scope.spans
                ]

            environment_spans = spans_at("/environment/v1/traces")
            multiplier = 2 if mode == "logfire" else 1
            servers = [
                span for span in environment_spans if span.kind == Span.SPAN_KIND_SERVER
            ]
            assert len(servers) == 2 * multiplier, (mode, len(servers))
            assert len({span.span_id for span in servers}) == 2
            assert all(span.name == "GET /items/{item_id}" for span in servers)
            if mode in ("global", "explicit"):
                assert sorted(
                    (span.context.trace_id, span.context.span_id, span.name)
                    for span in original_spans.get_finished_spans()
                ) == sorted(
                    (
                        int.from_bytes(span.trace_id, "big"),
                        int.from_bytes(span.span_id, "big"),
                        span.name,
                    )
                    for span in environment_spans
                )
            if mode in ("sentry-first", "fastapi-first"):
                sentry_spans = spans_at("/sentry/traces")
                assert {span.span_id for span in sentry_spans} == {
                    span.span_id for span in environment_spans
                }
            if mode == "sentry-classic":
                assert items.count("event") == 2, items
                assert items.count("transaction") == 2, items

            log_requests = [
                ExportLogsServiceRequest.FromString(body)
                for url, body, _ in received
                if url == "/environment/v1/logs"
            ]
            logs = [
                record
                for request in log_requests
                for resource in request.resource_logs
                for scope in resource.scope_logs
                for record in scope.log_records
            ]
            assert len(logs) == 2 * multiplier, (mode, len(logs))
            assert all(
                record.trace_id in {span.trace_id for span in servers}
                for record in logs
            )
            metric_requests = [
                ExportMetricsServiceRequest.FromString(body)
                for url, body, _ in received
                if url == "/environment/v1/metrics"
            ]
            counts = [
                point.count
                for request in metric_requests
                for resource in request.resource_metrics
                for scope in resource.scope_metrics
                for metric in scope.metrics
                if metric.name == "http.server.request.duration"
                for point in getattr(metric, metric.WhichOneof("data")).data_points
            ]
            assert counts and counts[-1] == 2, counts
            assert all(
                headers.get("x-cloud") == "preserved"
                for url, _, headers in received
                if url.startswith("/environment/")
            )
            assert len(_runtime._configured) == (0 if mode == "logfire-opt-out" else 3)
            _runtime._shutdown()
            if mode in ("global", "explicit"):
                # FastAPI's cleanup closes its own exporters, leaving the provider and
                # previously installed vendor components usable.
                count = len(original_spans.get_finished_spans())
                with tp.get_tracer("vendor").start_as_current_span("still-running"):
                    pass
                assert len(original_spans.get_finished_spans()) == count + 1
                lp.get_logger("vendor").emit(body="still-running")
                assert len(original_logs.get_finished_logs()) == 3
                assert original_metrics.get_metrics_data() is not None
                tp.shutdown()
                mp.shutdown()
                lp.shutdown()
        finally:
            _runtime._shutdown()
            if mode.startswith("logfire"):
                logfire.shutdown()
