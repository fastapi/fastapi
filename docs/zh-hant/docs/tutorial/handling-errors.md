# 錯誤處理 { #handling-errors }

在許多情況下，你需要通知使用你 API 的用戶端發生錯誤。

這個用戶端可能是帶有前端的瀏覽器、他人的程式碼、IoT 裝置等。

你可能需要告訴用戶端：

* 用戶端沒有足夠權限執行該操作。
* 用戶端沒有權限存取該資源。
* 用戶端嘗試存取的項目不存在。
* 等等。

在這些情況下，通常會回傳範圍為 400（400 到 499）的 HTTP 狀態碼。

這類似於 200 範圍的 HTTP 狀態碼（200 到 299）。那些「200」狀態碼表示請求在某種程度上是「成功」的。

400 範圍的狀態碼表示用戶端錯誤。

還記得那些「404 Not Found」錯誤（和梗）嗎？

## 使用 `HTTPException` { #use-httpexception }

要向用戶端回傳帶有錯誤的 HTTP 回應，使用 `HTTPException`。

### 匯入 `HTTPException` { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[1] *}

### 在程式中 raise 一個 `HTTPException` { #raise-an-httpexception-in-your-code }

`HTTPException` 是一般的 Python 例外，但包含與 API 相關的附加資料。

因為它是 Python 的例外，你不是 `return`，而是 `raise`。

這也表示，如果你在某個工具函式中（該函式被你的「路徑操作函式」呼叫），並在該工具函式裡 raise `HTTPException`，那麼「路徑操作函式」剩下的程式碼將不會執行；該請求會立刻被終止，並將 `HTTPException` 的 HTTP 錯誤傳回給用戶端。

為何選擇 raise 例外而非回傳值的好處，會在相依性與安全性章節更為明顯。

在這個範例中，當用戶端以不存在的 ID 請求項目時，raise 一個狀態碼為 `404` 的例外：

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[11] *}

### 回應結果 { #the-resulting-response }

如果用戶端請求 `http://example.com/items/foo`（`item_id` 為 `"foo"`），會收到 200 的 HTTP 狀態碼，以及以下 JSON 回應：

```JSON
{
  "item": "The Foo Wrestlers"
}
```

但如果用戶端請求 `http://example.com/items/bar`（不存在的 `item_id` `"bar"`），會收到 404（"not found"）的 HTTP 狀態碼，以及以下 JSON 回應：

```JSON
{
  "detail": "Item not found"
}
```

/// tip

在 raise 一個 `HTTPException` 時，你可以將任何可轉為 JSON 的值作為 `detail` 參數，不只限於 `str`。

你可以傳入 `dict`、`list` 等。

**FastAPI** 會自動處理並轉為 JSON。

///

## 新增自訂標頭 { #add-custom-headers }

有些情況需要在 HTTP 錯誤回應中加入自訂標頭，例如某些安全性情境。

你大概不需要在程式碼中直接使用。

但若你在進階情境中需要，可以這樣加入自訂標頭：

{* ../../docs_src/handling_errors/tutorial002_py310.py hl[14] *}

## 安裝自訂例外處理器 { #install-custom-exception-handlers }

你可以使用 <a href="https://www.starlette.dev/exceptions/" class="external-link" target="_blank">Starlette 的相同例外工具</a> 來加入自訂例外處理器。

假設你有一個自訂例外 `UnicornException`，你（或你使用的函式庫）可能會 `raise` 它。

而你想用 FastAPI 全域處理這個例外。

你可以使用 `@app.exception_handler()` 加入自訂例外處理器：

{* ../../docs_src/handling_errors/tutorial003_py310.py hl[5:7,13:18,24] *}

在這裡，如果你請求 `/unicorns/yolo`，該「路徑操作」會 `raise` 一個 `UnicornException`。

但它會被 `unicorn_exception_handler` 所處理。

因此你會得到一個乾淨的錯誤回應，HTTP 狀態碼為 `418`，JSON 內容如下：

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | 技術細節

你也可以使用 `from starlette.requests import Request` 與 `from starlette.responses import JSONResponse`。

**FastAPI** 以便利性為由，提供和 `starlette.responses` 相同的介面於 `fastapi.responses`。但大多數可用的回應類型其實直接來自 Starlette。`Request` 也一樣。

///

## 覆寫預設例外處理器 { #override-the-default-exception-handlers }

**FastAPI** 內建了一些預設例外處理器。

這些處理器負責在你 `raise` 一個 `HTTPException` 或請求帶有無效資料時，回傳預設的 JSON 回應。

你可以用自己的處理器來覆寫它們。

### 覆寫請求驗證例外 { #override-request-validation-exceptions }

當請求包含無效資料時，**FastAPI** 會在內部 raise 一個 `RequestValidationError`。

它同時也包含了對應的預設例外處理器。

要覆寫它，匯入 `RequestValidationError`，並用 `@app.exception_handler(RequestValidationError)` 來裝飾你的例外處理器。

例外處理器會接收一個 `Request` 和該例外。

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[2,14:19] *}

現在，如果你前往 `/items/foo`，預設的 JSON 錯誤本應為：

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

你將會改而得到文字版：

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### 覆寫 `HTTPException` 的錯誤處理器 { #override-the-httpexception-error-handler }

同樣地，你也可以覆寫 `HTTPException` 的處理器。

例如，你可能想在這些錯誤時回傳純文字而非 JSON：

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[3:4,9:11,25] *}

/// note | 技術細節

你也可以使用 `from starlette.responses import PlainTextResponse`。

**FastAPI** 以便利性為由，提供和 `starlette.responses` 相同的介面於 `fastapi.responses`。但大多數可用的回應類型其實直接來自 Starlette。

///

/// warning

請注意，`RequestValidationError` 內含驗證錯誤發生的檔名與行號，如果你願意，可以在日誌中顯示這些相關資訊。

但這也代表如果你只是把它轉成字串並直接回傳，可能會洩漏一些關於你系統的資訊。因此這裡的程式碼會分別擷取並顯示每個錯誤。

///

### 使用 `RequestValidationError` 的 body { #use-the-requestvalidationerror-body }

`RequestValidationError` 包含它收到的（但無效的）`body`。

在開發應用時，你可以用它來記錄 body 並除錯、回傳給使用者等。

{* ../../docs_src/handling_errors/tutorial005_py310.py hl[14] *}

現在嘗試送出一個無效的項目，例如：

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

你會收到一個告知資料無效、且包含所收到 body 的回應：

```JSON hl_lines="12-15"
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### FastAPI 的 `HTTPException` 與 Starlette 的 `HTTPException` { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI** 有自己定義的 `HTTPException`。

而 **FastAPI** 的 `HTTPException` 錯誤類別是繼承自 Starlette 的 `HTTPException` 錯誤類別。

唯一的差異是，**FastAPI** 的 `HTTPException` 在 `detail` 欄位接受任何可轉為 JSON 的資料，而 Starlette 的 `HTTPException` 只接受字串。

因此，在你的程式碼中，你可以一如往常地 raise **FastAPI** 的 `HTTPException`。

但當你註冊例外處理器時，應該針對 Starlette 的 `HTTPException` 來註冊。

如此一來，如果 Starlette 的內部程式碼，或任何 Starlette 擴充/外掛 raise 了 Starlette 的 `HTTPException`，你的處理器就能攔截並處理它。

在這個範例中，為了能在同一份程式碼中同時使用兩種 `HTTPException`，我們把 Starlette 的例外重新命名為 `StarletteHTTPException`：

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### 重用 **FastAPI** 的例外處理器 { #reuse-fastapis-exception-handlers }

如果你想在使用例外的同時，沿用 **FastAPI** 的預設例外處理器，你可以從 `fastapi.exception_handlers` 匯入並重用預設的處理器：

{* ../../docs_src/handling_errors/tutorial006_py310.py hl[2:5,15,21] *}

在這個範例中，你只是用一段很生動的訊息把錯誤印出來，不過重點是：你可以使用該例外，然後直接重用預設的例外處理器。
