# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/zh-hant"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI 框架，高效能，易於學習，快速開發，適用於生產環境</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**文件**： [https://fastapi.tiangolo.com/zh-hant](https://fastapi.tiangolo.com/zh-hant)

**程式碼**： [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI 是一個現代、快速（高效能）的 Web 框架，用於以 Python 並基於標準的 Python 型別提示來構建 API。

主要特點包含：

* **快速**：非常高的效能，可與 **NodeJS** 和 **Go** 相當（歸功於 Starlette 和 Pydantic）。[最快的 Python 框架之一](#performance)。
* **極速開發**：開發功能的速度可提升約 200% 至 300%。*
* **更少的 Bug**：減少約 40% 的人為（開發者）錯誤。*
* **直覺**：具有出色的編輯器支援，處處都有 <dfn title="也稱為：自動完成、自動補全、IntelliSense">自動補全</dfn>。更少的偵錯時間。
* **簡單**：設計上易於使用與學習。更少的讀文件時間。
* **簡潔**：最小化程式碼重複性。每個參數宣告可帶來多個功能。更少的錯誤。
* **穩健**：立即獲得可投入生產的程式碼，並自動生成互動式文件。
* **標準化**：基於（且完全相容於）API 的開放標準：[OpenAPI](https://github.com/OAI/OpenAPI-Specification)（之前稱為 Swagger）和 [JSON Schema](https://json-schema.org/)。

<small>* 基於內部開發團隊在建立生產應用程式時的測試預估。</small>

## 贊助 { #sponsors }

<!-- sponsors -->

### 基石贊助商 { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### 金級與銀級贊助商 { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

[其他贊助商](https://fastapi.tiangolo.com/zh-hant/fastapi-people/#sponsors)

## 評價 { #opinions }

"_[...] 近期大量使用 **FastAPI**。[...] 我實際上打算在我在**微軟**團隊的所有**機器學習**服務上使用它。其中一些正在整合到核心的 **Windows** 產品，以及一些 **Office** 產品。_"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(ref)</small></a></div>

---

"_我們採用了 **FastAPI** 函式庫來啟動一個 **REST** 伺服器，供查詢以取得**預測**。[for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/"><small>(ref)</small></a></div>

---

"_**Netflix** 很高興宣布我們的**危機管理**協調框架 **Dispatch** 開源！[使用 **FastAPI** 建構]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(ref)</small></a></div>

---

"_我對 **FastAPI** 興奮得不得了。超好玩！_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong>[Python Bytes](https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855) podcast 主持人</strong> <a href="https://x.com/brianokken/status/1112220079972728832"><small>(ref)</small></a></div>

---

"_老實說，你們做的看起來非常穩健又精緻。很多方面都正是我希望 **Hug** 成為的樣子——看到有人把它建出來真的很鼓舞人心。_"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong>[Hug](https://github.com/hugapi/hug) 創作者</strong> <a href="https://news.ycombinator.com/item?id=19455465"><small>(ref)</small></a></div>

---

"_如果你想學一個用於構建 REST API 的**現代框架**，看看 **FastAPI** [...] 它很快、易用、也容易學習 [...]_"

"_我們的 **API** 已經改用 **FastAPI** [...] 我想你會喜歡它 [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong>[Explosion AI](https://explosion.ai) 創辦人 - [spaCy](https://spacy.io) 創作者</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680"><small>(ref)</small></a></div>

---

"_如果有人想要打造一個可用於生產環境的 Python API，我強力推薦 **FastAPI**。它**設計優雅**、**簡單易用**且**高度可擴展**，已經成為我們 API first 開發策略中的**關鍵元件**，推動了許多自動化與服務，例如我們的 Virtual TAC Engineer。_"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(ref)</small></a></div>

---

## FastAPI 迷你紀錄片 { #fastapi-mini-documentary }

在 2025 年底發布了一支 [FastAPI 迷你紀錄片](https://www.youtube.com/watch?v=mpR8ngthqiE)，你可以在線上觀看：

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**，命令列的 FastAPI { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

如果你不是在做 Web API，而是要建立一個在終端機中使用的 <abbr title="Command Line Interface - 命令列介面">CLI</abbr> 應用程式，可以看看 [**Typer**](https://typer.tiangolo.com/)。

**Typer** 是 FastAPI 的小老弟。他立志成為命令列世界的 **FastAPI**。⌨️ 🚀

## 需求 { #requirements }

FastAPI 是站在以下巨人的肩膀上：

* [Starlette](https://www.starlette.dev/) 負責 Web 部分。
* [Pydantic](https://docs.pydantic.dev/) 負責資料部分。

## 安裝 { #installation }

建立並啟用一個[虛擬環境](https://fastapi.tiangolo.com/zh-hant/virtual-environments/)，然後安裝 FastAPI：

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**注意**：請務必將 `"fastapi[standard]"` 用引號包起來，以確保在所有終端機中都能正常運作。

## 範例 { #example }

### 建立 { #create-it }

建立檔案 `main.py`，內容如下：

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>或使用 <code>async def</code>...</summary>

如果你的程式碼使用 `async` / `await`，請使用 `async def`：

```Python hl_lines="7  12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

**注意**：

如果你不確定，請查看文件中 _"In a hurry?"_ 章節的[關於文件中的 `async` 與 `await`](https://fastapi.tiangolo.com/zh-hant/async/#in-a-hurry)。

</details>

### 運行 { #run-it }

使用以下指令運行伺服器：

<div class="termy">

```console
$ fastapi dev

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>關於指令 <code>fastapi dev</code>...</summary>

指令 `fastapi dev` 會讀取你的 `main.py`，偵測其中的 **FastAPI** 應用，並使用 [Uvicorn](https://www.uvicorn.dev) 啟動伺服器。

預設情況下，`fastapi dev` 會在本機開發時啟用自動重新載入。

可在 [FastAPI CLI 文件](https://fastapi.tiangolo.com/zh-hant/fastapi-cli/)中閱讀更多資訊。

</details>

### 檢查 { #check-it }

使用瀏覽器開啟 [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery)。

你將會看到以下 JSON 回應：

```JSON
{"item_id": 5, "q": "somequery"}
```

你已經建立了一個具有以下功能的 API：

* 透過路徑 `/` 和 `/items/{item_id}` 接受 HTTP 請求。
* 以上兩個路徑都接受 `GET` <em>操作</em>（也被稱為 HTTP _方法_）。
* 路徑 `/items/{item_id}` 有一個 `int` 型別的路徑參數 `item_id`。
* 路徑 `/items/{item_id}` 有一個可選的 `str` 查詢參數 `q`。

### 互動式 API 文件 { #interactive-api-docs }

接著前往 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

你會看到自動生成的互動式 API 文件（由 [Swagger UI](https://github.com/swagger-api/swagger-ui) 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 替代 API 文件 { #alternative-api-docs }

現在前往 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)。

你會看到另一種自動文件（由 [ReDoc](https://github.com/Rebilly/ReDoc) 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 範例升級 { #example-upgrade }

現在修改 `main.py` 檔案，使其能從 `PUT` 請求接收 body。

多虧了 Pydantic，你可以用標準的 Python 型別來宣告 body。

```Python hl_lines="2  7-10 23-25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

`fastapi dev` 伺服器應會自動重新載入。

### 互動式 API 文件升級 { #interactive-api-docs-upgrade }

前往 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

* 互動式 API 文件會自動更新，包含新的 body：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* 點擊「Try it out」按鈕，你可以填寫參數並直接與 API 互動：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* 然後點擊「Execute」按鈕，使用者介面會與你的 API 溝通、送出參數、取得結果並顯示在螢幕上：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### 替代 API 文件升級 { #alternative-api-docs-upgrade }

現在前往 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)。

* 替代文件也會反映新的查詢參數與 body：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 總結 { #recap }

總結來說，你只需在函式參數中**一次**宣告參數、body 等的型別。

你使用的是現代標準的 Python 型別。

你不需要學新的語法、特定函式庫的方法或類別，等等。

就用標準的 **Python**。

例如，對於一個 `int`：

```Python
item_id: int
```

或是一個更複雜的 `Item` 模型：

```Python
item: Item
```

…透過一次宣告，你將獲得：

* 編輯器支援，包括：
    * 自動補全。
    * 型別檢查。
* 資料驗證：
    * 當資料無效時，自動且清楚的錯誤。
    * 即使是深度巢狀的 JSON 物件也能驗證。
* 輸入資料的 <dfn title="也稱為：序列化、解析、封送">轉換</dfn>：從網路讀入到 Python 資料與型別。包含：
    * JSON。
    * 路徑參數。
    * 查詢參數。
    * Cookies。
    * 標頭。
    * 表單。
    * 檔案。
* 輸出資料的 <dfn title="也稱為：序列化、解析、封送">轉換</dfn>：從 Python 資料與型別轉換為網路資料（JSON）：
    * 轉換 Python 型別（`str`、`int`、`float`、`bool`、`list` 等）。
    * `datetime` 物件。
    * `UUID` 物件。
    * 資料庫模型。
    * ...還有更多。
* 自動生成的互動式 API 文件，包含 2 種替代的使用者介面：
    * Swagger UI。
    * ReDoc。

---

回到前面的程式碼範例，**FastAPI** 會：

* 驗證 `GET` 與 `PUT` 請求的路徑中是否包含 `item_id`。
* 驗證 `GET` 與 `PUT` 請求中的 `item_id` 是否為 `int` 型別。
    * 如果不是，客戶端會看到清楚有用的錯誤。
* 在 `GET` 請求中檢查是否有名為 `q` 的可選查詢參數（如 `http://127.0.0.1:8000/items/foo?q=somequery`）。
    * 因為 `q` 參數被宣告為 `= None`，所以它是可選的。
    * 若沒有 `None`，則它會是必填（就像 `PUT` 時的 body）。
* 對於 `/items/{item_id}` 的 `PUT` 請求，以 JSON 讀取 body：
    * 檢查是否有必填屬性 `name`，且為 `str`。
    * 檢查是否有必填屬性 `price`，且為 `float`。
    * 檢查是否有可選屬性 `is_offer`，若存在則應為 `bool`。
    * 以上也適用於深度巢狀的 JSON 物件。
* 自動在 JSON 與 Python 之間轉換。
* 以 OpenAPI 記錄所有內容，可用於：
    * 互動式文件系統。
    * 為多種語言自動產生用戶端程式碼的系統。
* 直接提供兩種互動式文件網頁介面。

---

我們只觸及了表面，但你已經了解它的運作方式了。

試著把這一行：

```Python
    return {"item_name": item.name, "item_id": item_id}
```

…從：

```Python
        ... "item_name": item.name ...
```

…改為：

```Python
        ... "item_price": item.price ...
```

…然後看看你的編輯器如何自動補全屬性並知道它們的型別：

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

若想看包含更多功能的完整範例，請參考 <a href="https://fastapi.tiangolo.com/zh-hant/tutorial/">Tutorial - User Guide</a>。

**劇透警告**：教學 - 使用者指南包含：

* 來自不同來源的**參數**宣告：例如 **headers**、**cookies**、**form fields** 和 **files**。
* 如何設定**驗證限制**，如 `maximum_length` 或 `regex`。
* 一個非常強大且易用的 **<dfn title="也稱為：components、resources、providers、services、injectables">依賴注入</dfn>** 系統。
* 安全與驗證，包含支援 **OAuth2** 搭配 **JWT tokens** 與 **HTTP Basic** 驗證。
* 宣告**深度巢狀 JSON 模型**的進階（但同樣簡單）技巧（感謝 Pydantic）。
* 與 [Strawberry](https://strawberry.rocks) 及其他函式庫的 **GraphQL** 整合。
* 許多額外功能（感謝 Starlette），例如：
    * **WebSockets**
    * 基於 HTTPX 與 `pytest` 的極其簡單的測試
    * **CORS**
    * **Cookie Sessions**
    * ...以及更多。

### 部署你的應用（可選） { #deploy-your-app-optional }

你也可以選擇將 FastAPI 應用部署到 [FastAPI Cloud](https://fastapicloud.com)，如果你還沒加入，去登記等候名單吧。🚀

如果你已經有 **FastAPI Cloud** 帳號（我們已從等候名單邀請你 😉），你可以用一個指令部署你的應用。

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

就這樣！現在你可以在該 URL 造訪你的應用。✨

#### 關於 FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** 由 **FastAPI** 的同一位作者與團隊打造。

它讓你以最小的努力精簡地完成 API 的**建置**、**部署**與**存取**流程。

它把用 FastAPI 開發應用的**開發者體驗**帶到**部署**到雲端的流程中。🎉

FastAPI Cloud 是「FastAPI 與好朋友們」這些開源專案的主要贊助與資金來源。✨

#### 部署到其他雲端供應商 { #deploy-to-other-cloud-providers }

FastAPI 是開源且基於標準。你可以把 FastAPI 應用部署到任何你選擇的雲端供應商。

依照你雲端供應商的指南來部署 FastAPI 應用吧。🤓

## 效能 { #performance }

獨立的 TechEmpower 基準測試顯示，在 Uvicorn 下運行的 **FastAPI** 應用是[最快的 Python 框架之一](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7)，僅次於 Starlette 與 Uvicorn 本身（FastAPI 內部使用它們）。(*)

想了解更多，請參閱[測試結果](https://fastapi.tiangolo.com/zh-hant/benchmarks/)。

## 依賴套件 { #dependencies }

FastAPI 依賴 Pydantic 與 Starlette。

### `standard` 依賴套件 { #standard-dependencies }

當你以 `pip install "fastapi[standard]"` 安裝 FastAPI 時，會包含 `standard` 這組可選依賴套件：

Pydantic 會使用：

* [`email-validator`](https://github.com/JoshData/python-email-validator) - 用於電子郵件驗證。

Starlette 會使用：

* [`httpx`](https://www.python-httpx.org) - 若要使用 `TestClient` 必須安裝。
* [`jinja2`](https://jinja.palletsprojects.com) - 若要使用預設的模板設定必須安裝。
* [`python-multipart`](https://github.com/Kludex/python-multipart) - 若要支援表單 <dfn title="將來自 HTTP 請求的字串轉換為 Python 資料">"解析"</dfn>，搭配 `request.form()`。

FastAPI 會使用：

* [`uvicorn`](https://www.uvicorn.dev) - 用於載入並服務你的應用的伺服器。這包含 `uvicorn[standard]`，其中含有一些高效能服務所需的依賴（例如 `uvloop`）。
* `fastapi-cli[standard]` - 提供 `fastapi` 指令。
    * 其中包含 `fastapi-cloud-cli`，可讓你將 FastAPI 應用部署到 [FastAPI Cloud](https://fastapicloud.com)。

### 不含 `standard` 依賴套件 { #without-standard-dependencies }

如果你不想包含 `standard` 可選依賴，可以改用 `pip install fastapi`（而不是 `pip install "fastapi[standard]"`）。

### 不含 `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

如果你想安裝帶有 standard 依賴、但不包含 `fastapi-cloud-cli`，可以使用 `pip install "fastapi[standard-no-fastapi-cloud-cli]"`。

### 額外可選依賴套件 { #additional-optional-dependencies }

有些額外依賴你可能也會想安裝。

Pydantic 的額外可選依賴：

* [`pydantic-settings`](https://docs.pydantic.dev/latest/usage/pydantic_settings/) - 設定管理。
* [`pydantic-extra-types`](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/) - 與 Pydantic 一起使用的額外型別。

FastAPI 的額外可選依賴：

* [`orjson`](https://github.com/ijl/orjson) - 若要使用 `ORJSONResponse` 必須安裝。
* [`ujson`](https://github.com/esnme/ultrajson) - 若要使用 `UJSONResponse` 必須安裝。

## 授權 { #license }

本專案以 MIT 授權條款釋出。
