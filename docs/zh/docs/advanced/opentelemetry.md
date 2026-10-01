# OpenTelemetry { #opentelemetry }

当你的 API 正在运行时，你可能想知道它接收了多少流量、哪些请求很慢，以及何时发生了错误。

**遥测**是关于你的应用程序行为的数据，可帮助你回答这些问题。常见类型包括：

- **指标**：可以随时间汇总的度量，例如响应时间和正在处理的请求数量。
- **追踪**：单个请求及处理它们所执行操作的记录。每个计时的操作称为一个 **span**。
- **日志**：带时间戳的事件记录，例如应用程序启动或某个操作失败。

[**OpenTelemetry**](https://opentelemetry.io/) 是一组用于收集遥测数据并将其发送到监控服务的标准和工具，你可以在监控服务的仪表板中查看这些数据。

**FastAPI 默认提供 OpenTelemetry 支持**，用于 HTTP 请求的追踪、指标和日志。WebSocket 连接也会提供追踪和日志。要查看这些数据，请配置一个监控服务来接收它们。

## 安装 FastAPI { #install-fastapi }

安装带有 `standard` extras 的 FastAPI，其中包含用于发送遥测数据的包：

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## 创建应用 { #create-the-app }

创建文件 `main.py`：

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

注意，这些默认就能正常工作，你不需要编写任何自定义代码就能让遥测生效。

## FastAPI Cloud { #fastapi-cloud }

当你使用 `fastapi[standard]` 部署到 [FastAPI Cloud](https://fastapicloud.com) 时，指标会自动工作。你不需要再配置任何其他内容。

在 Pro 计划中，你可以在 [Metrics 仪表板](https://fastapicloud.com/docs/monitoring-and-performance/metrics/)中查看请求数量、错误率和响应时间。

<img src="/img/tutorial/opentelemetry/image01.png" alt="带有示例数据的 FastAPI Cloud Pro 指标仪表板">

## 其他监控服务 { #other-monitoring-services }

要将遥测数据发送到其他监控服务，请配置一个接受 **OTLP** 的端点，OTLP 是 OpenTelemetry 用于发送遥测数据的协议。请使用该服务的 HTTP/protobuf 基础端点。

设置这些环境变量，将示例 URL 替换为你的端点：

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` 用于在监控服务中标识你的应用。该端点是接收数据的基础 URL。在该 URL 下，追踪会发送到 `/v1/traces`，指标会发送到 `/v1/metrics`，日志会发送到 `/v1/logs`。

如果你的服务需要认证，请将 `OTEL_EXPORTER_OTLP_HEADERS` 设置为它指定的 headers，例如 `api-key=YOUR_API_KEY`。

## 运行应用 { #run-the-app }

在同一个终端中启动应用：

<div class="termy">

```console
$ uv run fastapi run
```

</div>

在另一个终端中发送请求：

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

打开你的监控服务并找到 `my-api`。下一次导出后，你可以看到一个包含 `GET /items/{item_id}` span 的追踪，以及请求数量、响应时长和活跃请求的指标。

## 自定义遥测 { #customize-telemetry }

### 配置 providers 和 exporters { #configure-providers-and-exporters }

**provider** 提供用于记录追踪、指标或日志的对象。它的配置控制这些数据如何被处理和导出。

遥测库可以配置 OpenTelemetry 的全局 providers。在应用启动前配置该库，FastAPI 会自动使用这些 providers。

当环境中设置了 OTLP 端点时，FastAPI 会为每个已启用的 provider 添加一个指向该目标的 exporter。现有 exporters 会继续将数据发送到它们自己的目标。

每个目标只配置一次。如果另一个库已经处理了环境中的目标，请禁用它的环境导出，或关闭 FastAPI 的自动设置：

```python
app = FastAPI(telemetry={"auto_configure": False})
```

你也可以直接在 `telemetry` 字典中传入 provider。例如，这个 provider 使用 OpenTelemetry 的 console exporter 在你的终端中打印请求 spans：

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

**exporter** 会将 spans 发送到它们的目标。`BatchSpanProcessor` 会对 spans 分组，并在后台发送它们。将 console exporter 替换为你的监控库提供的 exporter，即可使用它的目标。更多配置选项请参阅 [OpenTelemetry 的 Python instrumentation 指南](https://opentelemetry.io/docs/languages/python/instrumentation/)。

在同一个字典中使用 `meter_provider` 或 `logger_provider` 来提供指标或日志 provider。创建 provider 的应用程序或库负责管理它的关闭。FastAPI 管理它添加的导出组件。

/// warning | 警告

OpenTelemetry 默认使用全局 providers。不能保证[挂载的子应用](sub-applications.md)拥有独立的遥测配置。

///

### 追踪请求操作 { #trace-request-operations }

默认情况下，请求追踪包含用于解析依赖项、运行你的路径操作函数、序列化响应，以及运行 FastAPI 的 `BackgroundTasks` 中每个任务的 spans。这些 spans 使用相同的 provider 和 exporters。

后台任务 spans 仍然属于该请求的追踪。它们在 HTTP 响应 span 结束后运行，因此不会增加测量到的响应时间。

如果只想记录 HTTP 请求 span，请将 `operation_spans` 设置为 `False`：

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### 追踪 WebSocket 连接 { #trace-websocket-connections }

每个 WebSocket 连接都有一个 span，例如 `WS /ws/{room}`，覆盖处理程序和依赖项清理。它使用相同的 providers 和设置，包括用于依赖项解析和 endpoint 执行的 `operation_spans`。

HTTP 请求指标仅覆盖 HTTP 请求。使用代码 `1000` 或 `1001` 的正常 WebSocket 断开不会产生错误日志。

### 检查错误 { #inspect-errors }

FastAPI 会将未处理的异常记录为 OpenTelemetry 日志，并关联到请求或连接的追踪。即使追踪未被采样，也会记录错误日志。

异常日志包含异常的类型、消息和堆栈跟踪。消息和堆栈跟踪可能包含敏感信息。使用你的 provider 的日志处理器来过滤或脱敏它们，或将 `logs` 设置为 `False` 以禁用这些日志。

FastAPI 还会将请求验证失败记录为警告日志，其中包含路由和错误数量。这些日志不包含无效输入。

## 选择要记录的内容 { #choose-what-to-record }

`telemetry` 字典还接受以下设置：

| 设置 | 用途 | 默认值 |
| --- | --- | --- |
| `tracing` | 记录 HTTP 请求和 WebSocket 连接 spans | `True` |
| `metrics` | 记录 HTTP 请求指标 | `True` |
| `logs` | 记录验证失败和未处理的异常 | `True` |
| `operation_spans` | 为请求操作添加 spans | `True` |
| `exclude` | 当接收 ASGI scope 的函数返回 `True` 时跳过请求 | `None` |
| `auto_configure` | 为环境变量中设置的端点添加 exporters | `True` |

例如，要在排除健康检查的同时收集指标：

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

当你的应用程序自行处理 provider 设置时（例如在其 lifespan 函数中），请将 `auto_configure` 设置为 `False`。
