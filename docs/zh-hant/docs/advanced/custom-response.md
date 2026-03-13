# 自訂回應——HTML、串流、檔案與其他 { #custom-response-html-stream-file-others }

預設情況下，**FastAPI** 會使用 `JSONResponse` 傳回回應。

你可以像在[直接回傳 Response](response-directly.md){.internal-link target=_blank} 中所示，直接回傳一個 `Response` 來覆寫它。

但如果你直接回傳一個 `Response`（或其子類別，如 `JSONResponse`），資料將不會被自動轉換（即使你宣告了 `response_model`），而且文件也不會自動產生（例如，在產生的 OpenAPI 中包含 HTTP 標頭 `Content-Type` 的特定「media type」）。

你也可以在「路徑操作裝飾器」中使用 `response_class` 參數，宣告要使用的 `Response`（例如任意 `Response` 子類別）。

你從「路徑操作函式」回傳的內容，會被放進該 `Response` 中。

若該 `Response` 的 media type 是 JSON（`application/json`），像 `JSONResponse` 與 `UJSONResponse`，則你回傳的資料會自動以你在「路徑操作裝飾器」中宣告的 Pydantic `response_model` 進行轉換（與過濾）。

/// note

若你使用的回應類別沒有 media type，FastAPI 會假設你的回應沒有內容，因此不會在產生的 OpenAPI 文件中記錄回應格式。

///

## 使用 `ORJSONResponse` { #use-orjsonresponse }

例如，若你在追求效能，你可以安裝並使用 <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>，並將回應設為 `ORJSONResponse`。

匯入你想使用的 `Response` 類別（子類），並在「路徑操作裝飾器」中宣告它。

對於大型回應，直接回傳 `Response` 會比回傳 `dict` 快得多。

這是因為預設情況下，FastAPI 會檢查每個項目並確認它能被序列化為 JSON，使用與教學中說明的相同[JSON 相容編碼器](../tutorial/encoder.md){.internal-link target=_blank}。這使你可以回傳「任意物件」，例如資料庫模型。

但如果你確定你回傳的內容「可以用 JSON 序列化」，你可以直接將它傳給回應類別，避免 FastAPI 在把你的回傳內容交給回應類別之前，先經過 `jsonable_encoder` 所帶來的額外開銷。

{* ../../docs_src/custom_response/tutorial001b_py310.py hl[2,7] *}

/// info

參數 `response_class` 也會用來定義回應的「media type」。

在此情況下，HTTP 標頭 `Content-Type` 會被設為 `application/json`。

而且它會以此形式被記錄到 OpenAPI 中。

///

/// tip

`ORJSONResponse` 只在 FastAPI 中可用，在 Starlette 中不可用。

///

## HTML 回應 { #html-response }

要直接從 **FastAPI** 回傳 HTML，使用 `HTMLResponse`。

- 匯入 `HTMLResponse`。
- 在「路徑操作裝飾器」中，將 `HTMLResponse` 傳給 `response_class` 參數。

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info

參數 `response_class` 也會用來定義回應的「media type」。

在此情況下，HTTP 標頭 `Content-Type` 會被設為 `text/html`。

而且它會以此形式被記錄到 OpenAPI 中。

///

### 回傳 `Response` { #return-a-response }

如[直接回傳 Response](response-directly.md){.internal-link target=_blank} 所示，你也可以在「路徑操作」中直接回傳以覆寫回應。

上面的相同範例，回傳 `HTMLResponse`，可以像這樣：

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning

由你的「路徑操作函式」直接回傳的 `Response` 不會被記錄進 OpenAPI（例如不會記錄 `Content-Type`），也不會出現在自動產生的互動式文件中。

///

/// info

當然，實際的 `Content-Type` 標頭、狀態碼等，會來自你回傳的 `Response` 物件。

///

### 在 OpenAPI 中文件化並覆寫 `Response` { #document-in-openapi-and-override-response }

如果你想在函式內覆寫回應，同時又要在 OpenAPI 中記錄「media type」，你可以同時使用 `response_class` 參數並回傳一個 `Response` 物件。

此時，`response_class` 只會用於記錄該 OpenAPI「路徑操作」，而你回傳的 `Response` 將會如實使用。

#### 直接回傳 `HTMLResponse` { #return-an-htmlresponse-directly }

例如，可能會像這樣：

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

在這個例子中，函式 `generate_html_response()` 已經產生並回傳了一個 `Response`，而不是把 HTML 當作 `str` 回傳。

透過回傳 `generate_html_response()` 的結果，你其實已經回傳了一個 `Response`，這會覆寫 **FastAPI** 的預設行為。

但因為你同時也在 `response_class` 中傳入了 `HTMLResponse`，**FastAPI** 便能在 OpenAPI 與互動式文件中，將其以 `text/html` 的 HTML 形式記錄：

<img src="/img/tutorial/custom-response/image01.png">

## 可用的回應 { #available-responses }

以下是一些可用的回應類別。

記得你可以用 `Response` 回傳其他任何東西，甚至建立自訂的子類別。

/// note | 技術細節

你也可以使用 `from starlette.responses import HTMLResponse`。

**FastAPI** 將 `starlette.responses` 以 `fastapi.responses` 提供給你（開發者）做為方便之用。但大多數可用的回應其實直接來自 Starlette。

///

### `Response` { #response }

主要的 `Response` 類別，其他回應皆繼承自它。

你也可以直接回傳它。

它接受以下參數：

- `content` - `str` 或 `bytes`。
- `status_code` - `int` 類型的 HTTP 狀態碼。
- `headers` - 由字串組成的 `dict`。
- `media_type` - 描述 media type 的 `str`。例如 `"text/html"`。

FastAPI（實際上是 Starlette）會自動包含 Content-Length 標頭。也會根據 `media_type`（並為文字型別附加 charset）包含 Content-Type 標頭。

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

接收文字或位元組並回傳 HTML 回應，如上所述。

### `PlainTextResponse` { #plaintextresponse }

接收文字或位元組並回傳純文字回應。

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

接收資料並回傳 `application/json` 編碼的回應。

這是 **FastAPI** 的預設回應，如上所述。

### `ORJSONResponse` { #orjsonresponse }

使用 <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> 的快速替代 JSON 回應，如上所述。

/// info

這需要安裝 `orjson`，例如使用 `pip install orjson`。

///

### `UJSONResponse` { #ujsonresponse }

使用 <a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a> 的替代 JSON 回應。

/// info

這需要安裝 `ujson`，例如使用 `pip install ujson`。

///

/// warning

`ujson` 在處理某些邊界情況時，沒那麼嚴謹，較 Python 內建實作更「隨意」。

///

{* ../../docs_src/custom_response/tutorial001_py310.py hl[2,7] *}

/// tip

`ORJSONResponse` 可能是更快的替代方案。

///

### `RedirectResponse` { #redirectresponse }

回傳一個 HTTP 重新導向。預設使用 307 狀態碼（Temporary Redirect）。

你可以直接回傳 `RedirectResponse`：

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

或者你可以在 `response_class` 參數中使用它：

{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

若這麼做，你就可以在「路徑操作函式」中直接回傳 URL。

在此情況下，所使用的 `status_code` 會是 `RedirectResponse` 的預設值 `307`。

---

你也可以同時搭配 `status_code` 與 `response_class` 參數：

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

接收一個 async 產生器或一般的產生器／疊代器，並以串流方式傳送回應本文。

{* ../../docs_src/custom_response/tutorial007_py310.py hl[2,14] *}

#### 對「類檔案物件」使用 `StreamingResponse` { #using-streamingresponse-with-file-like-objects }

如果你有一個<a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">類檔案（file-like）</a>物件（例如 `open()` 回傳的物件），你可以建立一個產生器函式來疊代該類檔案物件。

如此一來，你不必先把它全部讀進記憶體，就能將那個產生器函式傳給 `StreamingResponse` 並回傳。

這也包含許多用於雲端儲存、影像／影音處理等的函式庫。

{* ../../docs_src/custom_response/tutorial008_py310.py hl[2,10:12,14] *}

1. 這是產生器函式。因為它內含 `yield` 陳述式，所以是「產生器函式」。
2. 透過 `with` 區塊，我們確保在產生器函式結束後關閉類檔案物件。因此，在完成傳送回應後就會關閉。
3. 這個 `yield from` 告訴函式去疊代名為 `file_like` 的東西。對於每個被疊代到的部分，就把該部分當作此產生器函式（`iterfile`）的輸出進行 `yield`。

    因此，這是一個把「生成」工作在內部轉交給其他東西的產生器函式。

    透過這樣做，我們可以把它放進 `with` 區塊，藉此確保在完成後關閉類檔案物件。

/// tip

注意，這裡我們使用的是標準的 `open()`，它不支援 `async` 與 `await`，因此我們用一般的 `def` 來宣告路徑操作。

///

### `FileResponse` { #fileresponse }

以非同步串流方式將檔案作為回應。

它在初始化時所需的參數與其他回應型別不同：

- `path` - 要串流的檔案路徑。
- `headers` - 要包含的自訂標頭，字典形式。
- `media_type` - 描述 media type 的字串。若未設定，將根據檔名或路徑推斷 media type。
- `filename` - 若設定，會包含在回應的 `Content-Disposition` 中。

檔案回應會包含適當的 `Content-Length`、`Last-Modified` 與 `ETag` 標頭。

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

你也可以使用 `response_class` 參數：

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

在此情況下，你可以在「路徑操作函式」中直接回傳檔案路徑。

## 自訂回應類別 { #custom-response-class }

你可以建立自己的自訂回應類別，繼承自 `Response` 並加以使用。

例如，假設你要使用 <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>，但想套用一些未包含在 `ORJSONResponse` 類別中的自訂設定。

假設你想回傳縮排且格式化的 JSON，因此要使用 orjson 選項 `orjson.OPT_INDENT_2`。

你可以建立 `CustomORJSONResponse`。你主要需要做的是建立一個 `Response.render(content)` 方法，將內容以 `bytes` 回傳：

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

現在，不再是回傳：

```json
{"message": "Hello World"}
```

……這個回應會回傳：

```json
{
  "message": "Hello World"
}
```

當然，你大概能找到比格式化 JSON 更好的方式來利用這個能力。😉

## 預設回應類別 { #default-response-class }

在建立 **FastAPI** 類別實例或 `APIRouter` 時，你可以指定預設要使用哪個回應類別。

用來設定的是 `default_response_class` 參數。

在下面的例子中，**FastAPI** 會在所有「路徑操作」中預設使用 `ORJSONResponse`，而不是 `JSONResponse`。

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip

你仍然可以在「路徑操作」中像以前一樣覆寫 `response_class`。

///

## 其他文件化選項 { #additional-documentation }

你也可以在 OpenAPI 中使用 `responses` 宣告 media type 與其他許多細節：[在 OpenAPI 中的額外回應](additional-responses.md){.internal-link target=_blank}。
