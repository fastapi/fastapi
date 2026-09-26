# OpenTelemetry { #opentelemetry }

When your API is running, you might want to know how much traffic it receives, which requests are slow, and when errors happen.

**Telemetry** is data about your application's behavior that helps you answer these questions. Common types include:

- **Metrics**: measurements you can summarize over time, such as response times and the number of requests being handled.
- **Traces**: records of individual requests and the operations performed to handle them. Each timed operation is called a **span**.
- **Logs**: timestamped records of events, such as an application starting or an operation failing.

[**OpenTelemetry**](https://opentelemetry.io/) is a set of standards and tools for collecting telemetry and sending it to a monitoring service, where you can explore it in dashboards.

**FastAPI provides OpenTelemetry support by default** for HTTP request traces, metrics, and logs. WebSocket connections also provide traces and logs. To see that data, configure a monitoring service to receive it.

## Install FastAPI { #install-fastapi }

Install FastAPI with the `standard` extras, which include the packages for sending telemetry:

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## Create the app { #create-the-app }

Create a file `main.py`:

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

## Choose where to send telemetry { #choose-where-to-send-telemetry }

/// tip

When you deploy to [FastAPI Cloud](https://fastapicloud.com) with `fastapi[standard]`, metrics work automatically. You don't have to configure anything else. You can view request counts and response times in the [Metrics dashboard](https://fastapicloud.com/docs/monitoring-and-performance/metrics/) on Pro plans.

///

Your monitoring service will provide an endpoint that accepts **OTLP**, the OpenTelemetry protocol for sending telemetry. Use its HTTP/protobuf base endpoint.

Set these environment variables, replacing the example URL with your endpoint:

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` identifies your app in the monitoring service. The endpoint is the base URL for receiving data. Traces are sent to `/v1/traces`, metrics to `/v1/metrics`, and logs to `/v1/logs` under that URL.

If your service requires authentication, set `OTEL_EXPORTER_OTLP_HEADERS` to the headers it specifies, for example `api-key=YOUR_API_KEY`.

## Run the app { #run-the-app }

Start the app in the same terminal:

<div class="termy">

```console
$ uv run fastapi run
```

</div>

In another terminal, send a request:

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

Open your monitoring service and find `my-api`. After the next export, you can see a trace with a `GET /items/{item_id}` span, along with metrics for request counts, response duration, and active requests.

## Customize telemetry { #customize-telemetry }

### Configure providers and exporters { #configure-providers-and-exporters }

A **provider** supplies the objects that record traces, metrics, or logs. Its configuration controls how that data is processed and exported.

Telemetry libraries can configure OpenTelemetry's global providers. Configure the library before the app starts, and FastAPI uses those providers automatically.

When an OTLP endpoint is set in the environment, FastAPI adds an exporter for that destination to each enabled provider. Existing exporters continue sending data to their destinations.

Configure each destination once. If another library already handles the environment destination, disable its environment export or turn off FastAPI's automatic setup:

```python
app = FastAPI(telemetry={"auto_configure": False})
```

You can also pass a provider directly in the `telemetry` dictionary. For example, this provider uses OpenTelemetry's console exporter to print request spans in your terminal:

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

The **exporter** sends the spans to their destination. `BatchSpanProcessor` groups spans and sends them in the background. Replace the console exporter with one supplied by your monitoring library to use its destination. See [OpenTelemetry's Python instrumentation guide](https://opentelemetry.io/docs/languages/python/instrumentation/) for more configuration options.

Use `meter_provider` or `logger_provider` in the same dictionary to supply a metrics or logs provider. The application or library creating a provider manages its shutdown. FastAPI manages the export components it adds.

/// warning

OpenTelemetry uses global providers by default. Independent telemetry configuration for [mounted sub-applications](sub-applications.md) is not guaranteed.

///

### Trace request operations { #trace-request-operations }

By default, request traces include spans for resolving dependencies, running your path operation function, serializing the response, and running each task in FastAPI's `BackgroundTasks`. These spans use the same provider and exporters.

Background task spans remain part of the request's trace. They run after the HTTP response span ends, so they do not increase the measured response time.

To record only the HTTP request span, set `operation_spans` to `False`:

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### Trace WebSocket connections { #trace-websocket-connections }

Each WebSocket connection has a span such as `WS /ws/{room}`, covering the handler and dependency cleanup. It uses the same providers and settings, including `operation_spans` for dependency resolution and endpoint execution.

HTTP request metrics cover HTTP requests only. Normal WebSocket disconnects with codes `1000` or `1001` do not produce error logs.

### Inspect errors { #inspect-errors }

FastAPI records unhandled exceptions as OpenTelemetry logs, linked to the request's or connection's trace. Error logs are recorded even when the trace is not sampled.

Exception logs include the exception's type, message, and stack trace. Messages and stack traces can contain sensitive information. Use your provider's log processors to filter or redact them, or set `logs` to `False` to disable these logs.

FastAPI also records request validation failures as warning logs with the route and error count. These logs do not include the invalid input.

## Choose what to record { #choose-what-to-record }

The `telemetry` dictionary also accepts these settings:

| Setting | Purpose | Default |
| --- | --- | --- |
| `tracing` | Record HTTP request and WebSocket connection spans | `True` |
| `metrics` | Record HTTP request metrics | `True` |
| `logs` | Record validation failures and unhandled exceptions | `True` |
| `operation_spans` | Add spans for request operations | `True` |
| `exclude` | Skip requests when a function receiving the ASGI scope returns `True` | `None` |
| `auto_configure` | Add exporters for endpoints set in environment variables | `True` |

For example, to collect metrics while excluding health checks:

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

Set `auto_configure` to `False` when your application handles provider setup itself, such as inside its lifespan function.
