# 第一步 { #first-steps }

最簡單的 FastAPI 檔案可能看起來像這樣：

{* ../../docs_src/first_steps/tutorial001_py39.py *}

將其複製到一個名為 `main.py` 的檔案中。

執行即時重新載入伺服器（live server）：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

在輸出中，有一列類似於：

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

那列顯示了你的應用程式在本機上提供服務的 URL。

### 查看它 { #check-it }

在瀏覽器中打開 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>。

你將看到如下的 JSON 回應：

```JSON
{"message": "Hello World"}
```

### 互動式 API 文件 { #interactive-api-docs }

現在，前往 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你將看到自動的互動式 API 文件（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 替代 API 文件 { #alternative-api-docs }

現在，前往 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

你將看到另一種自動文件（由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** 使用定義 API 的 **OpenAPI** 標準來生成一個「schema」，包含你的所有 API。

#### 「Schema」 { #schema }

「schema」是對某個事物的定義或描述。它不是實作它的程式碼，而僅僅是一個抽象的描述。

#### API「schema」 { #api-schema }

在這種情況下，<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> 是一個規範，它規定了如何定義 API 的 schema。

這個 schema 定義包含了你的 API 路徑、它們可能接收的參數等內容。

#### 資料「schema」 { #data-schema }

「schema」這個術語也可能指某些資料的結構，例如 JSON 內容。

在這種情況下，它指的是 JSON 的屬性、以及它們的資料型別等。

#### OpenAPI 和 JSON Schema { #openapi-and-json-schema }

OpenAPI 為你的 API 定義了一個 API schema。而該 schema 使用 **JSON Schema**（JSON 資料 schema 的標準）包含你的 API 傳送與接收的資料定義（或「schemas」）。

#### 檢查 `openapi.json` { #check-the-openapi-json }

如果你對原始的 OpenAPI schema 長什麼樣子感到好奇，FastAPI 會自動生成一個 JSON（schema），其中包含你的所有 API 的描述。

你可以直接在：<a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a> 查看它。

它會顯示一個開頭類似於以下內容的 JSON：

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

#### OpenAPI 的用途 { #what-is-openapi-for }

OpenAPI schema 驅動了內建的兩個互動式文件系統。

而且有許多替代方案，全部都基於 OpenAPI。你可以輕鬆地將任何這些替代方案添加到使用 **FastAPI** 建置的應用程式中。

你也可以用它自動生成程式碼，讓與你的 API 通訊的 client 使用。例如，前端、行動或 IoT 應用程式。

### 部署你的應用程式（可選） { #deploy-your-app-optional }

你也可以選擇把你的 FastAPI 應用程式部署到 <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>；如果你還沒加入候補名單，就去加入吧。 🚀

如果你已經有 **FastAPI Cloud** 帳號（我們從候補名單邀請了你 😉），你可以用一個指令部署你的應用程式。

在部署之前，請確認你已登入：

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

接著部署你的應用程式：

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

就這樣！現在你可以透過那個 URL 存取你的應用程式。 ✨

## 逐步回顧 { #recap-step-by-step }

### 第一步：引入 `FastAPI` { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py39.py hl[1] *}

`FastAPI` 是一個 Python 類別，提供你的 API 所有功能。

/// note | Technical Details

`FastAPI` 是一個直接繼承自 `Starlette` 的類別。

你同樣可以透過 `FastAPI` 來使用 <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> 所有的功能。

///

### 第二步：建立一個 `FastAPI`「實例」 { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py39.py hl[3] *}

這裡的 `app` 變數將會是 `FastAPI` 類別的一個「實例」。

這將是你用來建立所有 API 的主要互動點。

### 第三步：建立一個 *路徑操作* { #step-3-create-a-path-operation }

#### 路徑 { #path }

這裡的「路徑」指的是 URL 中自第一個 `/` 開始的最後一段部分。

例如，在 URL 中：

```
https://example.com/items/foo
```

...路徑將會是：

```
/items/foo
```

/// info

「路徑」也常被稱為「端點 endpoint」或「路由 route」。

///

在建置 API 時，「路徑」是分離「關注點」和「資源」的主要方式。

#### 操作 { #operation }

這裡的「操作」指的是 HTTP 的「方法」之一。

其中包括：

* `POST`
* `GET`
* `PUT`
* `DELETE`

...以及更少見的：

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

在 HTTP 協定中，你可以使用這些「方法」之一（或更多）與每個路徑進行通訊。

---

在建置 API 時，你通常使用這些特定的 HTTP 方法來執行特定的動作。

通常你使用：

* `POST`：用來建立資料。
* `GET`：用來讀取資料。
* `PUT`：用來更新資料。
* `DELETE`：用來刪除資料。

所以，在 OpenAPI 中，每個 HTTP 方法都被稱為「操作」。

我們也將稱它們為「**操作**」。

#### 定義一個 *路徑操作裝飾器* { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py39.py hl[6] *}

`@app.get("/")` 告訴 **FastAPI**，下面那個函式負責處理前往以下位置的請求：

* 路徑 `/`
* 使用 <abbr title="an HTTP GET method"><code>get</code> operation</abbr>

/// info | `@decorator` Info

Python 中的 `@something` 語法被稱為「裝飾器」。

你把它放在一個函式上面。像一個漂亮的裝飾帽子（我猜這是術語的來源）。

一個「裝飾器」會對下面的函式做一些事情。

在這種情況下，這個裝飾器告訴 **FastAPI**，下面的函式對應於 **路徑** `/` 和 **操作** `get`。

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

你可以依照你的需求自由使用每個操作（HTTP 方法）。

**FastAPI** 不強制任何特定意義。

這裡的資訊是作為指南，而不是要求。

例如，當使用 GraphQL 時，你通常只使用 `POST` 操作來執行所有動作。

///

### 第四步：定義 **路徑操作函式** { #step-4-define-the-path-operation-function }

這是我們的「**路徑操作函式**」：

* **path**：是 `/`。
* **operation**：是 `get`。
* **function**：是「裝飾器」下面的函式（在 `@app.get("/")` 下面）。

{* ../../docs_src/first_steps/tutorial001_py39.py hl[7] *}

這就是一個 Python 函式。

當 **FastAPI** 收到一個前往 URL "`/`" 並使用 `GET` 操作的請求時，它就會被呼叫。

在這種情況下，它是一個 `async` 函式。

---

你也可以將它定義為一個一般函式，而不是 `async def`：

{* ../../docs_src/first_steps/tutorial003_py39.py hl[7] *}

/// note

如果你不知道差別，請查看 [Async: *"In a hurry?"*](../async.md#in-a-hurry){.internal-link target=_blank}。

///

### 第五步：回傳內容 { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py39.py hl[8] *}

你可以回傳一個 `dict`、`list`、`str`、`int` 等單一值。

你也可以回傳 Pydantic 模型（稍後你會看到更多關於這方面的內容）。

有很多其他物件和模型會自動轉換為 JSON（包括 ORMs 等）。試用你最喜歡的，很有可能它們已經有支援。

### 第六步：部署它 { #step-6-deploy-it }

用一個指令將你的應用程式部署到 **<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>**：`fastapi deploy`。 🎉

#### 關於 FastAPI Cloud { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** 是由 **FastAPI** 背後的同一位作者與團隊打造。

它簡化了以最少力氣進行 **建置**、**部署** 與**存取** API 的流程。

它把用 FastAPI 建置應用程式的同樣 **developer experience**，帶到把它們 **部署** 到雲端的流程中。 🎉

FastAPI Cloud 是 *FastAPI and friends* 開源專案的主要贊助者與資金提供者。 ✨

#### 部署到其他雲端供應商 { #deploy-to-other-cloud-providers }

FastAPI 是開源且基於標準。你可以把 FastAPI 應用程式部署到你選擇的任何雲端供應商。

請依照你的雲端供應商指南來部署 FastAPI 應用程式。 🤓

## 回顧 { #recap }

* 引入 `FastAPI`。
* 建立一個 `app` 實例。
* 使用像 `@app.get("/")` 這樣的裝飾器來撰寫 **路徑操作裝飾器**。
* 定義一個 **路徑操作函式**；例如 `def root(): ...`。
* 使用命令 `fastapi dev` 執行開發伺服器。
* （可選）使用 `fastapi deploy` 部署你的應用程式。
