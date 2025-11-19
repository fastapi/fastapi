# 第一步

最簡單的 FastAPI 檔案可能看起來像這樣：

{* ../../docs_src/first_steps/tutorial001.py *}

將其複製到一個名為 `main.py` 的文件中。

執行即時重新載入伺服器（live server）：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:single">main.py</u>
<font color="#3465A4">INFO    </font> Using path <font color="#3465A4">main.py</font>
<font color="#3465A4">INFO    </font> Resolved absolute path <font color="#75507B">/home/user/code/awesomeapp/</font><font color="#AD7FA8">main.py</font>
<font color="#3465A4">INFO    </font> Searching for package file structure from directories with <font color="#3465A4">__init__.py</font> files
<font color="#3465A4">INFO    </font> Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

 ╭─ <font color="#8AE234"><b>Python module file</b></font> ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

<font color="#3465A4">INFO    </font> Importing module <font color="#4E9A06">main</font>
<font color="#3465A4">INFO    </font> Found importable FastAPI app

 ╭─ <font color="#8AE234"><b>Importable FastAPI app</b></font> ─╮
 │                          │
 │  <span style="background-color:#272822"><font color="#FF4689">from</font></span><span style="background-color:#272822"><font color="#F8F8F2"> main </font></span><span style="background-color:#272822"><font color="#FF4689">import</font></span><span style="background-color:#272822"><font color="#F8F8F2"> app</font></span><span style="background-color:#272822">  </span>  │
 │                          │
 ╰──────────────────────────╯

<font color="#3465A4">INFO    </font> Using import string <font color="#8AE234"><b>main:app</b></font>

 <span style="background-color:#C4A000"><font color="#2E3436">╭────────── FastAPI CLI - Development mode ───────────╮</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Serving at: http://127.0.0.1:8000                  │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  API docs: http://127.0.0.1:8000/docs               │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Running in development mode, for production use:   │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  </font></span><span style="background-color:#C4A000"><font color="#555753"><b>fastapi run</b></font></span><span style="background-color:#C4A000"><font color="#2E3436">                                        │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">╰─────────────────────────────────────────────────────╯</font></span>

<font color="#4E9A06">INFO</font>:     Will watch for changes in these directories: [&apos;/home/user/code/awesomeapp&apos;]
<font color="#4E9A06">INFO</font>:     Uvicorn running on <b>http://127.0.0.1:8000</b> (Press CTRL+C to quit)
<font color="#4E9A06">INFO</font>:     Started reloader process [<font color="#34E2E2"><b>2265862</b></font>] using <font color="#34E2E2"><b>WatchFiles</b></font>
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">2265873</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
```

</div>

在輸出中，有一列類似於：

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

那列顯示了你的應用程式正在本地端機器上運行的 URL。

### 查看它

在瀏覽器中打開 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

你將看到如下的 JSON 回應：

```JSON
{"message": "Hello World"}
```

### 互動式 API 文件

現在，前往 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

你將看到自動的互動式 API 文件（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 替代 API 文件

現在，前往 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

你將看到另一種自動文件（由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** 使用定義 API 的 **OpenAPI** 標準來生成一個 「schema」 與你的所有 API。

#### 「Schema」

「schema」是對某個事物的定義或描述。它並不是實作它的程式碼，而僅僅是一個抽象的描述。

#### API 「schema」

在這種情況下，<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> 是一個規範，它規定了如何定義 API 的 schema。

這個 schema 定義包含了你的 API 路徑、可能接收的參數等內容。

#### 資料 「schema」

「schema」這個術語也可能指某些資料的結構，比如 JSON 內容的結構。

在這種情況下，它指的是 JSON 的屬性、資料型別等。

#### OpenAPI 和 JSON Schema

OpenAPI 定義了 API 的 schema。這個 schema 包含了使用 **JSON Schema** 定義的資料，這是 JSON 資料 schema 的標準。

#### 檢查 `openapi.json`

如果你好奇原始的 OpenAPI schema 長什麼樣子，FastAPI 會自動生成一個包含所有 API 描述的 JSON (schema)。

你可以直接在 <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a> 查看它。

它會顯示一個 JSON，類似於：

```JSON
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### OpenAPI 的用途

OpenAPI schema 驅動了兩個互動式文件系統。

而且有許多替代方案，所有這些都是基於 OpenAPI。你可以輕鬆地將任何這些替代方案添加到使用 **FastAPI** 建置的應用程式中。

你也可以用它自動生成程式碼，讓前端、手機應用程式或物聯網設備等與你的 API 進行通訊。

## 逐步回顧

### 第一步：引入 `FastAPI`

{* ../../docs_src/first_steps/tutorial001.py h1[1] *}

`FastAPI` 是一個 Python 類別，提供所有 API 的全部功能。

/// note | Technical Details

`FastAPI` 是一個直接繼承自 `Starlette` 的類別。

你同樣可以透過 `FastAPI` 來使用 <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> 所有的功能。

///

### 第二步：建立一個 `FastAPI` 「實例」

{* ../../docs_src/first_steps/tutorial001.py h1[3] *}

這裡的 `app` 變數將會是 `FastAPI` 類別的「實例」。

這將是你建立所有 API 的主要互動點。

### 第三步：建立一個 *路徑操作*

#### 路徑

這裡的「路徑」指的是 URL 中自第一個 `/` 以後的部分。

例如，在 URL 中：

```
https://example.com/items/foo
```

……的路徑將會是：

```
/items/foo
```

/// info

「路徑」也常被稱為「端點 endpoint」或「路由 route」。

///

在建置 API 時，「路徑」是分離「關注點」和「資源」的主要方式。

#### 操作

這裡的「操作」指的是 HTTP 的「方法」之一。

其中包括：

* `POST`
* `GET`
* `PUT`
* `DELETE`

……以及更少見的：

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

在 HTTP 協定中，你可以使用這些「方法」之一（或更多）與每個路徑進行通信。

---

在建置 API 時，你通常使用這些特定的 HTTP 方法來執行特定的動作。

通常你使用：

* `POST`：用來建立資料。
* `GET`：用來讀取資料。
* `PUT`：用來更新資料。
* `DELETE`：用來刪除資料。

所以，在 OpenAPI 中，每個 HTTP 方法都被稱為「操作」。

我們將會稱它們為「**操作**」。

#### 定義一個 *路徑操作裝飾器*

{* ../../docs_src/first_steps/tutorial001.py h1[6] *}

`@app.get("/")` 告訴 **FastAPI** 那個函式負責處理請求：

* 路徑 `/`
* 使用 <abbr title="HTTP GET 方法"><code>get</code>操作</abbr>

/// info | `@decorator` Info

Python 中的 `@something` 語法被稱為「裝飾器」。

你把它放在一個函式上面。像一個漂亮的裝飾帽子（我猜這是術語的來源）。

一個「裝飾器」會對下面的函式做一些事情。

在這種情況下，這個裝飾器告訴 **FastAPI** 那個函式對應於 **路徑** `/` 和 **操作** `get`.

這就是「**路徑操作裝飾器**」。

///

你也可以使用其他的操作：

* `@app.post()`
* `@app.put()`
* `@app.delete()`

以及更少見的：

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip

你可以自由地使用每個操作（HTTP 方法）。

**FastAPI** 不強制任何特定的意義。

這裡的資訊作為一個指南，而不是要求。

例如，當使用 GraphQL 時，你通常只使用 `POST` 操作。

///

### 第四步：定義 **路徑操作函式**

這是我們的「**路徑操作函式**」：

* **path**: 是 `/`.
* **operation**: 是 `get`.
* **function**: 是裝飾器下面的函式（在 `@app.get("/")` 下面）。

{* ../../docs_src/first_steps/tutorial001.py h1[7] *}

這就是一個 Python 函式。

它將會在 **FastAPI** 收到一個請求時被呼叫，使用 `GET` 操作。

在這種情況下，它是一個 `async` 函式。

---

你可以將它定義為一個正常的函式，而不是 `async def`:

{* ../../docs_src/first_steps/tutorial003.py h1[7] *}

/// note

如果你不知道差別，請查看 [Async: *"In a hurry?"*](../async.md#in-a-hurry){.internal-link target=_blank}.

///

### 第五步：回傳內容

{* ../../docs_src/first_steps/tutorial001.py h1[8] *}

你可以返回一個 `dict`、`list`、單個值作為 `str`、`int` 等。

你也可以返回 Pydantic 模型（稍後你會看到更多關於這方面的內容）。

有很多其他物件和模型會自動轉換為 JSON（包括 ORMs，等等）。試用你最喜歡的，很有可能它們已經有支援。

## 回顧

* 引入 `FastAPI`.
* 建立一個 `app` 實例。
* 寫一個 **路徑操作裝飾器** 使用裝飾器像 `@app.get("/")`。
* 定義一個 **路徑操作函式**；例如，`def root(): ...`。
* 使用命令 `fastapi dev` 執行開發伺服器。
