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
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**文件**： <a href="https://fastapi.tiangolo.com/zh-hant" target="_blank">https://fastapi.tiangolo.com</a>

**原始碼**： <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI 是一個現代、快速（高效能）的 Web 框架，用於以 Python（基於標準 Python 型別提示）建構 API。

主要特點包含：

* **快速**： 非常高的效能，可與 **NodeJS** 和 **Go** 效能相當（歸功於 Starlette 和 Pydantic）。[可用的最快 Python 框架之一](#performance)。
* **快速撰寫程式碼**： 提高開發功能的速度約 200% 至 300%。 *
* **更少的 Bug**： 減少約 40% 的人為（開發者）導致的錯誤。 *
* **直覺**： 具有出色的編輯器支援。處處都有<abbr title="也被稱為自動完成、自動補全、IntelliSense">Completion</abbr>。更少的除錯時間。
* **簡單**： 設計上易於使用和學習。更少的閱讀文件時間。
* **簡潔**： 最小化程式碼重複性。每個參數宣告即可獲得多項功能。更少的 Bug。
* **穩健**： 立即獲得可用於生產環境的程式碼，並有自動生成的互動式文件。
* **基於標準**： 基於（且完全相容於）API 的開放標準：<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a>（之前被稱為 Swagger）與 <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>。

<small>* 基於內部開發團隊在建立生產應用程式時所做測試的估算。</small>

## 贊助 { #sponsors }

<!-- sponsors -->

### Keystone 贊助商 { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### 金級與銀級贊助商 { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/zh-hant/fastapi-people/#sponsors" class="external-link" target="_blank">其他贊助商</a>

## 評價 { #opinions }

"_[...] 近期大量使用 **FastAPI**。[...] 我其實正計畫把它用在我們團隊在 **Microsoft 的所有 ML 服務**中。其中一些正在整合到核心的 **Windows** 產品和一些 **Office** 產品。_"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_我們採用 **FastAPI** 函式庫來啟動一個可被查詢以取得**預測**的 **REST** 伺服器。[for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** 很榮幸宣布開源我們的**危機管理**協調框架：**Dispatch**！[使用 **FastAPI** 建構]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_我對 **FastAPI** 興奮得不得了。它太有趣了！_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_老實說，你建造的東西看起來非常堅固且精緻。在很多方面，這就是我希望 **Hug** 成為的樣子——看到有人建造出來真的很鼓舞人心。_"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_如果你想學一個用來建構 REST API 的**現代框架**，看看 **FastAPI** [...] 它很快、易於使用且易於學習 [...]_"

"_我們的 **API** 已經改用 **FastAPI** [...] 我想你會喜歡它 [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> 創辦人 - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_如果有人想要建立一個生產環境的 Python API，我強烈推薦 **FastAPI**。它**設計精美**、**使用簡單**且**高度可擴充**，已成為我們 API 優先開發策略中的**關鍵組件**，並且驅動了許多自動化與服務，例如我們的 Virtual TAC Engineer。_"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## FastAPI 迷你紀錄片 { #fastapi-mini-documentary }

在 2025 年底發布了一部 <a href="https://www.youtube.com/watch?v=mpR8ngthqiE" class="external-link" target="_blank">FastAPI 迷你紀錄片</a>，你可以線上觀看：

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE" target="_blank"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**，CLI 的 FastAPI { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

如果你不是在開發 Web API，而是在開發一個要在終端機中使用的 <abbr title="Command Line Interface">CLI</abbr> 應用程式，不妨試試 <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>。

**Typer** 是 FastAPI 的小兄弟，並且旨在成為 **CLI 的 FastAPI**。 ⌨️ 🚀

## 安裝需求 { #requirements }

FastAPI 是站在以下巨人的肩膀上：

* <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> 負責 Web 的部分。
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 負責資料的部分。

## 安裝 { #installation }

建立並啟用一個 <a href="https://fastapi.tiangolo.com/zh-hant/virtual-environments/" class="external-link" target="_blank">虛擬環境</a>，然後安裝 FastAPI：

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**注意**：請確認你把 `"fastapi[standard]"` 放在引號中，以確保它能在所有終端機中正常運作。

## 範例 { #example }

### 建立 { #create-it }

建立一個檔案 `main.py`，內容如下：

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>或使用 <code>async def</code>...</summary>

如果你的程式使用 `async` / `await`，請使用 `async def`：

```Python hl_lines="9  14"
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**注意**：

如果你不確定，請查看文件中 _"In a hurry?"_ 章節關於 <a href="https://fastapi.tiangolo.com/zh-hant/async/#in-a-hurry" target="_blank">`async` 和 `await`</a> 的說明。

</details>

### 運行 { #run-it }

使用以下指令運行伺服器：

<div class="termy">

```console
$ fastapi dev main.py

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
<summary>關於指令 <code>fastapi dev main.py</code>...</summary>

指令 `fastapi dev` 會讀取你的 `main.py` 檔案，偵測其中的 **FastAPI** app，並使用 <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a> 啟動伺服器。

預設情況下，`fastapi dev` 會啟用自動重新載入，方便本機開發。

你可以在 <a href="https://fastapi.tiangolo.com/zh-hant/fastapi-cli/" target="_blank">FastAPI CLI 文件</a> 了解更多。

</details>

### 檢查 { #check-it }

使用瀏覽器開啟 <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>。

你將會看到以下 JSON 回應：

```JSON
{"item_id": 5, "q": "somequery"}
```

你已經建立了一個具有以下功能的 API：

* 在 _路徑_ `/` 與 `/items/{item_id}` 接收 HTTP 請求。
* 兩個 _路徑_ 都使用 `GET` <em>操作</em>（也稱為 HTTP _方法_）。
* _路徑_ `/items/{item_id}` 有一個 _路徑參數_ `item_id`，其型別應為 `int`。
* _路徑_ `/items/{item_id}` 有一個選填的 `str` _查詢參數_ `q`。

### 互動式 API 文件 { #interactive-api-docs }

現在前往 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你會看到自動生成的互動式 API 文件（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 替代 API 文件 { #alternative-api-docs }

接著前往 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

你會看到替代的自動文件（由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 範例升級 { #example-upgrade }

現在修改 `main.py` 檔案來接收 `PUT` 請求的 body。

藉由 Pydantic，你可以使用標準 Python 型別來宣告 body。

```Python hl_lines="4  9-12  25-27"
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

`fastapi dev` 伺服器應該會自動重新載入。

### 互動式 API 文件升級 { #interactive-api-docs-upgrade }

現在前往 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

* 互動式 API 文件會自動更新，並包含新的 body：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* 點擊 "Try it out" 按鈕，你可以填寫參數並直接與 API 互動：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* 然後點擊 "Execute" 按鈕，使用者介面會與你的 API 溝通，送出參數、取得結果並顯示在畫面上：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### 替代 API 文件升級 { #alternative-api-docs-upgrade }

接著前往 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

* 替代文件也會反映新的查詢參數與 body：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 總結 { #recap }

總結來說，你只需要**一次**像函式參數一樣，宣告參數、body 等的型別。

你使用的是標準、現代的 Python 型別。

你不需要學習新的語法、特定函式庫的方法或類別等。

只要標準的 **Python**。

例如，一個 `int`：

```Python
item_id: int
```

或一個更複雜的 `Item` model：

```Python
item: Item
```

...透過這一次宣告，你將獲得：

* 編輯器支援，包含：
    * 自動補全。
    * 型別檢查。
* 資料驗證：
    * 當資料無效時，自動且清楚地回報錯誤。
    * 即使是深層巢狀的 JSON 物件也能驗證。
* <abbr title="也被稱為： 序列化、解析、封送處理">Conversion</abbr>輸入資料：將來自網路的資料轉換為 Python 資料與型別。可從以下讀取：
    * JSON。
    * 路徑參數。
    * 查詢參數。
    * Cookies。
    * Headers。
    * Forms。
    * Files。
* <abbr title="也被稱為： 序列化、解析、封送處理">Conversion</abbr>輸出資料：將 Python 資料與型別轉換為網路資料（JSON）：
    * 轉換 Python 型別（`str`、`int`、`float`、`bool`、`list` 等）。
    * `datetime` 物件。
    * `UUID` 物件。
    * 資料庫 models。
    * ...以及更多。
* 自動生成的互動式 API 文件，包含 2 種替代的使用者介面：
    * Swagger UI。
    * ReDoc。

---

回到前面的程式碼範例，**FastAPI** 還會：

* 驗證 `GET` 與 `PUT` 請求的路徑中是否包含 `item_id`。
* 驗證 `GET` 與 `PUT` 請求的 `item_id` 是否為 `int` 型別。
    * 如果不是，用戶端會看到有用且清楚的錯誤。
* 檢查 `GET` 請求是否有名為 `q` 的選填查詢參數（例如 `http://127.0.0.1:8000/items/foo?q=somequery`）。
    * 因為 `q` 參數宣告為 `= None`，所以它是選填的。
    * 若沒有 `None`，它就會是必填（就像 `PUT` 的 body 一樣）。
* 對 `PUT` 請求 `/items/{item_id}`，將 body 讀取為 JSON：
    * 檢查是否有必填屬性 `name` 且其型別應為 `str`。
    * 檢查是否有必填屬性 `price` 且其型別必須為 `float`。
    * 檢查是否有選填屬性 `is_offer`，若存在其型別應為 `bool`。
    * 以上也適用於深層巢狀的 JSON 物件。
* 自動在 JSON 之間做轉換（進出）。
* 使用 OpenAPI 記錄所有內容，可用於：
    * 互動式文件系統。
    * 支援多種語言的自動用戶端程式碼生成系統。
* 直接提供 2 種互動式文件 Web 介面。

---

雖然我們只觸及表面，但你已經理解它是如何運作的。

試著修改這一行：

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...從：

```Python
        ... "item_name": item.name ...
```

...改成：

```Python
        ... "item_price": item.price ...
```

...然後看看你的編輯器如何自動補全屬性，並知道它們的型別：

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

要看包含更多功能的完整範例，請參考 <a href="https://fastapi.tiangolo.com/zh-hant/tutorial/">教學 - 使用者指南</a>。

**劇透警告**：教學 - 使用者指南包含：

* 從不同位置宣告**參數**，例如：**headers**、**cookies**、**form 欄位**和**檔案**。
* 如何設定 **驗證限制**，例如 `maximum_length` 或 `regex`。
* 強大且易用的 **<abbr title="也被稱為元件、資源、提供者、服務或是可注入物">Dependency Injection</abbr>** 系統。
* 安全性與身份驗證，包含支援 **OAuth2**、**JWT tokens** 與 **HTTP Basic** 驗證。
* 更進階（但同樣簡單）的技巧，用於宣告**深層巢狀的 JSON models**（歸功於 Pydantic）。
* 與 <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> 及其他函式庫的 **GraphQL** 整合。
* 許多額外功能（歸功於 Starlette），例如：
    * **WebSockets**
    * 基於 HTTPX 與 `pytest` 的極其簡單測試
    * **CORS**
    * **Cookie Sessions**
    * ...以及更多。

### 部署你的 app（可選） { #deploy-your-app-optional }

你也可以選擇將 FastAPI app 部署到 <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>；如果你還沒加入候補名單，可以前往加入。 🚀

如果你已經有 **FastAPI Cloud** 帳號（我們已從候補名單邀請你 😉），你可以用一個指令部署你的應用程式。

部署前，請確保你已登入：

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

接著部署你的 app：

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

就這樣！現在你可以透過該 URL 存取你的 app。 ✨

#### 關於 FastAPI Cloud { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** 是由 **FastAPI** 背後的同一位作者與團隊打造。

它以最少的投入，大幅簡化 **建構**、**部署** 與 **存取** API 的流程。

它把使用 FastAPI 建構 app 的相同 **developer experience**，也帶到了把它們**部署**到雲端的過程。 🎉

FastAPI Cloud 是 *FastAPI and friends* 開源專案的主要贊助商與資金提供者。 ✨

#### 部署到其他雲端供應商 { #deploy-to-other-cloud-providers }

FastAPI 是開源並基於標準的。你可以將 FastAPI app 部署到任何你選擇的雲端供應商。

請依照你的雲端供應商指南來部署 FastAPI app。 🤓

## 效能 { #performance }

來自獨立機構 TechEmpower 的測試顯示，在 Uvicorn 下執行的 **FastAPI** 應用程式是 <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">可用的最快 Python 框架之一</a>，僅次於 Starlette 和 Uvicorn 本身（FastAPI 內部使用）。（*）

想了解更多，請參考 <a href="https://fastapi.tiangolo.com/zh-hant/benchmarks/" class="internal-link" target="_blank">測試結果</a>。

## 依賴 { #dependencies }

FastAPI 依賴 Pydantic 與 Starlette。

### `standard` 依賴 { #standard-dependencies }

當你使用 `pip install "fastapi[standard]"` 安裝 FastAPI 時，它會包含 `standard` 這組選填依賴：

由 Pydantic 使用：

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - 用於電子郵件驗證。

由 Starlette 使用：

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - 若你想使用 `TestClient`，則必須安裝。
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - 若你想使用預設的 template 設定，則必須安裝。
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - 若你想透過 `request.form()` 支援表單 <abbr title="將來自 HTTP 請求的字串轉換為 Python 資料">"parsing"</abbr>，則必須安裝。

由 FastAPI 使用：

* <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> - 用於載入與提供應用程式的伺服器。這包含 `uvicorn[standard]`，其內含一些用於高效能服務所需的依賴（例如 `uvloop`）。
* `fastapi-cli[standard]` - 用於提供 `fastapi` 指令。
    * 其中包含 `fastapi-cloud-cli`，可讓你將 FastAPI 應用程式部署到 <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>。

### 不含 `standard` 依賴 { #without-standard-dependencies }

如果你不想包含 `standard` 選填依賴，你可以使用 `pip install fastapi`（而不是 `pip install "fastapi[standard]"`）來安裝。

### 不含 `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

如果你想安裝含標準依賴但不含 `fastapi-cloud-cli` 的 FastAPI，你可以使用 `pip install "fastapi[standard-no-fastapi-cloud-cli]"` 安裝。

### 額外的選填依賴 { #additional-optional-dependencies }

你可能還會想安裝一些額外的依賴。

Pydantic 額外選填依賴：

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - 用於設定管理。
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - 用於與 Pydantic 一起使用的額外型別。

FastAPI 額外選填依賴：

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - 若你想使用 `ORJSONResponse`，則必須安裝。
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - 若你想使用 `UJSONResponse`，則必須安裝。

## 授權 { #license }

此專案以 MIT 授權條款授權。
