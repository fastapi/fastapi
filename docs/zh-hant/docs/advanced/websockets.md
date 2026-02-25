# WebSockets { #websockets }

你可以在 **FastAPI** 中使用 <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSockets</a>。

## 安裝 `websockets` { #install-websockets }

請先建立[虛擬環境](../virtual-environments.md){.internal-link target=_blank}、啟用它，然後安裝 `websockets`（一個讓你更容易使用「WebSocket」通訊協定的 Python 套件）：

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## WebSockets 用戶端 { #websockets-client }

### 在生產環境 { #in-production }

在你的生產系統中，你很可能有一個使用現代框架（如 React、Vue.js 或 Angular）建立的前端。

而為了透過 WebSockets 與後端通訊，你通常會使用前端的工具。

或者你可能有一個原生行動應用，使用原生程式碼直接與 WebSocket 後端通訊。

又或者你有其他任何方式與 WebSocket 端點通訊。

---

但在這個範例中，我們會用一個非常簡單的 HTML 文件與一些 JavaScript，全都寫在一個長字串裡。

當然，這並不理想，你不會在生產環境這樣做。

在生產環境你通常會用上述其中一種方式。

但這是能讓我們專注於 WebSocket 伺服端並跑起一個可運作範例的最簡單方式：

{* ../../docs_src/websockets/tutorial001_py310.py hl[2,6:38,41:43] *}

## 建立一個 `websocket` { #create-a-websocket }

在你的 **FastAPI** 應用中，建立一個 `websocket`：

{* ../../docs_src/websockets/tutorial001_py310.py hl[1,46:47] *}

/// note | 技術細節

你也可以使用 `from starlette.websockets import WebSocket`。

**FastAPI** 直接提供相同的 `WebSocket` 只是為了方便你這位開發者，但它其實是直接來自 Starlette。

///

## 等待與傳送訊息 { #await-for-messages-and-send-messages }

在你的 WebSocket 路由中，你可以 `await` 接收訊息並傳送訊息。

{* ../../docs_src/websockets/tutorial001_py310.py hl[48:52] *}

你可以接收與傳送二進位、文字與 JSON 資料。

## 試試看 { #try-it }

如果你的檔案名為 `main.py`，用以下指令執行應用：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

在瀏覽器開啟 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>。

你會看到一個像這樣的簡單頁面：

<img src="/img/tutorial/websockets/image01.png">

你可以在輸入框輸入訊息並送出：

<img src="/img/tutorial/websockets/image02.png">

你的 **FastAPI** 應用會透過 WebSockets 回應：

<img src="/img/tutorial/websockets/image03.png">

你可以傳送（與接收）多則訊息：

<img src="/img/tutorial/websockets/image04.png">

而且它們都會使用同一個 WebSocket 連線。

## 使用 `Depends` 與其他功能 { #using-depends-and-others }

在 WebSocket 端點中，你可以從 `fastapi` 匯入並使用：

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

它們的運作方式與其他 FastAPI 端點/*路徑操作* 相同：

{* ../../docs_src/websockets/tutorial002_an_py310.py hl[68:69,82] *}

/// info

因為這是 WebSocket，拋出 `HTTPException` 並沒有意義，因此我們改為拋出 `WebSocketException`。

你可以使用規範中定義的<a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">有效關閉代碼</a>之一。

///

### 用依賴試用 WebSocket { #try-the-websockets-with-dependencies }

如果你的檔案名為 `main.py`，用以下指令執行應用：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

在瀏覽器開啟 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>。

在那裡你可以設定：

* "Item ID"，用於路徑。
* "Token"，作為查詢參數。

/// tip

注意查詢參數 `token` 會由一個依賴處理。

///

之後你就能連線到 WebSocket，並開始收發訊息：

<img src="/img/tutorial/websockets/image05.png">

## 處理斷線與多個用戶端 { #handling-disconnections-and-multiple-clients }

當 WebSocket 連線關閉時，`await websocket.receive_text()` 會拋出 `WebSocketDisconnect` 例外，你可以像範例中那樣捕捉並處理。

{* ../../docs_src/websockets/tutorial003_py310.py hl[79:81] *}

試用方式：

* 用多個瀏覽器分頁開啟該應用。
* 從每個分頁傳送訊息。
* 然後關閉其中一個分頁。

這會引發 `WebSocketDisconnect` 例外，其他所有用戶端都會收到類似以下的訊息：

```
Client #1596980209979 left the chat
```

/// tip

上面的應用是一個極簡範例，用來示範如何處理並向多個 WebSocket 連線廣播訊息。

但請注意，因為所有狀態都在記憶體中的單一 list 裡管理，它只會在該程序執行期間生效，且僅適用於單一程序。

如果你需要一個容易與 FastAPI 整合、但更健壯，且可由 Redis、PostgreSQL 等後端支援的方案，請參考 <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a>。

///

## 更多資訊 { #more-info }

想了解更多選項，請參考 Starlette 的文件：

* <a href="https://www.starlette.dev/websockets/" class="external-link" target="_blank">`WebSocket` 類別</a>。
* <a href="https://www.starlette.dev/endpoints/#websocketendpoint" class="external-link" target="_blank">以類別為基礎的 WebSocket 處理</a>。
