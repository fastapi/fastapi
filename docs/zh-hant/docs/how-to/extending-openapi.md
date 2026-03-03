# 擴充 OpenAPI { #extending-openapi }

有些情況你可能需要修改自動產生的 OpenAPI 結構（schema）。

本章將示範如何做。

## 一般流程 { #the-normal-process }

一般（預設）的流程如下。

`FastAPI` 應用程式（實例）有一個 `.openapi()` 方法，會回傳 OpenAPI 結構。

在建立應用物件時，會同時註冊一個 `/openapi.json`（或你在 `openapi_url` 設定的路徑）的路徑操作（path operation）。

這個路徑只會回傳一個 JSON 回應，內容就是應用的 `.openapi()` 方法結果。

預設情況下，`.openapi()` 會先檢查 `.openapi_schema` 屬性是否已有內容，有的話就直接回傳。

若沒有，則會呼叫 `fastapi.openapi.utils.get_openapi` 這個工具函式來產生。

`get_openapi()` 函式會接收以下參數：

* `title`：OpenAPI 的標題，會顯示在文件中。
* `version`：你的 API 版本，例如 `2.5.0`。
* `openapi_version`：所使用的 OpenAPI 規格版本。預設為最新版本：`3.1.0`。
* `summary`：API 的簡短摘要。
* `description`：API 的描述，可包含 Markdown，會顯示在文件中。
* `routes`：路由列表，也就是所有已註冊的路徑操作。來源為 `app.routes`。

/// info

`summary` 參數在 OpenAPI 3.1.0 以上可用，且需 FastAPI 0.99.0 以上版本支援。

///

## 覆寫預設行為 { #overriding-the-defaults }

基於上述資訊，你可以用相同的工具函式來產生 OpenAPI 結構，並覆寫你需要客製的部分。

例如，我們要加入 <a href="https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo" class="external-link" target="_blank">ReDoc 的 OpenAPI 擴充，插入自訂 logo</a>。

### 一般的 **FastAPI** { #normal-fastapi }

先照常撰寫你的 **FastAPI** 應用：

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[1,4,7:9] *}

### 產生 OpenAPI 結構 { #generate-the-openapi-schema }

接著，在 `custom_openapi()` 函式內，使用相同的工具函式來產生 OpenAPI 結構：

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[2,15:21] *}

### 修改 OpenAPI 結構 { #modify-the-openapi-schema }

現在可以加入 ReDoc 擴充，在 OpenAPI 結構的 `info`「物件」中新增自訂的 `x-logo`：

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[22:24] *}

### 快取 OpenAPI 結構 { #cache-the-openapi-schema }

你可以把 `.openapi_schema` 屬性當作「快取」來儲存已產生的結構。

這樣使用者每次開啟 API 文件時，應用就不必重複產生結構。

結構只會產生一次，之後的請求都會使用相同的快取結果。

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[13:14,25:26] *}

### 覆寫方法 { #override-the-method }

現在你可以用新的函式取代 `.openapi()` 方法。

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[29] *}

### 檢查看看 { #check-it }

造訪 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> 後，你會看到自訂的 logo（此例為 **FastAPI** 的 logo）：

<img src="/img/tutorial/extending-openapi/image01.png">
