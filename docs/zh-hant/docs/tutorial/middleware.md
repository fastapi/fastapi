# 中介軟體 { #middleware }

你可以在 **FastAPI** 應用程式中加入中介軟體。

「中介軟體」是一個函式，在任何特定的*路徑操作*處理之前先處理每個**請求**；在回傳之前，也會處理每個**回應**。

- 它會攔截進到應用程式的每個**請求**。
- 然後可以對該**請求**做一些處理或執行所需的程式碼。
- 接著把**請求**傳遞給應用程式的其餘部分（某個*路徑操作*）處理。
- 之後再接收應用程式（某個*路徑操作*）所產生的**回應**。
- 可以對該**回應**做一些處理或執行所需的程式碼。
- 然後回傳**回應**。

/// note | 技術細節

如果你有使用帶有 `yield` 的相依性，其釋放階段的程式碼會在中介軟體之後執行。

若有背景工作（在[背景工作](background-tasks.md){.internal-link target=_blank}一節會介紹，你稍後會看到），它們會在所有中介軟體之後執行。

///

## 建立中介軟體 { #create-a-middleware }

要建立中介軟體，將裝飾器 `@app.middleware("http")` 加在函式上方。

中介軟體函式會接收：

- `request`。
- 一個函式 `call_next`，會以 `request` 作為參數。
    - 這個函式會把 `request` 傳給對應的*路徑操作*。
    - 然後回傳對應*路徑操作*所產生的 `response`。
- 然後你可以在回傳之前進一步修改 `response`。

{* ../../docs_src/middleware/tutorial001_py310.py hl[8:9,11,14] *}

/// tip

請記得，自訂的非標準標頭可以<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">使用 `X-` 前綴</a>。

但如果你有自訂標頭並希望瀏覽器端的用戶端能看到它們，你需要在 CORS 設定（[CORS（Cross-Origin Resource Sharing）](cors.md){.internal-link target=_blank}）中使用 <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette 的 CORS 文件</a>所記載的參數 `expose_headers` 將它們加入。

///

/// note | 技術細節

你也可以使用 `from starlette.requests import Request`。

**FastAPI** 為了方便開發者而提供了它，但實際上它直接來自 Starlette。

///

### 在 `response` 之前與之後 { #before-and-after-the-response }

你可以在任何*路徑操作*接收 `request` 之前，加入要執行的程式碼。

也可以在產生出 `response` 之後、回傳之前執行程式碼。

例如，你可以新增一個自訂標頭 `X-Process-Time`，其內容為處理請求並產生回應所花費的秒數：

{* ../../docs_src/middleware/tutorial001_py310.py hl[10,12:13] *}

/// tip

這裡我們使用 <a href="https://docs.python.org/3/library/time.html#time.perf_counter" class="external-link" target="_blank">`time.perf_counter()`</a> 而不是 `time.time()`，因為在這些用例中它可能更精確。🤓

///

## 多個中介軟體的執行順序 { #multiple-middleware-execution-order }

當你使用 `@app.middleware()` 裝飾器或 `app.add_middleware()` 方法加入多個中介軟體時，每個新的中介軟體都會包裹應用程式，形成一個堆疊。最後加入的中介軟體位於最外層，最先加入的位於最內層。

在請求路徑上，最外層的中介軟體最先執行。

在回應路徑上，它最後執行。

例如：

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

執行順序如下：

- **請求**：MiddlewareB → MiddlewareA → 路由

- **回應**：路由 → MiddlewareA → MiddlewareB

這種堆疊行為可確保中介軟體以可預期且可控制的順序執行。

## 其他中介軟體 { #other-middlewares }

你之後可以在[進階使用者指南：進階中介軟體](../advanced/middleware.md){.internal-link target=_blank}閱讀更多關於其他中介軟體的內容。

下一節你將會讀到如何使用中介軟體處理 <abbr title="Cross-Origin Resource Sharing - 跨來源資源共用">CORS</abbr>。
