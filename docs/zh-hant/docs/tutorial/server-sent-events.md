# Server-Sent Events（SSE） { #server-sent-events-sse }

你可以使用 Server-Sent Events（SSE）把資料串流傳送給用戶端。

這與[串流 JSON Lines](stream-json-lines.md)類似，但使用瀏覽器原生支援、透過 [`EventSource` API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 的 `text/event-stream` 格式。

/// info

在 FastAPI 0.135.0 新增。

///

## 什麼是 Server-Sent Events？ { #what-are-server-sent-events }

SSE 是一種透過 HTTP 從伺服器向用戶端串流傳送資料的標準。

每個事件都是一個小型文字區塊，包含 `data`、`event`、`id` 和 `retry` 等「欄位」，並以空白行分隔。

看起來像這樣：

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE 常用於 AI 聊天串流、即時通知、日誌與可觀察性，以及其他由伺服器主動推送更新給用戶端的情境。

/// tip

如果你要串流二進位資料，例如影片或音訊，請參考進階指南：[串流資料](../advanced/stream-data.md)。

///

## 使用 FastAPI 串流 SSE { #stream-sse-with-fastapi }

要在 FastAPI 中串流 SSE，請在你的路徑操作函式（path operation function）中使用 `yield`，並設定 `response_class=EventSourceResponse`。

從 `fastapi.sse` 匯入 `EventSourceResponse`：

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

每個 `yield` 的項目都會以 JSON 編碼並放在 SSE 事件的 `data:` 欄位中送出。

如果你把回傳型別宣告為 `AsyncIterable[Item]`，FastAPI 會用它來透過 Pydantic 進行**驗證**、**文件化**與**序列化**。

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip

因為 Pydantic 會在 **Rust** 端進行序列化，如果你有宣告回傳型別，效能會比未宣告時高很多。

///

### 非 async 的路徑操作函式 { #non-async-path-operation-functions }

你也可以使用一般的 `def` 函式（沒有 `async`），並同樣使用 `yield`。

FastAPI 會確保正確執行，不會阻塞事件迴圈。

由於此函式不是 async，正確的回傳型別是 `Iterable[Item]`：

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### 無回傳型別 { #no-return-type }

你也可以省略回傳型別。FastAPI 會使用 [`jsonable_encoder`](./encoder.md) 轉換資料並送出。

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

如果你需要設定 `event`、`id`、`retry` 或 `comment` 等 SSE 欄位，你可以改為 `yield` 出 `ServerSentEvent` 物件，而不是單純的資料。

從 `fastapi.sse` 匯入 `ServerSentEvent`：

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

`data` 欄位一律會以 JSON 編碼。你可以傳入任何可序列化為 JSON 的值，包括 Pydantic 模型。

## 原始資料 { #raw-data }

如果你需要在**不**進行 JSON 編碼的情況下傳送資料，請使用 `raw_data` 取代 `data`。

這對於傳送已格式化的文字、日誌行或特殊的 <dfn title="用於表示特殊條件或狀態的值">"哨兵"</dfn> 值（例如 `[DONE]`）很有用。

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note

`data` 與 `raw_data` 互斥。每個 `ServerSentEvent` 只能設定其中一個。

///

## 使用 `Last-Event-ID` 繼續 { #resuming-with-last-event-id }

當瀏覽器在連線中斷後重新連線時，會在 `Last-Event-ID` 標頭中傳送最後接收到的 `id`。

你可以將它作為標頭參數讀取，並用來從用戶端中斷處繼續串流：

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## 使用 POST 的 SSE { #sse-with-post }

SSE 可搭配**任何 HTTP 方法**，不僅限於 `GET`。

這對於像是透過 `POST` 串流 SSE 的協定（例如 [MCP](https://modelcontextprotocol.io)）很有用：

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## 技術細節 { #technical-details }

FastAPI 內建實作了一些 SSE 的最佳實務。

- 當 15 秒內沒有任何訊息時，傳送一次**「保活」`ping` 註解**，以避免某些代理伺服器關閉連線；此作法源自於[HTML 規範：Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes)中的建議。
- 設定 `Cache-Control: no-cache` 標頭，以**防止快取**串流內容。
- 設定特殊標頭 `X-Accel-Buffering: no`，以**避免**在像 Nginx 這類代理中被**緩衝**。

你不需要做任何事，開箱即用。🤓
