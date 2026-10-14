# OpenTelemetry { #opentelemetry }

當你的 API 運作時，你可能會想知道它收到多少流量、哪些請求較慢，以及何時發生錯誤。

**遙測（Telemetry）**是關於應用程式行為的資料，能協助你回答這些問題。常見類型包括：

- **指標（Metrics）**：可隨時間彙整的測量值，例如回應時間和正在處理的請求數量。
- **追蹤（Traces）**：個別請求及其處理過程中所執行操作的記錄。每個計時的操作稱為一個 **span**。
- **日誌（Logs）**：附有時間戳記的事件記錄，例如應用程式啟動或操作失敗。

[**OpenTelemetry**](https://opentelemetry.io/) 是一套標準與工具，用於收集遙測資料並將其傳送到監控服務，讓你能在儀表板中查看這些資料。

**FastAPI 預設提供 OpenTelemetry 支援**，涵蓋 HTTP 請求的追蹤、指標和日誌。WebSocket 連線也提供追蹤和日誌。若要查看這些資料，請設定監控服務來接收它們。

## 安裝 FastAPI { #install-fastapi }

安裝 FastAPI 時加上 `standard` 額外選項，其中包含傳送遙測資料所需的套件：

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## 建立應用程式 { #create-the-app }

建立一個 `main.py` 檔案：

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

請注意，這些功能預設就能運作，你不需要撰寫任何自訂程式碼來啟用遙測。

## FastAPI Cloud { #fastapi-cloud }

當你使用 `fastapi[standard]` 部署到 [FastAPI Cloud](https://fastapicloud.com) 時，指標功能會自動運作。你不需要做任何額外設定。

使用 Pro 方案時，你可以在[指標儀表板](https://fastapicloud.com/docs/monitoring-and-performance/metrics/)中查看請求數量、錯誤率和回應時間。

<img src="/img/tutorial/opentelemetry/image01.png" alt="含有範例資料的 FastAPI Cloud Pro 指標儀表板">

## 其他監控服務 { #other-monitoring-services }

若要將遙測資料傳送到其他監控服務，請設定一個接受 **OTLP** 的端點。OTLP 是 OpenTelemetry 用於傳送遙測資料的協定。請使用該服務的 HTTP/protobuf 基礎端點。

設定以下環境變數，並將範例 URL 替換為你的端點：

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` 用於在監控服務中識別你的應用程式。端點是接收資料的基礎 URL。追蹤會傳送到該 URL 下的 `/v1/traces`，指標傳送到 `/v1/metrics`，日誌則傳送到 `/v1/logs`。

如果你的服務需要驗證身分，請將 `OTEL_EXPORTER_OTLP_HEADERS` 設定為該服務指定的標頭，例如 `api-key=YOUR_API_KEY`。

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

開啟你的監控服務並找到 `my-api`。下一次匯出後，你就能看到包含 `GET /items/{item_id}` span 的追蹤，以及請求數量、回應時間和處理中請求的指標。

## 自訂遙測 { #customize-telemetry }

### 設定提供者和匯出器 { #configure-providers-and-exporters }

**提供者（provider）**提供用於記錄追蹤、指標或日誌的物件。其設定控制這些資料的處理與匯出方式。

遙測函式庫可以設定 OpenTelemetry 的全域提供者。在應用程式啟動前設定好函式庫，FastAPI 就會自動使用這些提供者。

當環境中設定了 OTLP 端點時，FastAPI 會為每個已啟用的提供者新增一個指向該目的地的匯出器。現有的匯出器會繼續將資料傳送到各自的目的地。

每個目的地只需設定一次。如果另一個函式庫已經負責處理環境變數指定的目的地，請停用該函式庫依環境變數進行匯出的功能，或關閉 FastAPI 的自動設定：

```python
app = FastAPI(telemetry={"auto_configure": False})
```

你也可以直接在 `telemetry` 字典中傳入提供者。例如，這個提供者使用 OpenTelemetry 的主控台匯出器，在終端機中印出請求的 span：

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

**匯出器（exporter）**會將 span 傳送到目的地。`BatchSpanProcessor` 會將 span 分組，並在背景傳送。將主控台匯出器替換成監控函式庫提供的匯出器，即可使用該函式庫的目的地。更多設定選項請參閱 [OpenTelemetry 的 Python instrumentation 指南](https://opentelemetry.io/docs/languages/python/instrumentation/)。

在同一個字典中使用 `meter_provider` 或 `logger_provider`，即可提供指標或日誌的提供者。建立提供者的應用程式或函式庫負責管理其關閉流程。FastAPI 則管理它所新增的匯出元件。

/// warning | 警告

OpenTelemetry 預設使用全域提供者。不保證[掛載的子應用程式](sub-applications.md)能使用獨立的遙測設定。

///

### 追蹤請求操作 { #trace-request-operations }

預設情況下，請求追蹤會包含解析相依性、執行路徑操作函式、序列化回應，以及執行 FastAPI `BackgroundTasks` 中各個任務的 span。這些 span 使用相同的提供者和匯出器。

背景任務的 span 仍屬於該請求的追蹤。它們在 HTTP 回應 span 結束後才執行，因此不會增加測得的回應時間。

若只想記錄 HTTP 請求 span，請將 `operation_spans` 設為 `False`：

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### 追蹤 WebSocket 連線 { #trace-websocket-connections }

每個 WebSocket 連線都有一個 span，例如 `WS /ws/{room}`，涵蓋處理函式及相依性清理。它使用相同的提供者和設定，包括用於相依性解析和端點執行的 `operation_spans`。

HTTP 請求指標僅涵蓋 HTTP 請求。使用代碼 `1000` 或 `1001` 正常中斷的 WebSocket 連線不會產生錯誤日誌。

### 檢查錯誤 { #inspect-errors }

FastAPI 會將未處理的例外記錄為 OpenTelemetry 日誌，並連結到該請求或連線的追蹤。即使追蹤未被取樣，仍會記錄錯誤日誌。

例外日誌包含例外的類型、訊息和堆疊追蹤。訊息與堆疊追蹤可能包含敏感資訊。請使用提供者的日誌處理器來篩選或遮蔽這些資訊，或將 `logs` 設為 `False` 以停用這些日誌。

FastAPI 也會將請求驗證失敗記錄為警告日誌，其中包含路由和錯誤數量。這些日誌不會包含無效的輸入。

## 選擇要記錄的內容 { #choose-what-to-record }

`telemetry` 字典也接受以下設定：

| 設定 | 用途 | 預設值 |
| --- | --- | --- |
| `tracing` | 記錄 HTTP 請求和 WebSocket 連線的 span | `True` |
| `metrics` | 記錄 HTTP 請求指標 | `True` |
| `logs` | 記錄驗證失敗和未處理的例外 | `True` |
| `operation_spans` | 為請求操作新增 span | `True` |
| `exclude` | 當接收 ASGI scope 的函式回傳 `True` 時，略過該請求 | `None` |
| `auto_configure` | 為環境變數中設定的端點新增匯出器 | `True` |

例如，若要收集指標，但排除健康檢查：

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

當你的應用程式自行處理提供者設定時，例如在 lifespan 函式中設定，請將 `auto_configure` 設為 `False`。
