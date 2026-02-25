# 替代方案、靈感與比較 { #alternatives-inspiration-and-comparisons }

啟發 FastAPI 的來源、與其他方案的比較，以及從中學到的內容。

## 介紹 { #intro }

沒有前人的工作，就不會有 **FastAPI**。

在它誕生之前，已經有許多工具啟發了它的設計。

我多年來一直避免打造新框架。起初我嘗試用許多不同的框架、外掛與工具，來實作 **FastAPI** 涵蓋的所有功能。

但在某個時間點，除了創建一個能提供所有這些功能、汲取前人工具的優點，並以最佳方式組合起來、同時運用過去甚至不存在的語言特性（Python 3.6+ 的型別提示）之外，已別無他法。

## 先前的工具 { #previous-tools }

### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a> { #django }

它是最受歡迎且廣受信任的 Python 框架。像 Instagram 等系統就是用它打造的。

它與關聯式資料庫（如 MySQL 或 PostgreSQL）相對緊密耦合，因此要以 NoSQL 資料庫（如 Couchbase、MongoDB、Cassandra 等）作為主要儲存引擎並不容易。

它一開始是為在後端產生 HTML 而設計，而非為了建立提供現代前端（如 React、Vue.js、Angular）或其他系統（如 <abbr title="Internet of Things - 物聯網">IoT</abbr> 裝置）使用的 API。

### <a href="https://www.django-rest-framework.org/" class="external-link" target="_blank">Django REST Framework</a> { #django-rest-framework }

Django REST framework 的目標是成為一套在 Django 之上構建 Web API 的彈性工具組，以強化其 API 能力。

它被 Mozilla、Red Hat、Eventbrite 等眾多公司使用。

它是「自動 API 文件」的早期典範之一，而這正是啟發我「尋找」**FastAPI** 的第一個想法。

/// note | 注意

Django REST Framework 由 Tom Christie 創建。他同時也是 Starlette 與 Uvicorn 的作者，而 **FastAPI** 就是建立在它們之上。

///

/// check | 啟發 **FastAPI**

提供自動化的 API 文件網頁使用者介面。

///

### <a href="https://flask.palletsprojects.com" class="external-link" target="_blank">Flask</a> { #flask }

Flask 是一個「微框架」，它不包含資料庫整合，也沒有像 Django 那樣內建許多功能。

這種簡單與彈性，讓你可以把 NoSQL 資料庫作為主要的資料儲存系統。

由於它非常簡單，學起來相對直觀，儘管文件在某些地方會變得較技術性。

它也常用於其他不一定需要資料庫、使用者管理或 Django 內建眾多功能的應用程式。雖然這些功能中的許多都可以用外掛新增。

這種元件的解耦，以及作為可擴充以精準滿足需求的「微框架」，是我想要保留的關鍵特性。

基於 Flask 的簡潔，它看起來很適合用來構建 API。接下來要找的，就是 Flask 世界裡的「Django REST Framework」。

/// check | 啟發 **FastAPI**

成為一個微框架，讓所需的工具與元件能輕鬆搭配組合。

具備簡單、易用的路由系統。

///

### <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests</a> { #requests }

**FastAPI** 其實不是 **Requests** 的替代品。兩者的範疇截然不同。

在 FastAPI 應用程式「內部」使用 Requests 其實很常見。

儘管如此，FastAPI 仍從 Requests 得到了不少啟發。

**Requests** 是一個「與 API 互動」（作為用戶端）的程式庫，而 **FastAPI** 是一個「建立 API」（作為伺服端）的程式庫。

它們大致位於相反兩端，彼此互補。

Requests 設計非常簡單直觀、容易使用，且有合理的預設值。同時它也非常強大且可自訂。

因此，如其官網所言：

> Requests is one of the most downloaded Python packages of all time

用法非常簡單。例如，發出一個 `GET` 請求，你會寫：

```Python
response = requests.get("http://example.com/some/url")
```

相對地，FastAPI 的 API 路徑操作（path operation）可能像這樣：

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

看看 `requests.get(...)` 與 `@app.get(...)` 的相似之處。

/// check | 啟發 **FastAPI**

* 擁有簡單直觀的 API。
* 直接使用 HTTP 方法名稱（操作），以直接、直觀的方式表達。
* 具備合理的預設值，同時提供強大的自訂能力。

///

### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a> { #swagger-openapi }

我想從 Django REST Framework 得到的主要功能是自動 API 文件。

後來我發現有一個使用 JSON（或 YAML，JSON 的延伸）來描述 API 的標準，叫做 Swagger。

而且已有對 Swagger API 的網頁使用者介面。因此，只要能為 API 產生 Swagger 文件，就可以自動使用這個網頁介面。

之後 Swagger 交由 Linux 基金會管理，並更名為 OpenAPI。

因此，談到 2.0 版時常說「Swagger」，而 3+ 版則是「OpenAPI」。

/// check | 啟發 **FastAPI**

採用並使用開放的 API 規格標準，而非自訂格式。

並整合基於標準的使用者介面工具：

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>
* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>

選擇這兩個是因為它們相當受歡迎且穩定，但稍加搜尋，你會發現有數十種 OpenAPI 的替代使用者介面（都能與 **FastAPI** 一起使用）。

///

### Flask 的 REST 框架 { #flask-rest-frameworks }

有幾個 Flask 的 REST 框架，但在投入時間調查後，我發現許多已停止維護或被棄置，且存在一些關鍵問題使之不適用。

### <a href="https://marshmallow.readthedocs.io/en/stable/" class="external-link" target="_blank">Marshmallow</a> { #marshmallow }

API 系統需要的主要功能之一是資料「<dfn title="也稱為 marshalling、轉換">序列化</dfn>」，也就是把程式中的資料（Python）轉成能透過網路傳輸的形式。例如，將含有資料庫資料的物件轉成 JSON 物件、把 `datetime` 物件轉成字串等等。

API 需要的另一個重要功能是資料驗證，確保資料在特定條件下有效。例如，某個欄位必須是 `int`，而不是隨便的字串。這對於輸入資料特別有用。

沒有資料驗證系統的話，你就得在程式碼中手動逐一檢查。

這些功能正是 Marshmallow 所要提供的。它是很棒的函式庫，我之前也大量使用。

但它誕生於 Python 型別提示出現之前。因此，為了定義每個 <dfn title="資料應如何組成的定義">結構（schema）</dfn>，你需要使用 Marshmallow 提供的特定工具與類別。

/// check | 啟發 **FastAPI**

用程式碼定義能自動提供資料型別與驗證的「schemas」。

///

### <a href="https://webargs.readthedocs.io/en/latest/" class="external-link" target="_blank">Webargs</a> { #webargs }

API 所需的另一項大功能，是從傳入請求中<dfn title="讀取並轉換為 Python 資料">解析</dfn>資料。

Webargs 是在多個框架（包含 Flask）之上提供該功能的工具。

它底層使用 Marshmallow 來做資料驗證，且由同一群開發者建立。

它是一個很棒的工具，在有 **FastAPI** 之前我也經常使用。

/// info

Webargs 由與 Marshmallow 相同的開發者創建。

///

/// check | 啟發 **FastAPI**

自動驗證傳入請求資料。

///

### <a href="https://apispec.readthedocs.io/en/stable/" class="external-link" target="_blank">APISpec</a> { #apispec }

Marshmallow 與 Webargs 以外掛提供驗證、解析與序列化。

但文件仍然缺失，於是 APISpec 出現了。

它是多個框架的外掛（Starlette 也有對應外掛）。

它的作法是：你在處理路由的每個函式的 docstring 中，用 YAML 格式撰寫結構定義。

然後它會產生 OpenAPI schemas。

在 Flask、Starlette、Responder 等框架中都是這樣運作。

但這又帶來一個問題：在 Python 字串中（大型 YAML）加入一段微語法。

編輯器幫不上太多忙。而且如果我們修改了參數或 Marshmallow 的 schemas 卻忘了同步修改 YAML docstring，產生的結構就會過時。

/// info

APISpec 由與 Marshmallow 相同的開發者創建。

///

/// check | 啟發 **FastAPI**

支援 API 的開放標準 OpenAPI。

///

### <a href="https://flask-apispec.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-apispec</a> { #flask-apispec }

這是一個 Flask 外掛，把 Webargs、Marshmallow 與 APISpec 串在一起。

它使用 Webargs 與 Marshmallow 的資訊，透過 APISpec 自動產生 OpenAPI 結構。

它是個很棒但被低估的工具。它理應比許多 Flask 外掛更受歡迎，可能因為它的文件過於簡潔與抽象。

這解決了在 Python 文件字串中撰寫 YAML（另一種語法）的问题。

在打造 **FastAPI** 前，我最喜歡的後端技術組合就是 Flask、Flask-apispec、Marshmallow 與 Webargs。

使用它促成了數個 Flask 全端（full-stack）產生器。這些是我（以及若干外部團隊）至今主要使用的技術組合：

* <a href="https://github.com/tiangolo/full-stack" class="external-link" target="_blank">https://github.com/tiangolo/full-stack</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchbase</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchdb" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchdb</a>

而這些全端產生器，也成為了 [**FastAPI** 專案產生器](project-generation.md){.internal-link target=_blank} 的基礎。

/// info

Flask-apispec 由與 Marshmallow 相同的開發者創建。

///

/// check | 啟發 **FastAPI**

從定義序列化與驗證的相同程式碼，自動產生 OpenAPI 結構（schema）。

///

### <a href="https://nestjs.com/" class="external-link" target="_blank">NestJS</a>（與 <a href="https://angular.io/" class="external-link" target="_blank">Angular</a>） { #nestjs-and-angular }

這甚至不是 Python。NestJS 是受 Angular 啟發的 JavaScript（TypeScript）NodeJS 框架。

它達成的效果與 Flask-apispec 能做的有點相似。

它有一套受 Angular 2 啟發的整合式相依性注入（Dependency Injection）系統。需要預先註冊「可注入」元件（就像我所知的其他相依性注入系統一樣），因此會增加冗長與重複程式碼。

由於參數以 TypeScript 型別描述（與 Python 型別提示相似），編輯器支援相當不錯。

但因為 TypeScript 的型別在編譯成 JavaScript 後不會被保留，它無法僅靠型別同時定義驗證、序列化與文件。由於這點以及部分設計決定，若要取得驗證、序列化與自動結構產生，就需要在許多地方加上裝飾器，因此會相當冗長。

它無法很好地處理巢狀模型。若請求的 JSON 主體中有內層欄位，且這些內層欄位又是巢狀 JSON 物件，就無法被妥善地文件化與驗證。

/// check | 啟發 **FastAPI**

使用 Python 型別以獲得優秀的編輯器支援。

提供強大的相依性注入系統，並想辦法將重複程式碼降到最低。

///

### <a href="https://sanic.readthedocs.io/en/latest/" class="external-link" target="_blank">Sanic</a> { #sanic }

它是最早基於 `asyncio` 的極高速 Python 框架之一，並做得很像 Flask。

/// note | 技術細節

它使用 <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a> 取代預設的 Python `asyncio` 事件圈。這也是它如此之快的原因。

它明顯啟發了 Uvicorn 與 Starlette，而在公開的基準測試中，它們目前比 Sanic 更快。

///

/// check | 啟發 **FastAPI**

想辦法達到瘋狂的效能。

這就是為什麼 **FastAPI** 建立於 Starlette 之上，因為它是可用的最快框架（由第三方評測）。

///

### <a href="https://falconframework.org/" class="external-link" target="_blank">Falcon</a> { #falcon }

Falcon 是另一個高效能 Python 框架，設計上極簡，並作為其他框架（如 Hug）的基礎。

它設計為函式接收兩個參數，一個是「request」，一個是「response」。然後你從 request「讀取」資料、往 response「寫入」資料。由於這種設計，無法使用標準的 Python 型別提示，直接以函式參數宣告請求參數與主體。

因此，資料驗證、序列化與文件必須以程式碼手動完成，無法自動化。或者需在 Falcon 之上實作另一層框架（如 Hug）。其他受 Falcon 設計啟發的框架也有同樣的區別：將 request 與 response 物件作為參數。

/// check | 啟發 **FastAPI**

設法取得優秀的效能。

連同 Hug（Hug 建立於 Falcon 之上）一起，也啟發 **FastAPI** 在函式中宣告一個 `response` 參數。

不過在 FastAPI 中它是可選的，主要用來設定標頭、Cookie 與替代狀態碼。

///

### <a href="https://moltenframework.com/" class="external-link" target="_blank">Molten</a> { #molten }

我在 **FastAPI** 打造的早期發現了 Molten。它有一些相當類似的想法：

* 基於 Python 型別提示。
* 從這些型別取得驗證與文件。
* 相依性注入系統。

它沒有使用像 Pydantic 這樣的第三方資料驗證、序列化與文件庫，而是有自己的。因此，這些資料型別定義較不容易重複使用。

它需要更為冗長的設定。而且因為它基於 WSGI（而非 ASGI），並未設計來享受如 Uvicorn、Starlette、Sanic 等工具所提供的高效能。

其相依性注入系統需要預先註冊依賴，並且依據宣告的型別來解析依賴。因此，無法宣告多個能提供相同型別的「元件」。

路由需要在單一地方宣告，使用在其他地方宣告的函式（而不是用可以直接放在端點處理函式上方的裝飾器）。這更接近 Django 的作法，而不是 Flask（與 Starlette）的作法。它在程式碼中分離了其實相當緊密耦合的事物。

/// check | 啟發 **FastAPI**

用模型屬性的「預設值」來定義資料型別的額外驗證。這提升了編輯器支援，而這在當時的 Pydantic 還不支援。

這實際上也啟發了 Pydantic 的部分更新，以支援相同的驗證宣告風格（這些功能現在已在 Pydantic 中可用）。

///

### <a href="https://github.com/hugapi/hug" class="external-link" target="_blank">Hug</a> { #hug }

Hug 是最早使用 Python 型別提示來宣告 API 參數型別的框架之一。這是個很棒的點子，也啟發了其他工具。

它在宣告中使用自訂型別而非標準 Python 型別，但仍然是巨大的一步。

它也是最早能以 JSON 產出自訂結構、描述整個 API 的框架之一。

它不是基於 OpenAPI 與 JSON Schema 等標準。因此，與其他工具（如 Swagger UI）的整合並不直覺。但它仍是一個非常創新的想法。

它有個有趣、少見的功能：同一個框架可同時建立 API 與 CLI。

由於它基於同步 Python 網頁框架的舊標準（WSGI），無法處理 WebSocket 與其他功能，儘管效能仍然很高。

/// info

Hug 由 Timothy Crosley 創建，他同時也是 <a href="https://github.com/timothycrosley/isort" class="external-link" target="_blank">`isort`</a> 的作者，一個自動排序 Python 匯入的好工具。

///

/// check | 啟發 **FastAPI** 的想法

Hug 啟發了 APIStar 的部分設計，也是我覺得最有前景的工具之一，與 APIStar 並列。

Hug 啟發 **FastAPI** 使用 Python 型別提示宣告參數，並自動產生定義 API 的結構。

Hug 啟發 **FastAPI** 在函式中宣告 `response` 參數以設定標頭與 Cookie。

///

### <a href="https://github.com/encode/apistar" class="external-link" target="_blank">APIStar</a> (<= 0.5) { #apistar-0-5 }

在決定打造 **FastAPI** 之前，我找到了 **APIStar** 伺服器。它幾乎具備我所尋找的一切，而且設計很出色。

它是我見過最早使用 Python 型別提示來宣告參數與請求的框架實作之一（早於 NestJS 與 Molten）。我與 Hug 幾乎在同時間發現它。不過 APIStar 使用的是 OpenAPI 標準。

它基於相同的型別提示，在多處自動進行資料驗證、資料序列化與 OpenAPI 結構產生。

主體結構（body schema）的定義並未使用像 Pydantic 那樣的 Python 型別提示，更像 Marshmallow，因此編輯器支援沒有那麼好，但整體而言，APIStar 是當時最好的選擇。

它在當時的效能評測中名列前茅（僅被 Starlette 超越）。

一開始它沒有自動 API 文件的網頁 UI，但我知道我可以替它加上 Swagger UI。

它有相依性注入系統。需要預先註冊元件，與上面提到的其他工具相同。不過這仍是很棒的功能。

我從未能在完整專案中使用它，因為它沒有安全性整合，所以無法取代我用 Flask-apispec 全端產生器所擁有的全部功能。我曾把新增該功能的 pull request 放在待辦清單中。

但之後，專案的重心改變了。

它不再是 API 網頁框架，因為作者需要專注於 Starlette。

現在的 APIStar 是一套用於驗證 OpenAPI 規格的工具，不是網頁框架。

/// info

APIStar 由 Tom Christie 創建。他也創建了：

* Django REST Framework
* Starlette（**FastAPI** 建立於其上）
* Uvicorn（Starlette 與 **FastAPI** 使用）

///

/// check | 啟發 **FastAPI**

存在。

用相同的 Python 型別同時宣告多件事（資料驗證、序列化與文件），並同時提供出色的編輯器支援，這是一個極好的點子。

在長時間尋找並測試多種不同替代方案後，APIStar 是最好的可用選擇。

當 APIStar 不再作為伺服器存在，而 Starlette 誕生並成為更好的基礎時，這成為打造 **FastAPI** 的最後一個靈感。

我將 **FastAPI** 視為 APIStar 的「精神繼承者」，同時基於所有這些先前工具的經驗，改進並擴增了功能、型別系統與其他部分。

///

## **FastAPI** 所採用的工具 { #used-by-fastapi }

### <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> { #pydantic }

Pydantic 是基於 Python 型別提示，定義資料驗證、序列化與文件（使用 JSON Schema）的函式庫。

這讓它非常直覺。

它可與 Marshmallow 相提並論。儘管在效能測試中它比 Marshmallow 更快。而且因為它基於相同的 Python 型別提示，編輯器支援也很出色。

/// check | **FastAPI** 用於

處理所有資料驗證、資料序列化與自動模型文件（基於 JSON Schema）。

**FastAPI** 接著會把這些 JSON Schema 資料放入 OpenAPI 中，此外還有其他許多功能。

///

### <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> { #starlette }

Starlette 是一個輕量的 <dfn title="用於構建非同步 Python 網頁應用的新標準">ASGI</dfn> 框架／工具集，非常適合用來建構高效能的 asyncio 服務。

它非常簡單直觀。設計上易於擴充，且元件化。

它具備：

* 令人印象深刻的效能。
* WebSocket 支援。
* 行程內（in-process）背景任務。
* 啟動與關閉事件。
* 建立在 HTTPX 上的測試用戶端。
* CORS、GZip、靜態檔案、串流回應。
* Session 與 Cookie 支援。
* 100% 測試涵蓋率。
* 100% 型別註解的程式碼庫。
* 幾乎沒有硬性相依。

Starlette 目前是測試中最快的 Python 框架。僅次於 Uvicorn（它不是框架，而是伺服器）。

Starlette 提供所有網頁微框架的基礎功能。

但它不提供自動的資料驗證、序列化或文件。

這正是 **FastAPI** 在其上方加入的主要功能之一，且全部基於 Python 型別提示（使用 Pydantic）。此外還有相依性注入系統、安全性工具、OpenAPI 結構產生等。

/// note | 技術細節

ASGI 是由 Django 核心團隊成員正在開發的新「標準」。它尚未成為「Python 標準」（PEP），但他們正著手進行中。

儘管如此，它已被多個工具作為「標準」採用。這大幅提升了互通性，例如你可以把 Uvicorn 換成其他 ASGI 伺服器（如 Daphne 或 Hypercorn），或加入相容 ASGI 的工具，如 `python-socketio`。

///

/// check | **FastAPI** 用於

處理所有核心網頁部分，並在其上加上功能。

`FastAPI` 這個類別本身直接繼承自 `Starlette` 類別。

因此，凡是你能用 Starlette 做的事，你幾乎都能直接用 **FastAPI** 完成，因為它基本上就是加強版的 Starlette。

///

### <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a> { #uvicorn }

Uvicorn 是基於 uvloop 與 httptools 的極速 ASGI 伺服器。

它不是網頁框架，而是伺服器。例如，它不提供依據路徑路由的工具。這是像 Starlette（或 **FastAPI**）這樣的框架在其上方提供的功能。

它是 Starlette 與 **FastAPI** 推薦使用的伺服器。

/// check | **FastAPI** 建議用作

執行 **FastAPI** 應用的主要網頁伺服器。

你也可以使用 `--workers` 命令列選項，取得非同步的多製程伺服器。

更多細節請見[部署](deployment/index.md){.internal-link target=_blank}章節。

///

## 效能與速度 { #benchmarks-and-speed }

想了解、比較並看出 Uvicorn、Starlette 與 FastAPI 之間的差異，請參考[效能評測](benchmarks.md){.internal-link target=_blank}。
