# 路徑操作設定 { #path-operation-configuration }

你可以在你的「路徑操作裝飾器」中傳入多個參數來進行設定。

/// warning | 警告

請注意，這些參數是直接傳給「路徑操作裝飾器」，而不是傳給你的「路徑操作函式」。

///

## 回應狀態碼 { #response-status-code }

你可以為「路徑操作」的回應設定 (HTTP) `status_code`。

你可以直接傳入整數代碼，例如 `404`。

如果不記得每個數字代碼代表什麼，你可以使用 `status` 中的速記常數：

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

該狀態碼會用於回應，並被加入至 OpenAPI 結構描述中。

/// note | 技術細節

你也可以使用 `from starlette import status`。

**FastAPI** 提供與 `starlette.status` 相同的 `fastapi.status`，僅為了方便你這位開發者，但它其實直接來自 Starlette。

///

## 標籤 { #tags }

你可以為「路徑操作」加入標籤，傳入參數 `tags`，其值為由 `str` 組成的 `list`（通常只是一個 `str`）：

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

這些標籤會被加入到 OpenAPI 結構描述，並由自動化文件介面使用：

<img src="/img/tutorial/path-operation-configuration/image01.png">

### 含 Enum 的標籤 { #tags-with-enums }

如果你的應用很大，可能會累積數個標籤，你會希望對相關的「路徑操作」始終使用相同的標籤。

在這種情況下，可以考慮把標籤存放在 `Enum` 中。

**FastAPI** 對此的支援方式與使用普通字串相同：

{* ../../docs_src/path_operation_configuration/tutorial002b_py310.py hl[1,8:10,13,18] *}

## 摘要與描述 { #summary-and-description }

你可以加入 `summary` 與 `description`：

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[17:18] *}

## 從 docstring 取得描述 { #description-from-docstring }

由於描述常常較長、跨越多行，你可以在函式的 <dfn title="用於文件的多行字串，作為函式內的第一個運算式（不賦值給任何變數）">文件字串（docstring）</dfn> 中宣告「路徑操作」的描述，**FastAPI** 會從那裡讀取。

你可以在 docstring 中書寫 <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a>，它會被正確解析並顯示（會考慮 docstring 的縮排）。

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

這會用於互動式文件：

<img src="/img/tutorial/path-operation-configuration/image02.png">

## 回應描述 { #response-description }

你可以用參數 `response_description` 指定回應的描述：

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[18] *}

/// info | 資訊

請注意，`response_description` 專指回應，而 `description` 則是針對整個「路徑操作」的一般描述。

///

/// check | 檢查

OpenAPI 規範要求每個「路徑操作」都必須有一個回應描述。

因此，如果你未提供，**FastAPI** 會自動產生 "Successful response"。

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## 將「路徑操作」標記為已棄用 { #deprecate-a-path-operation }

若需要將「路徑操作」標記為 <dfn title="已過時，建議不要再使用">已棄用</dfn>，但不移除它，請傳入參數 `deprecated`：

{* ../../docs_src/path_operation_configuration/tutorial006_py310.py hl[16] *}

在互動式文件中，它會被清楚標示為已棄用：

<img src="/img/tutorial/path-operation-configuration/image04.png">

比較已棄用與未棄用的「路徑操作」在文件中的呈現：

<img src="/img/tutorial/path-operation-configuration/image05.png">

## 總結 { #recap }

你可以透過將參數傳給「路徑操作裝飾器」，輕鬆地設定並為你的「路徑操作」加入中繼資料。
