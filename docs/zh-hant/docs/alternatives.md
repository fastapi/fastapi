# 替代方案、啟發與比較

是甚麼啟發了 **FastAPI**， 它與其他替代方案的比較，以及它從中學到了什麼。

## 前言

如果不是因為前人的努力，**FastAPI** 就不會因此而存在。

在 **FastAPI** 之前有許多工具被創造出來，這些工具啟發了它的誕生。

多年來，我一直避免創建一個新的框架。最初，我嘗試使用許多不同的框架、插件和工具來解決 FastAPI 所涵蓋的所有功能。

但在某個時間點，除了創造一個能夠提供所有這些功能的工具之外，已經沒有其他選擇了。這個工具從之前的工具中汲取了最好的想法，並以最佳的方式將它們結合起來，同時利用了以前無法使用的語言特性（Python 3.6+ 的型別提示）。

## 先前的工具

### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a>

Django 是最受歡迎的 Python 框架，並且廣受信任。它被用來構建像 Instagram 這樣的系統。

它與關聯式資料庫（如 MySQL 或 PostgreSQL）的耦合度較高，因此將 NoSQL 資料庫（如 Couchbase、MongoDB、Cassandra 等）作為主要儲存引擎並不容易。

Django 的設計初衷是為了在後端生成 HTML，而不是為了建立供現代前端（如 React、Vue.js 和 Angular）或其他系統 (類似 <abbr title="Internet of Things">IoT</abbr> devices）使用的 API。

### <a href="https://www.django-rest-framework.org/" class="external-link" target="_blank">Django REST Framework</a>

Django REST Framework 是為了在 Django 的基礎上建構 Web API 而建立的靈活工具包，旨在提升其 API 功能。

它被許多公司使用，包括 Mozilla、Red Hat 和 Eventbrite。

它是自動生成 API 文件的早期範例之一，而這正是啟發「探索」FastAPI 的第一個想法之一。

/// note | 筆記

Django REST Framework 是 Tom Christie 所發明，他同時研發了 Starlette 和 Uvicorn，兩者皆是基於 **FastAPI**。

///

/// check | 啟發了 **FastAPI**

提供自動生成的 API 文件化網頁使用者介面（Web UI）。

///

### <a href="https://flask.palletsprojects.com" class="external-link" target="_blank">Flask</a>

Flask 是一個「微框架」，它並未內建資料庫整合功能，也不包含 Django 中預設提供的許多功能。

這種簡潔與靈活性，使得使用 NoSQL 資料庫作為主要資料儲存系統。

由於其設計極為簡潔，學習起來相對直觀，儘管其文件在某些部分仍需要點技術。

它也常被用於其他不一定需要資料庫、用戶管理或 Django 中預建的眾多功能之應用程式。儘管這些功能中的許多可以透過擴充套件來添加。

這種模組化的設計，以及作為一個可擴展以滿足特定需求的「微框架」，正是我希望保留的關鍵特性。

鑑於 Flask 的簡潔性，它似乎是構建 API 的理想選擇。接下來要尋找的，便是 Flask 的「Django REST Framework」。

/// check | 啟發了 **FastAPI**

成為微框架，使其能夠輕鬆組合和搭配所需的工具與元件。

具備簡單且易於使用的路由系統。

///

### <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests</a>

**FastAPI** 實際上並不是 Requests 的替代品。它們的應用範圍截然不同。

實際上，在 FastAPI 應用程式內部使用 Requests 是很常見的做法。

然而，FastAPI 仍然從 Requests 中獲得了不少靈感。

**Requests** 是一個用於與 API 互動（作為客戶端）的函式庫，而 **FastAPI** 則是一個用於構建 API（作為伺服器）的函式庫。

它們在某種程度上處於對立的兩端，彼此互補。

Requests 的設計非常簡潔且直觀，易於使用，並具有合理的預設值。但同時，它也非常強大且可自定義。

這就是為什麼官方網站上這樣說：

> Requests 是有史以來下載量最多的 Python 套件之一

它的使用方式非常簡單。例如，要發送一個 'GET' 請求，你可以這樣寫：

```Python
response = requests.get("http://example.com/some/url")
```

FastAPI 的對應 API 路徑操作可能會像這樣：

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

觀察 `requests.get(...)` 和 `@app.get(...)`的相似程度。

/// check | 啟發了 **FastAPI**

* 擁有一個簡單且直觀的 API。
* 在一個直觀且明確的方式，直接使用 HTTP 的 method names (operations)。
* 提供合理的預設值，同時具備強大的自定義功能。

///

### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a>

我從 Django REST Framework 中想要的主要功能是自動生成 API 文件。

後來我發現有一種標準可以用來記錄 API，使用 JSON（或 YAML，為 JSON 的擴展）來描述，稱為 Swagger。

而且已經有人為 Swagger API 創建了一個網頁用戶界面。因此，能夠為 API 生成 Swagger 文件，就能自動使用這個網頁用戶界面。

後來，Swagger 被移交給了 Linux 基金會，並更名為 OpenAPI。

這就是為什麼在談到 2.0 版本時，人們通常會說「Swagger」，而對於 3+ 版本則會說「OpenAPI」。

/// check | 啟發了 **FastAPI**

採用並使用 API 規範的開放標準，而非自定義的架構。

並整合基於標準的用戶介面工具：

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>
* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>

這兩者之所以被選中，是因為它們相當流行且穩定，但若稍加搜尋，你會發現有數十種適用於 OpenAPI 的替代用戶介面（你也可以在 **FastAPI** 中使用這些工具）。

///

### Flask REST Framework

市面上有多種 Flask 的 REST 框架，但在投入時間與精力進行調查後，我發現其中許多已經停止維護或被棄置，並且存在一些無法忽視的問題，使其難以滿足需求。

### <a href="https://marshmallow.readthedocs.io/en/stable/" class="external-link" target="_blank">Marshmallow</a>

API 系統所需的主要功能之一是數據 "<abbr title="又稱為marshalling、轉換">serialization</abbr>" 這是指將數據從程式碼（如 Python）中取出，並轉換成可以透過網路傳送的格式。例如，將包含資料庫數據的物件轉換為 JSON 物件，或將 'datetime' 物件轉換為字串等。

另一個 API 所需的重要功能是數據驗證，確保數據符合特定條件。例如，確保某個欄位是 int 類型，而不是隨機的字串。這對於接收的數據特別有用。

如果沒有數據驗證系統，你必須手動在程式碼中進行所有檢查。

這些功能正是 Marshmallow 所提供的主要功能。它是一個非常優秀的函式庫，我之前也經常使用它。

但 Marshmallow 是在 Python 型別提示（type hints）出現之前建立的。因此，要定義每個 <abbr title="數據應如何被組成的定義">schema</abbr> 你必須使用 Marshmallow 提供的特定工具和類別。

/// check | 啟發了 **FastAPI**

使用程式碼自動定義「模式」（schemas），以提供資料型別與驗證功能。

///

### <a href="https://webargs.readthedocs.io/en/latest/" class="external-link" target="_blank">Webargs</a>

API 的一個重要功能是從請求中解析 "<abbr title="讀取並轉換 Python 資料">parsing</abbr>" 資料，並將其轉換為 Python 可用的格式。

Webargs 是一款能夠在多種框架（包括 Flask）上提供此功能的工具。

它內部使用 Marshmallow 來執行資料驗證，並且與 Marshmallow 出自相同的開發團隊。

這是一款優秀的工具，在 **FastAPI** 問世之前，我也曾大量使用它。

/// info | 資訊

Webargs 由與 Marshmallow 相同的開發團隊打造。

///

/// check | 啟發了 **FastAPI**

實現對請求資料的自動驗證功能。

///

### <a href="https://apispec.readthedocs.io/en/stable/" class="external-link" target="_blank">APISpec</a>

Marshmallow 和 Webargs 提供驗證、解析與序列化作為插件。

但仍然缺乏文件化功能，於是 APISpec 應運而生。

它是一個適用於多個框架的插件（Starlette 也有對應的插件）。

其運作方式是開發者在處理路由的函式內，透過 docstring 以 YAML 格式撰寫結構定義，然後 APISpec 會根據這些定義產生 OpenAPI 規範。

這種方式適用於 Flask、Starlette、Responder 等框架。

然而，這又帶來了一個問題，即需要在 Python 字串內使用 YAML 這種微語法。

編輯器對此的支援有限，並且如果修改了參數或 Marshmallow 的 schema 而忘記更新 YAML docstring，則生成的 API 文件可能會過時。

/// info | 資訊

APISpec 是 Marshmallow 相同的開發團隊所創建。

///

/// check | 啟發了 **FastAPI**

支援 API 的開放標準 OpenAPI。

///

### <a href="https://flask-apispec.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-apispec</a>

這是一個 Flask 的擴充套件，將 Webargs、Marshmallow 和 APISpec 整合在一起。

它利用 Webargs 和 Marshmallow 提供的數據驗證與解析功能，透過 APISpec 自動產生 OpenAPI 規範。

這是一個極為實用但尚未廣受關注的工具。它應該比許多 Flask 插件更受歡迎，可能因為其文件過於簡潔和抽象。

此工具解決了在 Python docstring 內撰寫 YAML（另一種語法）的問題。

在 **FastAPI** 出現之前，我最喜歡的後端技術組合就是 Flask、Flask-apispec 搭配 Marshmallow 和 Webargs。

這套技術組合促成了多個 Flask 全端應用程式生成器的開發，我與多個外部團隊長期使用這些技術:

* <a href="https://github.com/tiangolo/full-stack" class="external-link" target="_blank">https://github.com/tiangolo/full-stack</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchbase</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchdb" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchdb</a>

這些全端應用程式生成器也是 [**FastAPI** Project Generators](project-generation.md){.internal-link target=_blank} 的基礎。

/// info | 資訊

Flask-apispec 由與 Marshmallow 相同的開發團隊所創建。

///

/// check | 啟發了 **FastAPI**

從原本的定義序列化與驗證的程式碼中，自動生成 OpemAPI schema。

///

### <a href="https://nestjs.com/" class="external-link" target="_blank">NestJS</a> (and <a href="https://angular.io/" class="external-link" target="_blank">Angular</a>)

這甚至不是 Python 框架，NestJS 是一個基於 JavaScript（TypeScript）的 Node.js 框架，靈感來自 Angular。

它實現了類似於 Flask-apispec 的功能。

它內建一套依賴注入（Dependency Injection）系統，靈感來自 Angular 2。與其他依賴注入系統一樣，它需要事先註冊「可注入項目（injectables）」，這導致程式碼變得更冗長且重複。

因為參數是用 TypeScript 型別（類似 Python 型別提示）來描述的，因此編輯器支援相當良好。

但由於 TypeScript 型別在編譯後不會保留於 JavaScript，因此無法同時用來定義驗證、序列化與文件化。

由於這一點及其他設計考量，要實現驗證、序列化與自動模式生成，需要在許多地方添加裝飾器，這導致程式碼變得冗長。

此外，它無法很好地處理巢狀模型。如果請求中的 JSON 主體包含內部欄位，而這些內部欄位本身又是巢狀的 JSON 物件，那麼這些巢狀結構可能無法正確地被文件化與驗證。

/// check | 啟發了 **FastAPI**

使用 Python 型別來獲得更強大的編輯器支援。

設計一個強大的依賴注入系統，並設法減少程式碼重複。

///

### <a href="https://sanic.readthedocs.io/en/latest/" class="external-link" target="_blank">Sanic</a>

這是一個基於 `asyncio` 極快的 Python 框架，與 Flask 非常相似。

/// note | 技術層面細節

它使用了 <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a> 而非 Python 預設的 `asyncio` loop。這也是讓它速度之快的原因。

它很明顯的啟發了 Uvicorn 和 Starlette，兩者在效能測試速度皆優於 Sanic。

///

/// check | 啟發了 **FastAPI**

找到一個可以有非常高效能的方法。

這也是為甚麼 **FastAPI** 是基於 Starlette，因為它是目前最快的框架(由第三方效能測試測試後)。

///

### <a href="https://falconframework.org/" class="external-link" target="_blank">Falcon</a>

Falcon 是另一個高效能的 Python 框架，設計簡潔，並作為 Hug 等其他框架的基礎。

它的設計方式是讓函式接收兩個參數：「請求（request）」與「回應（response）」，然後從請求中讀取數據，並寫入回應。

因此，無法使用標準 Python 型別註記來宣告請求參數與主體。 數據驗證、序列化與文件化必須手動編寫，或是透過像 Hug 這類基於 Falcon 的框架來實現。

/// check | 啟發了 **FastAPI**

尋找方法以獲得優秀的效能。

與 Hug 一樣（因為 Hug 是基於 Falcon 的），啟發 FastAPI 讓函式可選擇性地使用 response 參數來設置標頭、cookie 和狀態碼。

///

### <a href="https://moltenframework.com/" class="external-link" target="_blank">Molten</a>

我在建立 FastAPI 的初期發現了 Molten，它的設計理念與 FastAPI 相當相似：

* 基於 Python 型別註解（type hints）。
* 透過型別自動執行驗證與文件生成。
* 內建依賴注入系統。

然而，Molten 並未採用像 Pydantic 這樣的第三方資料驗證、序列化與文件生成工具，而是內建了一套自己的解決方案。因此，定義的資料型別無法像 Pydantic 那樣輕鬆地被重複使用。

此外，Molten 需要較為冗長的設定，且它是基於 WSGI（而非 ASGI），因此無法充分利用 Uvicorn、Starlette 和 Sanic 等工具所提供的高效能特性。

Molten 的相依性注入系統要求先行註冊所有相依性，並且是根據所宣告的型別來解析相依性。因此，不允許有多個「元件」提供相同的型別。

路由定義則是集中在單一位置，並使用在其他地方定義的函式來處理請求，而非像 Flask 或 Starlette 那樣透過裝飾器（decorator）直接將路由與處理函式綁定在一起。這種方式與 Django 的作法較為相似，但它將程式碼中關聯性較高的部分分開處理，可能影響可讀性與維護性。

/// check | 啟發了 **FastAPI**

Molten 的一個設計概念啟發了 FastAPI 允許透過模型屬性的「預設值」來定義額外的資料驗證規則。這樣的做法能夠提升編輯器的支援度，而在當時的 Pydantic 中尚未支援。

此概念後來也促使 Pydantic 進行改進，加入了相同的驗證宣告風格。目前，Pydantic 已經完全支援此功能。

///

### <a href="https://github.com/hugapi/hug" class="external-link" target="_blank">Hug</a>

Hug 是最早使用 Python 型別提示（type hints） 來宣告 API 參數類型的框架之一。這個創新理念啟發了許多後續工具的發展。

雖然 Hug 使用的是自訂型別而非標準 Python 型別，但這仍然是一大進步。

Hug 也是最早支援 自動生成 API 架構（schema） 的框架之一，能夠以 JSON 格式定義整個 API。

然而，Hug 沒有基於 OpenAPI 或 JSON Schema 標準，這使得它較難與 Swagger UI 等其他工具整合。但即便如此，它仍然是一個相當創新的設計。

Hug 也具備一個罕見而有趣的功能：同時支援 API 與 CLI 應用程式的開發，讓開發者可以用相同的框架來構建不同類型的應用。

由於 Hug 採用了 WSGI（同步 Python Web 框架的舊標準），它無法處理 WebSockets 等非同步功能，但仍然具有高效能。

/// info | 資訊

Hug 由 Timothy Crosley 創建，他同時也是 <a href="https://github.com/timothycrosley/isort" class="external-link" target="_blank">`isort`</a> 的作者。
是一款自動整理 Python import 語句的優秀工具。

///

/// check | 一些啟發 **FastAPI** 的點子

Hug 啟發了 APIStar 的部分設計，也與 APIStar 一起，成為當時最具潛力的框架之一。

Hug 的創新理念對 FastAPI 產生了直接影響，特別是使用 Python 型別提示來宣告參數，以及自動生成 API 架構（schema）。

此外，Hug 也啟發了 **FastAPI** 在函式中宣告 `response` 參數，以設定 回應標頭（headers）與 cookies。

///

### <a href="https://github.com/encode/apistar" class="external-link" target="_blank">APIStar</a> (<= 0.5)

在我打算建構 **FastAPI** 前我發現了 **APIStar** 伺服器。它擁有了幾乎我所需要的一切功能，而且還有良好的設計。

它是我見過最早使用 Python 型別提示（type hints）來宣告參數與請求的框架之一（比 NestJS 和 Molten 還早）。我大約在發現 Hug 的同時也接觸到了它。但 APIStar 採用了 OpenAPI 標準。

它能夠自動進行資料驗證、資料序列化，並且根據相同的型別提示在多個地方生成 OpenAPI 架構（schema）。

不過，APIStar 的請求體（Body）架構定義並不像 Pydantic 那樣直接使用 Python 型別提示，而是更接近 Marshmallow。因此，編輯器的支援性相對較差，但即便如此，當時 APIStar 仍是最好的選擇。

當時，它的基準測試（Benchmark）表現最佳，只有 Starlette 能超越它。

最初，它沒有自動生成 API 文件的 Web UI，但我知道可以手動加入 Swagger UI 來補足這項功能。

它也具備依賴注入（Dependency Injection）系統，雖然需要事先註冊元件（與前面提到的工具類似），但這仍然是一個相當實用的功能。

然而，我從未能在完整的專案中使用它，因為它沒有內建安全性整合，無法取代我當時透過 Flask-apispec 全端生成器所具備的完整功能。我原本計畫提交一個 Pull Request 來新增這項功能，但後來，這個專案的發展方向發生了變化。

它不再是一個 API Web 框架，因為作者需要專注於 Starlette。

如今，APIStar 只是一組用來驗證 OpenAPI 規範的工具，而不再是 Web 框架了。

/// note | 筆記

APIStar 是由 Tom Christie 創建的。他同時也是以下專案的作者：

* Django REST Framework
* Starlette (**FastAPI** 的基礎)
* Uvicorn (被 Starlette 和 **FastAPI** 使用)

///

/// check | 啟發了 **FastAPI**

在 Python 型別中同時宣告資料驗證、序列化和文件生成，並且提供極佳的編輯器支援，這對我來說是個天才般的設計。

我花了很長時間尋找類似的框架，並測試了許多不同的選擇，當時 APIStar 是最好的選項。

然而，APIStar 最終停止作為伺服器框架存在，而 Starlette 被創建，成為這類系統的新且更好的基礎。這成為我開發 **FastAPI** 的最終靈感來源。

我將 **FastAPI** 視為 APIStar 的「精神續作」，並在其基礎上改進與擴展功能、型別系統及其他部分，吸取了所有這些前人工具的經驗與優點。

///

## 被 **FastAPI** 所使用的

### <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>

Pydantic 是一個基於 Python 型別提示（type hints）來定義資料驗證、序列化與文件（使用 JSON Schema）的函式庫。

這讓它變得極為直觀易用。

它可與 Marshmallow 相提並論，但在效能測試中表現更快。此外，因為它同樣基於 Python 型別提示，編輯器支援性極佳。

/// check | **FastAPI** 透過 Pydantic 來處理：

資料驗證、 資料序列化和自動生成模型文件（基於 JSON Schema)。

接著，**FastAPI** 會將這些 JSON Schema 數據整合進 OpenAPI，除了這些功能外，還執行許多其他任務。

///

### <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a>

Starlette 是一個輕量級的 ASGI <abbr title="The new standard for building asynchronous Python web applications">ASGI</abbr> 框架/工具集，非常適合用來構建高效能的 asyncio 服務。

它設計簡單直觀，易於擴展，並擁有模組化的元件。

Starlette 的特色:

* 極佳的效能表現
* 支援 WebSocket
* 內部背景任務（In-process background tasks）
* 應用啟動與關閉事件（Startup & shutdown events）
* 基於 HTTPX 的測試客戶端
* 支援 CORS、GZip、靜態文件、串流回應
* 內建 Session 與 Cookie 支援
* 100% 測試覆蓋率
* 100% 型別註解（Type Annotation）代碼
* 極少的硬性依賴

Starlette 是目前測試過最快的 Python 框架，唯一能超越它的是 Uvicorn，但 Uvicorn 並非框架，而是伺服器。

Starlette 提供所有基礎的 Web 微框架功能。

但它不具備自動資料驗證、序列化或文件生成功能。

這正是 **FastAPI** 在其基礎上額外提供的關鍵特性，透過 Pydantic 與 Python 型別提示來實現。此外，**FastAPI** 還加入了 依賴注入系統、內建安全工具、OpenAPI 架構生成 等功能，使其更強大與易用。


/// note | 技術層面細節

ASGI 是由 Django 核心團隊成員開發的一種新的「標準」，目前尚未正式成為 Python 官方標準（PEP），但相關流程已在進行中。

儘管如此，ASGI 已經被許多工具採用為標準，大幅提升了不同工具間的互通性。 例如，你可以用 Daphne 或 Hypercorn 來替換 Uvicorn，或者加入 ASGI 相容工具，像 `python-socketio`.

///

/// check | **FastAPI** 使用它來

FastAPI 使用 ASGI 來處理所有核心的 Web 功能，並在其基礎上增加額外功能。

其 `FastAPI` 類別直接繼承自 `Starlette`類別。

因此，任何可以在 Starlette 上做的事情，都可以直接在 **FastAPI** 上做，因為 FastAPI 本質上就是增強版的 Starlette。

///

### <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>

Uvicorn 是一款極速的 ASGI 伺服器，基於 uvloop 和 httptools 架構而成。

它並不是一個網頁框架，而是一個伺服器。例如，它不提供路徑導向的路由功能，這部分需要像 Starlette 或 **FastAPI** 這類框架來實現。


Uvicorn 是 Starlette 和 **FastAPI** 官方推薦的伺服器。

/// check | **FastAPI** recommends it as

運行 **FastAPI** 應用程式的主要網頁伺服器。

此外，你還可以使用 `--workers` 指令選項，啟動非同步的多行程伺服器，以提升效能。

更多詳細資訊請參考[部署](deployment/index.md){.internal-link target=_blank}章節。

///

## 效能測試與速度

如需瞭解、比較並觀察 Uvicorn, Starlette 和 FastAPI，請前往[基準測試](benchmarks.md){.internal-link target=_blank}.
