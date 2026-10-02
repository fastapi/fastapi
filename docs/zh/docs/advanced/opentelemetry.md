# OpenTelemetry { #opentelemetry }

当你的 API 运行时，你可能想知道它接收了多少流量、哪些请求较慢，以及何时发生错误。

**遥测**是反映应用行为的数据，可以帮助你回答这些问题。常见类型包括：

- **指标（Metrics）**：可以按时间汇总的测量值，例如响应时间和正在处理的请求数。
- **追踪（Traces）**：记录单个请求及处理该请求所执行的操作。每个计时的操作称为一个 **span**。
- **日志（Logs）**：带有时间戳的事件记录，例如应用启动或操作失败。

[**OpenTelemetry**](https://opentelemetry.io/) 是一套用于收集遥测数据并将其发送到监控服务的标准和工具，你可以在监控服务的仪表板中查看这些数据。

**FastAPI 默认提供 OpenTelemetry 支持**，用于 HTTP 请求的追踪、指标和日志。WebSocket 连接也提供追踪和日志。要查看这些数据，请配置监控服务来接收它们。

## 安装 FastAPI { #install-fastapi }

安装 FastAPI 时启用 `standard` 扩展依赖，其中包含发送遥测数据所需的包：

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## 创建应用 { #create-the-app }

创建文件 `main.py`：

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

注意，这一切默认就能工作，你无需编写任何自定义代码即可使用遥测功能。

## FastAPI Cloud { #fastapi-cloud }

使用 `fastapi[standard]` 部署到 [FastAPI Cloud](https://fastapicloud.com) 时，指标功能会自动工作。你无需进行其他配置。

使用 Pro 套餐时，你可以在[指标仪表板](https://fastapicloud.com/docs/monitoring-and-performance/metrics/)中查看请求数、错误率和响应时间。

<img src="/img/tutorial/opentelemetry/image01.png" alt="显示示例数据的 FastAPI Cloud Pro 指标仪表板">

## 其他监控服务 { #other-monitoring-services }

要将遥测数据发送到其他监控服务，请配置一个接受 **OTLP** 的端点，OTLP 是 OpenTelemetry 用于发送遥测数据的协议。请使用该服务的 HTTP/protobuf 基础端点。

设置以下环境变量，将示例 URL 替换为你的端点：

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` 用于在监控服务中标识你的应用。端点是接收数据的基础 URL。追踪会发送到该 URL 下的 `/v1/traces`，指标发送到 `/v1/metrics`，日志发送到 `/v1/logs`。

如果你的服务需要身份验证，请将 `OTEL_EXPORTER_OTLP_HEADERS` 设置为该服务指定的请求头，例如 `api-key=YOUR_API_KEY`。

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

打开你的监控服务，找到 `my-api`。下一次导出后，你就能看到一条包含 `GET /items/{item_id}` span 的追踪，以及请求数、响应耗时和活跃请求数的指标。

## 自定义遥测 { #customize-telemetry }

### 配置 provider 和 exporter { #configure-providers-and-exporters }

**provider** 提供用于记录追踪、指标或日志的对象。其配置决定了这些数据的处理和导出方式。

遥测库可以配置 OpenTelemetry 的全局 provider。在应用启动之前配置好该库，FastAPI 就会自动使用这些 provider。

当环境中设置了 OTLP 端点时，FastAPI 会为每个已启用的 provider 添加一个向该目标发送数据的 exporter。现有的 exporter 会继续向各自的目标发送数据。

每个目标只需配置一次。如果另一个库已经负责向环境变量指定的目标导出数据，请禁用该库基于环境变量的导出功能，或关闭 FastAPI 的自动配置：

```python
app = FastAPI(telemetry={"auto_configure": False})
```

你也可以直接在 `telemetry` 字典中传入 provider。例如，下面的 provider 使用 OpenTelemetry 的控制台 exporter，在终端中打印请求 span：

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

**exporter** 将 span 发送到目标位置。`BatchSpanProcessor` 将 span 分组，并在后台发送。要使用监控库的目标位置，请将控制台 exporter 替换为该库提供的 exporter。更多配置选项请参阅 [OpenTelemetry 的 Python 插桩指南](https://opentelemetry.io/docs/languages/python/instrumentation/)。

在同一个字典中使用 `meter_provider` 或 `logger_provider` 来提供指标或日志 provider。创建 provider 的应用或库负责管理其关闭过程。FastAPI 负责管理它所添加的导出组件。

/// warning | 警告

OpenTelemetry 默认使用全局 provider。不保证[挂载的子应用](sub-applications.md)可以拥有独立的遥测配置。

///

### 追踪请求操作 { #trace-request-operations }

默认情况下，请求追踪包含以下操作的 span：解析依赖项、运行路径操作函数、序列化响应，以及运行 FastAPI 的 `BackgroundTasks` 中的每个任务。这些 span 使用相同的 provider 和 exporter。

后台任务的 span 仍属于该请求的追踪。它们在 HTTP 响应 span 结束后运行，因此不会增加测得的响应时间。

要仅记录 HTTP 请求 span，请将 `operation_spans` 设置为 `False`：

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### 追踪 WebSocket 连接 { #trace-websocket-connections }

每个 WebSocket 连接都有一个类似 `WS /ws/{room}` 的 span，涵盖处理函数和依赖项清理过程。它使用相同的 provider 和设置，包括用于依赖项解析和端点执行的 `operation_spans`。

HTTP 请求指标仅涵盖 HTTP 请求。使用代码 `1000` 或 `1001` 正常断开的 WebSocket 连接不会产生日志错误。

### 检查错误 { #inspect-errors }

FastAPI 将未处理的异常记录为 OpenTelemetry 日志，并关联到请求或连接的追踪。即使追踪未被采样，也会记录错误日志。

异常日志包含异常类型、消息和堆栈追踪。消息和堆栈追踪可能包含敏感信息。请使用 provider 的日志处理器对其进行过滤或脱敏，或将 `logs` 设置为 `False` 来禁用这些日志。

FastAPI 还会将请求验证失败记录为警告日志，其中包含路由和错误数量。这些日志不包含无效的输入。

## 选择要记录的内容 { #choose-what-to-record }

`telemetry` 字典还接受以下设置：

| 设置 | 用途 | 默认值 |
| --- | --- | --- |
| `tracing` | 记录 HTTP 请求和 WebSocket 连接的 span | `True` |
| `metrics` | 记录 HTTP 请求指标 | `True` |
| `logs` | 记录验证失败和未处理的异常 | `True` |
| `operation_spans` | 为请求操作添加 span | `True` |
| `exclude` | 当接收 ASGI scope 的函数返回 `True` 时跳过请求 | `None` |
| `auto_configure` | 为环境变量中设置的端点添加 exporter | `True` |

例如，要收集指标，同时排除健康检查：

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

当应用自行配置 provider 时，例如在其 lifespan 函数中配置，请将 `auto_configure` 设置为 `False`。
