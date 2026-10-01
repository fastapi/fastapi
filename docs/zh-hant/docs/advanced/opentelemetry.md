# OpenTelemetry { #opentelemetry }

當你的 API 正在執行時，你可能會想知道它接收了多少流量、哪些請求很慢，以及何時發生錯誤。

**遙測**是關於你的應用程式行為的資料，可幫助你回答這些問題。常見類型包括：

- **指標**：可以隨時間彙總的測量值，例如回應時間和正在處理的請求數量。
- **追蹤**：個別請求以及為處理它們而執行的操作記錄。每個計時操作稱為 **span**。
- **日誌**：帶有時間戳記的事件記錄，例如應用程式啟動或操作失敗。

[**OpenTelemetry**](https://opentelemetry.io/) 是一組標準和工具，用於收集遙測資料並將其傳送到監控服務，你可以在那裡透過儀表板探索這些資料。

**FastAPI 預設提供 OpenTelemetry 支援**，包括 HTTP 請求追蹤、指標和日誌。WebSocket 連線也會提供追蹤和日誌。若要查看這些資料，請設定監控服務來接收它們。

## 安裝 FastAPI { #install-fastapi }

使用 `standard` extras 安裝 FastAPI，其中包含傳送遙測資料所需的套件：

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## 建立應用程式 { #create-the-app }

建立檔案 `main.py`：

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

請注意，這一切預設就能運作，你不需要撰寫任何自訂程式碼就能讓遙測功能運作。

## FastAPI Cloud { #fastapi-cloud }

當你使用 `fastapi[standard]` 部署到 [FastAPI Cloud](https://fastapicloud.com) 時，指標會自動運作。你不需要再設定任何其他內容。

在 Pro 方案中，你可以在 [Metrics dashboard](https://fastapicloud.com/docs/monitoring-and-performance/metrics/) 檢視請求數、錯誤率和回應時間。

<img src="/img/tutorial/opentelemetry/image01.png" alt="FastAPI Cloud Pro 指標儀表板與範例資料">

## 其他監控服務 { #other-monitoring-services }

若要將遙測資料傳送到另一個監控服務，請設定一個接受 **OTLP** 的 endpoint，OTLP 是 OpenTelemetry 用來傳送遙測資料的協定。請使用該服務的 HTTP/protobuf 基礎 endpoint。

設定這些環境變數，並將範例 URL 替換為你的 endpoint：

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` 會在監控服務中識別你的應用程式。endpoint 是接收資料的基礎 URL。追蹤會傳送到該 URL 下的 `/v1/traces`，指標會傳送到 `/v1/metrics`，日誌會傳送到 `/v1/logs`。

如果你的服務需要驗證，請將 `OTEL_EXPORTER_OTLP_HEADERS` 設定為它指定的 headers，例如 `api-key=YOUR_API_KEY`。

## 執行應用程式 { #run-the-app }

在同一個終端機中啟動應用程式：

<div class="termy">

```console
$ uv run fastapi run
```

</div>

在另一個終端機中傳送請求：

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

開啟你的監控服務並找到 `my-api`。下一次匯出後，你可以看到包含 `GET /items/{item_id}` span 的追蹤，以及請求數、回應持續時間和作用中請求的指標。

## 自訂遙測 { #customize-telemetry }

### 設定 providers 和 exporters { #configure-providers-and-exporters }

**provider** 會提供用來記錄追蹤、指標或日誌的物件。它的設定會控制資料如何被處理和匯出。

遙測函式庫可以設定 OpenTelemetry 的全域 providers。在應用程式啟動前設定函式庫，FastAPI 就會自動使用這些 providers。

當環境中設定了 OTLP endpoint 時，FastAPI 會為每個已啟用的 provider 加入一個指向該目的地的 exporter。既有的 exporters 會繼續將資料傳送到它們的目的地。

每個目的地只設定一次。如果另一個函式庫已經處理環境中的目的地，請停用它的環境匯出，或關閉 FastAPI 的自動設定：

```python
app = FastAPI(telemetry={"auto_configure": False})
```

你也可以直接在 `telemetry` 字典中傳入 provider。例如，這個 provider 使用 OpenTelemetry 的 console exporter，在你的終端機中列印請求 span：

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

**exporter** 會將 spans 傳送到它們的目的地。`BatchSpanProcessor` 會將 spans 分組並在背景傳送。若要使用你的監控函式庫的目的地，請將 console exporter 替換為該函式庫提供的 exporter。更多設定選項請參閱 [OpenTelemetry 的 Python instrumentation 指南](https://opentelemetry.io/docs/languages/python/instrumentation/)。

在同一個字典中使用 `meter_provider` 或 `logger_provider`，以提供指標或日誌 provider。建立 provider 的應用程式或函式庫會管理它的關閉。FastAPI 會管理它加入的匯出元件。

/// warning | 警告

OpenTelemetry 預設使用全域 providers。無法保證 [已掛載的子應用程式](sub-applications.md) 具有獨立的遙測設定。

///

### 追蹤請求操作 { #trace-request-operations }

預設情況下，請求追蹤會包含解析依賴項、執行你的路徑操作函式、序列化回應，以及執行 FastAPI `BackgroundTasks` 中每個任務的 spans。這些 spans 會使用相同的 provider 和 exporters。

背景任務 spans 仍然屬於該請求的追蹤。它們會在 HTTP 回應 span 結束後執行，因此不會增加測量到的回應時間。

若只要記錄 HTTP 請求 span，請將 `operation_spans` 設定為 `False`：

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}

### 追蹤 WebSocket 連線 { #trace-websocket-connections }

每個 WebSocket 連線都有一個 span，例如 `WS /ws/{room}`，涵蓋 handler 和依賴項清理。它使用相同的 providers 和設定，包括用於依賴項解析與 endpoint 執行的 `operation_spans`。

HTTP 請求指標只涵蓋 HTTP 請求。使用代碼 `1000` 或 `1001` 的正常 WebSocket 斷線不會產生錯誤日誌。

### 檢查錯誤 { #inspect-errors }

FastAPI 會將未處理的例外記錄為 OpenTelemetry 日誌，並連結到請求或連線的追蹤。即使追蹤未被取樣，也會記錄錯誤日誌。

例外日誌包含例外的類型、訊息和堆疊追蹤。訊息和堆疊追蹤可能包含敏感資訊。請使用你的 provider 的 log processors 來過濾或遮蔽它們，或將 `logs` 設定為 `False` 以停用這些日誌。

FastAPI 也會將請求驗證失敗記錄為警告日誌，其中包含路由和錯誤數量。這些日誌不包含無效輸入。

## 選擇要記錄的內容 { #choose-what-to-record }

`telemetry` 字典也接受以下設定：

| 設定 | 用途 | 預設值 |
| --- | --- | --- |
| `tracing` | 記錄 HTTP 請求和 WebSocket 連線 spans | `True` |
| `metrics` | 記錄 HTTP 請求指標 | `True` |
| `logs` | 記錄驗證失敗和未處理的例外 | `True` |
| `operation_spans` | 為請求操作加入 spans | `True` |
| `exclude` | 當接收 ASGI scope 的函式回傳 `True` 時略過請求 | `None` |
| `auto_configure` | 為環境變數中設定的 endpoints 加入 exporters | `True` |

例如，若要在排除健康檢查的同時收集指標：

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

當你的應用程式自行處理 provider 設定時，例如在它的 lifespan 函式中，請將 `auto_configure` 設定為 `False`。
