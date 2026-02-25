# 自訂文件 UI 靜態資源（自我託管） { #custom-docs-ui-static-assets-self-hosting }

API 文件使用 Swagger UI 與 ReDoc，它們各自需要一些 JavaScript 與 CSS 檔案。

預設情況下，這些檔案會從 <abbr title="Content Delivery Network - 內容傳遞網路：一種服務，通常由多台伺服器組成，提供 JavaScript 與 CSS 等靜態檔案。常用來從更接近用戶端的伺服器提供這些檔案，以提升效能。">CDN</abbr> 提供。

但你可以自訂：你可以指定特定的 CDN，或自行提供這些檔案。

## 為 JavaScript 和 CSS 使用自訂 CDN { #custom-cdn-for-javascript-and-css }

假設你想使用不同的 <abbr title="Content Delivery Network - 內容傳遞網路">CDN</abbr>，例如使用 `https://unpkg.com/`。

若你所在的國家限制部分網址，這會很有用。

### 停用自動產生的文件 { #disable-the-automatic-docs }

第一步是停用自動文件，因為預設會使用預設的 CDN。

要停用它們，建立 `FastAPI` 應用時把相關 URL 設為 `None`：

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[8] *}

### 加入自訂文件 { #include-the-custom-docs }

現在你可以為自訂文件建立「路徑操作（path operation）」。

你可以重用 FastAPI 的內部函式來建立文件的 HTML 頁面，並傳入所需參數：

* `openapi_url`：文件 HTML 頁面用來取得你 API 的 OpenAPI schema 的 URL。可使用屬性 `app.openapi_url`。
* `title`：你的 API 標題。
* `oauth2_redirect_url`：可使用 `app.swagger_ui_oauth2_redirect_url` 以沿用預設值。
* `swagger_js_url`：Swagger UI 文件 HTML 用來取得「JavaScript」檔案的 URL。這是你的自訂 CDN 位址。
* `swagger_css_url`：Swagger UI 文件 HTML 用來取得「CSS」檔案的 URL。這是你的自訂 CDN 位址。

ReDoc 也類似...

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[2:6,11:19,22:24,27:33] *}

/// tip

當你使用 OAuth2 時，`swagger_ui_redirect` 的路徑操作是個輔助端點。

如果你把 API 與 OAuth2 提供者整合，便能完成認證並帶著取得的憑證回到 API 文件，接著以真正的 OAuth2 驗證與之互動。

Swagger UI 會在背後幫你處理，不過它需要這個「redirect」輔助端點。

///

### 建立路徑操作以進行測試 { #create-a-path-operation-to-test-it }

現在，為了測試一切是否正常，建立一個路徑操作：

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[36:38] *}

### 測試 { #test-it }

現在你應該能造訪 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>，重新載入頁面後，資源會從新的 CDN 載入。

## 自行託管文件所需的 JavaScript 與 CSS { #self-hosting-javascript-and-css-for-docs }

若你需要應用在離線、無公共網路或僅在區域網路中也能運作，自行託管 JavaScript 與 CSS 會很實用。

以下示範如何在同一個 FastAPI 應用中自行提供這些檔案，並設定文件使用它們。

### 專案檔案結構 { #project-file-structure }

假設你的專案檔案結構如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

現在建立一個目錄來存放這些靜態檔案。

新的檔案結構可能如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### 下載檔案 { #download-the-files }

下載文件所需的靜態檔案並放到 `static/` 目錄中。

你可以在各連結上按右鍵，選擇類似「另存連結為...」的選項。

Swagger UI 需要以下檔案：

* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" class="external-link" target="_blank">`swagger-ui-bundle.js`</a>
* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" class="external-link" target="_blank">`swagger-ui.css`</a>

而 ReDoc 需要以下檔案：

* <a href="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js" class="external-link" target="_blank">`redoc.standalone.js`</a>

之後，你的檔案結構可能如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### 提供靜態檔案 { #serve-the-static-files }

* 匯入 `StaticFiles`。
* 在特定路徑「掛載」一個 `StaticFiles()` 實例。

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[7,11] *}

### 測試靜態檔案 { #test-the-static-files }

啟動你的應用並前往 <a href="http://127.0.0.1:8000/static/redoc.standalone.js" class="external-link" target="_blank">http://127.0.0.1:8000/static/redoc.standalone.js</a>。

你應該會看到一個很長的 **ReDoc** JavaScript 檔案。

它可能會以如下內容開頭：

```JavaScript
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

這表示你的應用已能提供靜態檔案，且文件用的靜態檔已放在正確位置。

接著把應用設定為讓文件使用這些靜態檔。

### 為靜態檔案停用自動文件 { #disable-the-automatic-docs-for-static-files }

和使用自訂 CDN 一樣，第一步是停用自動文件，因為預設會使用 CDN。

要停用它們，建立 `FastAPI` 應用時把相關 URL 設為 `None`：

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[9] *}

### 加入使用靜態檔案的自訂文件 { #include-the-custom-docs-for-static-files }

同樣地，現在你可以為自訂文件建立路徑操作。

再次重用 FastAPI 的內部函式來建立文件的 HTML 頁面，並傳入所需參數：

* `openapi_url`：文件 HTML 頁面用來取得你 API 的 OpenAPI schema 的 URL。可使用屬性 `app.openapi_url`。
* `title`：你的 API 標題。
* `oauth2_redirect_url`：可使用 `app.swagger_ui_oauth2_redirect_url` 以沿用預設值。
* `swagger_js_url`：Swagger UI 文件 HTML 用來取得「JavaScript」檔案的 URL。這就是你的應用現在提供的檔案。
* `swagger_css_url`：Swagger UI 文件 HTML 用來取得「CSS」檔案的 URL。這就是你的應用現在提供的檔案。

ReDoc 也類似...

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[2:6,14:22,25:27,30:36] *}

/// tip

當你使用 OAuth2 時，`swagger_ui_redirect` 的路徑操作是個輔助端點。

如果你把 API 與 OAuth2 提供者整合，便能完成認證並帶著取得的憑證回到 API 文件，接著以真正的 OAuth2 驗證與之互動。

Swagger UI 會在背後幫你處理，不過它需要這個「redirect」輔助端點。

///

### 建立路徑操作以測試靜態檔案 { #create-a-path-operation-to-test-static-files }

現在，為了測試一切是否正常，建立一個路徑操作：

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[39:41] *}

### 測試使用靜態檔案的 UI { #test-static-files-ui }

現在，你應該可以關閉 WiFi，造訪你的文件 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>，並重新載入頁面。

即使沒有網際網路，也能看到你的 API 文件並與之互動。
