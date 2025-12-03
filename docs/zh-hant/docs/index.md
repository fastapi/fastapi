<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
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

**文件**： <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**程式碼**： <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI 是一個現代、快速（高效能）的 web 框架，用於 Python 並採用標準 Python 型別提示。

主要特點包含：

- **快速**： 非常高的效能，可與 **NodeJS** 和 **Go** 效能相當 (歸功於 Starlette and Pydantic)。 [FastAPI 是最快的 Python web 框架之一](#performance)。
- **極速開發**： 提高開發功能的速度約 200% 至 300%。 \*
- **更少的 Bug**： 減少約 40% 的人為（開發者）導致的錯誤。 \*
- **直覺**： 具有出色的編輯器支援，處處都有<abbr title="也被稱為自動完成、IntelliSense">自動補全</abbr>以減少偵錯時間。
- **簡單**： 設計上易於使用和學習，大幅減少閱讀文件的時間。
- **簡潔**： 最小化程式碼重複性。可以通過不同的參數聲明來實現更豐富的功能，和更少的錯誤。
- **穩健**： 立即獲得生產級可用的程式碼，還有自動生成互動式文件。
- **標準化**： 基於 (且完全相容於) OpenAPIs 的相關標準：<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a>（之前被稱為 Swagger）和<a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>。

<small>\* 基於內部開發團隊在建立生產應用程式時的測試預估。</small>

## 贊助

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">其他贊助商</a>

## 評價

"_[...] 近期大量的使用 **FastAPI**。 [...] 目前正在計畫在**微軟**團隊的**機器學習**服務中導入。其中一些正在整合到核心的 **Windows** 產品和一些 **Office** 產品。_"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_我們使用 **FastAPI** 來建立產生**預測**結果的 **REST** 伺服器。 [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** 很榮幸地宣布開源**危機管理**協調框架： **Dispatch**! [是使用 **FastAPI** 建構]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_我對 **FastAPI** 興奮得不得了。它太有趣了！_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_老實說，你建造的東西看起來非常堅固和精緻。在很多方面，這就是我想要的，看到有人建造它真的很鼓舞人心。_"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_如果您想學習一種用於構建 REST API 的**現代框架**，不能錯過 **FastAPI** [...] 它非常快速、且易於使用和學習 [...]_"

"_我們的 **APIs** 已經改用 **FastAPI** [...] 我想你會喜歡它 [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> 創辦人 - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_如果有人想要建立一個生產環境的 Python API，我強烈推薦 **FastAPI**，它**設計精美**，**使用簡單**且**高度可擴充**，它已成為我們 API 優先開發策略中的**關鍵組件**，並且驅動了許多自動化服務，例如我們的 Virtual TAC Engineer。_"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**，命令列中的 FastAPI

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

如果你不是在開發網頁 API，而是正在開發一個在終端機中運行的<abbr title="Command Line Interface">命令列</abbr>應用程式，不妨嘗試 <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>。

**Typer** 是 FastAPI 的小兄弟。他立志成為命令列的 **FastAPI**。 ⌨️ 🚀

## 安裝需求

FastAPI 是站在以下巨人的肩膀上：

- <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> 負責網頁的部分
- <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 負責資料的部分

## 安裝

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

你同時也會需要 ASGI 伺服器用於生產環境，像是 <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a> 或 <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>。

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## 範例

### 建立

- 建立一個 python 檔案 `main.py`，並寫入以下程式碼：

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
<summary>或可以使用 <code>async def</code>...</summary>

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

如果你不知道是否會用到，可以查看 _"In a hurry?"_ 章節中，關於 <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` 和 `await` 的部分</a>。

</details>

### 運行

使用以下指令運行伺服器：

<div class="termy">

```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>關於指令 <code>uvicorn main:app --reload</code>...</summary>

該指令 `uvicorn main:app` 指的是：

- `main`：`main.py` 檔案（一個 python 的 "模組"）。
- `app`：在 `main.py` 檔案中，使用 `app = FastAPI()` 建立的物件。
- `--reload`：程式碼更改後會自動重新啟動，請僅在開發時使用此參數。

</details>

### 檢查

使用瀏覽器開啟 <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>。

你將會看到以下的 JSON 回應：

```JSON
{"item_id": 5, "q": "somequery"}
```

你已經建立了一個具有以下功能的 API：

- 透過路徑 `/` 和 `/items/{item_id}` 接受 HTTP 請求。
- 以上路經都接受 `GET` <em>請求</em>（也被稱為 HTTP _方法_）。
- 路徑 `/items/{item_id}` 有一個 `int` 型別的 `item_id` 參數。
- 路徑 `/items/{item_id}` 有一個 `str` 型別的查詢參數 `q`。

### 互動式 API 文件

使用瀏覽器開啟 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你會看到自動生成的互動式 API 文件（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> 生成）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### ReDoc API 文件

使用瀏覽器開啟 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

你將看到 ReDoc 文件 (由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 生成)：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 範例升級

現在繼續修改 `main.py` 檔案，來接收一個帶有 body 的 `PUT` 請求。

我們使用 Pydantic 來使用標準的 Python 型別聲明請求。

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

伺服器將自動重新載入（因為在上一步中，你向 `uvicorn` 指令添加了 `--reload` 的選項）。

### 互動式 API 文件升級

使用瀏覽器開啟 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

- 互動式 API 文件會自動更新，並加入新的 body 請求：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

- 點擊 "Try it out" 按鈕， 你可以填寫參數並直接與 API 互動：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

- 然後點擊 "Execute" 按鈕，使用者介面將會向 API 發送請求，並將結果顯示在螢幕上：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### ReDoc API 文件升級

使用瀏覽器開啟 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

- ReDoc API 文件會自動更新，並加入新的參數和 body 請求：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 總結

總結來說， 你就像宣告函式的參數型別一樣，只宣告了一次請求參數和請求主體參數等型別。

你使用 Python 標準型別來完成聲明。

你不需要學習新的語法、類別、方法或函式庫等等。

只需要使用 **Python 以上的版本**。

舉個範例，比如宣告 int 的型別：

```Python
item_id: int
```

或是一個更複雜的 `Item` 模型：

```Python
item: Item
```

在進行一次宣告後，你將獲得：

- 編輯器支援：
    - 自動補全
    - 型別檢查
- 資料驗證：
    - 驗證失敗時自動生成清楚的錯誤訊息
    - 可驗證多層巢狀的 JSON 物件
- <abbr title="也被稱為： 序列化或解析">轉換</abbr>輸入的資料： 轉換來自網路請求到 Python 資料型別。包含以下數據：
    - JSON
    - 路徑參數
    - 查詢參數
    - Cookies
    - 請求標頭
    - 表單
    - 文件
- <abbr title="也被稱為： 序列化或解析">轉換</abbr>輸出的資料： 轉換 Python 資料型別到網路傳輸的 JSON：
    - 轉換 Python 型別 (`str`、 `int`、 `float`、 `bool`、 `list` 等)
    - `datetime` 物件
    - `UUID` 物件
    - 數據模型
    - ...還有其他更多
- 自動生成的 API 文件，包含 2 種不同的使用介面：
    - Swagger UI
    - ReDoc

---

回到前面的的程式碼範例，**FastAPI** 還會：

- 驗證 `GET` 和 `PUT` 請求路徑中是否包含 `item_id`。
- 驗證 `GET` 和 `PUT` 請求中的 `item_id` 是否是 `int` 型別。
    - 如果驗證失敗，將會返回清楚有用的錯誤訊息。
- 查看 `GET` 請求中是否有命名為 `q` 的查詢參數 (例如 `http://127.0.0.1:8000/items/foo?q=somequery`)。
    - 因為 `q` 參數被宣告為 `= None`，所以是選填的。
    - 如果沒有宣告 `None`，則此參數將會是必填 (例如 `PUT` 範例的請求 body)。
- 對於 `PUT` 的請求 `/items/{item_id}`，將會讀取 body 為 JSON：
    - 驗證是否有必填屬性 `name` 且型別是 `str`。
    - 驗證是否有必填屬性 `price` 且型別是 `float`。
    - 驗證是否有選填屬性 `is_offer` 且型別是 `bool`。
    - 以上驗證都適用於多層次巢狀 JSON 物件。
- 自動轉換 JSON 格式。
- 透過 OpenAPI 文件來記錄所有內容，可以被用於：
    - 互動式文件系統。
    - 自動為多種程式語言生成用戶端的程式碼。
- 提供兩種交互式文件介面。

---

雖然我們只敘述了表面的功能，但其實你已經理解了它是如何執行。

試著修改以下程式碼：

```Python
    return {"item_name": item.name, "item_id": item_id}
```

從：

```Python
        ... "item_name": item.name ...
```

修改為：

```Python
        ... "item_price": item.price ...
```

然後觀察你的編輯器，會自動補全並且還知道他們的型別：

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

有關更多功能的完整範例，可以參考 <a href="https://fastapi.tiangolo.com/tutorial/">教學 - 使用者指南</a>。

**劇透警告**： 教學 - 使用者指南內容有：

- 對來自不同地方的**參數**進行宣告：像是 **headers**, **cookies**, **form 表單**以及**上傳檔案**。
- 如何設定 **驗證限制** 像是 `maximum_length` or `regex`。
- 簡單且非常容易使用的 **<abbr title="也被稱為元件、資源、提供者、服務或是注入">依賴注入</abbr>** 系統。
- 安全性和身份驗證，包含提供支援 **OAuth2**、**JWT tokens** 和 **HTTP Basic** 驗證。
- 更進階 (但同樣簡單) 的宣告 **多層次的巢狀 JSON 格式** (感謝 Pydantic)。
- **GraphQL** 與 <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> 以及其他的相關函式庫進行整合。
- 更多其他的功能 (感謝 Starlette) 像是：
    - **WebSockets**
    - 於 HTTPX 和 `pytest` 的非常簡單測試
    - **CORS**
    - **Cookie Sessions**
    - ...以及更多

## 效能

來自獨立機構 TechEmpower 的測試結果，顯示在 Uvicorn 執行下的 **FastAPI** 是 <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">最快的 Python 框架之一</a>， 僅次於 Starlette 和 Uvicorn 本身 (兩者是 FastAPI 的底層)。 (\*)

想了解更多訊息，可以參考 <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">測試結果</a>。

## 可選的依賴套件

用於 Pydantic：

- <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - 用於電子郵件驗證。
- <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - 用於設定管理。
- <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - 用於與 Pydantic 一起使用的額外型別。

用於 Starlette：

- <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - 使用 `TestClient`時必須安裝。
- <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - 使用預設的模板配置時必須安裝。
- <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - 需要使用 `request.form()` 對表單進行<abbr title="轉換來自表單的 HTTP 請求到 Python 資料型別"> "解析" </abbr>時安裝。
- <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - 需要使用 `SessionMiddleware` 支援時安裝。
- <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - 用於支援 Starlette 的 `SchemaGenerator` (如果你使用 FastAPI，可能不需要它)。

用於 FastAPI / Starlette：

- <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> - 用於加載和運行應用程式的服務器。
- <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - 使用 `ORJSONResponse`時必須安裝。
- <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - 使用 `UJSONResponse` 時必須安裝。

你可以使用 `pip install "fastapi[all]"` 來安裝這些所有依賴套件。

## 授權

該項目遵循 MIT 許可協議。
