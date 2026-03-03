# 路徑操作進階設定 { #path-operation-advanced-configuration }

## OpenAPI operationId { #openapi-operationid }

/// warning

如果你不是 OpenAPI 的「專家」，大概不需要這個。

///

你可以用參數 `operation_id` 為你的*路徑操作（path operation）*設定要使用的 OpenAPI `operationId`。

你必須確保每個操作的 `operationId` 都是唯一的。

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py310.py hl[6] *}

### 使用路徑操作函式（path operation function）的名稱作為 operationId { #using-the-path-operation-function-name-as-the-operationid }

如果你想用 API 的函式名稱作為 `operationId`，你可以遍歷所有路徑，並使用各自的 `APIRoute.name` 覆寫每個*路徑操作*的 `operation_id`。

應在加入所有*路徑操作*之後再這麼做。

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py310.py hl[2, 12:21, 24] *}

/// tip

如果你會手動呼叫 `app.openapi()`，請務必先更新所有 `operationId` 再呼叫。

///

/// warning

如果你這樣做，必須確保每個*路徑操作函式*都有唯一的名稱，

即使它們位於不同的模組（Python 檔案）中。

///

## 從 OpenAPI 排除 { #exclude-from-openapi }

若要從產生的 OpenAPI 結構（也就是自動文件系統）中排除某個*路徑操作*，使用參數 `include_in_schema` 並將其設為 `False`：

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py310.py hl[6] *}

## 從 docstring 提供進階描述 { #advanced-description-from-docstring }

你可以限制 OpenAPI 從*路徑操作函式*的 docstring 中使用的內容行數。

加上一個 `\f`（跳頁字元，form feed）會讓 FastAPI 在此處截斷用於 OpenAPI 的輸出。

這個字元不會出現在文件中，但其他工具（例如 Sphinx）仍可使用其後的內容。

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## 額外回應 { #additional-responses }

你大概已看過如何為*路徑操作*宣告 `response_model` 與 `status_code`。

這會定義該*路徑操作*主要回應的中繼資料。

你也可以宣告額外的回應及其模型、狀態碼等。

文件中有完整章節說明，請見 [OpenAPI 中的額外回應](additional-responses.md){.internal-link target=_blank}。

## OpenAPI 額外資訊 { #openapi-extra }

當你在應用程式中宣告一個*路徑操作*時，FastAPI 會自動產生該*路徑操作*的相關中繼資料，並納入 OpenAPI 結構中。

/// note | 技術細節

在 OpenAPI 規格中，這稱為 <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Operation 物件</a>。

///

它包含關於*路徑操作*的所有資訊，並用於產生自動文件。

其中包含 `tags`、`parameters`、`requestBody`、`responses` 等。

這個針對單一路徑操作的 OpenAPI 結構通常由 FastAPI 自動產生，但你也可以擴充它。

/// tip

這是一個較低階的擴充介面。

如果你只需要宣告額外回應，更方便的方式是使用 [OpenAPI 中的額外回應](additional-responses.md){.internal-link target=_blank}。

///

你可以使用參數 `openapi_extra` 來擴充某個*路徑操作*的 OpenAPI 結構。

### OpenAPI 擴充 { #openapi-extensions }

`openapi_extra` 可用來宣告例如 [OpenAPI 擴充](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions) 的資料：

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py310.py hl[6] *}

打開自動產生的 API 文件時，你的擴充會顯示在該*路徑操作*頁面的底部。

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

而在檢視產生出的 OpenAPI（位於你的 API 的 `/openapi.json`）時，也可以在相應*路徑操作*中看到你的擴充：

```JSON hl_lines="22"
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
```

### 自訂 OpenAPI 路徑操作結構 { #custom-openapi-path-operation-schema }

`openapi_extra` 中的字典會與自動產生的該*路徑操作*之 OpenAPI 結構進行深度合併。

因此你可以在自動產生的結構上加入額外資料。

例如，你可以選擇用自己的程式碼讀取並驗證請求，而不使用 FastAPI 與 Pydantic 的自動功能，但仍然希望在 OpenAPI 結構中定義該請求。

你可以透過 `openapi_extra` 辦到：

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py310.py hl[19:36, 39:40] *}

在這個範例中，我們沒有宣告任何 Pydantic 模型。事實上，請求本文甚至不會被 <dfn title="從某種純格式（例如 bytes）轉換為 Python 物件">解析</dfn> 為 JSON，而是直接以 `bytes` 讀取，並由函式 `magic_data_reader()` 以某種方式負責解析。

儘管如此，我們仍可宣告請求本文的預期結構。

### 自訂 OpenAPI Content-Type { #custom-openapi-content-type }

用同樣的方法，你可以使用 Pydantic 模型來定義 JSON Schema，並把它包含到該*路徑操作*的自訂 OpenAPI 區段中。

即使請求中的資料型別不是 JSON 也可以這麼做。

例如，在這個應用中，我們不使用 FastAPI 內建的從 Pydantic 模型擷取 JSON Schema 的功能，也不使用 JSON 的自動驗證。實際上，我們將請求的 content type 宣告為 YAML，而非 JSON：

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[15:20, 22] *}

儘管沒有使用預設的內建功能，我們仍透過 Pydantic 模型手動產生想以 YAML 接收之資料的 JSON Schema。

接著我們直接使用請求，並將本文擷取為 `bytes`。這表示 FastAPI 甚至不會嘗試把請求負載解析為 JSON。

然後在程式中直接解析該 YAML 內容，並再次使用相同的 Pydantic 模型來驗證該 YAML 內容：

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[24:31] *}

/// tip

這裡我們重複使用同一個 Pydantic 模型。

不過也可以用其他方式進行驗證。

///
