# CORS（跨來源資源共用） { #cors-cross-origin-resource-sharing }

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS 或「Cross-Origin Resource Sharing」</a>指的是：當在瀏覽器中執行的前端以 JavaScript 與後端通訊，而後端與前端位於不同「來源（origin）」時的情境。

## 來源（Origin） { #origin }

一個來源是由通訊協定（`http`、`https`）、網域（`myapp.com`、`localhost`、`localhost.tiangolo.com`）與連接埠（`80`、`443`、`8080`）三者組合而成。

因此，以下皆是不同的來源：

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

即使它們都在 `localhost`，但使用了不同的通訊協定或連接埠，所以它們是不同的「來源」。

## 步驟 { #steps }

假設你的前端在瀏覽器中執行於 `http://localhost:8080`，其 JavaScript 嘗試與執行在 `http://localhost` 的後端通訊（因為未指定連接埠，瀏覽器會假設預設連接埠為 `80`）。

接著，瀏覽器會向 `:80` 的後端送出一個 HTTP `OPTIONS` 請求；若後端回傳適當的標頭，授權此不同來源（`http://localhost:8080`）的通訊，則在 `:8080` 的瀏覽器就會允許前端的 JavaScript 向 `:80` 的後端送出它的請求。

為了達成這點，`:80` 的後端必須有一份「允許的來源」清單。

在此情況下，該清單必須包含 `http://localhost:8080`，` :8080` 的前端才能正確運作。

## 萬用字元 { #wildcards }

也可以將清單宣告為 `"*"`（「wildcard」萬用字元），表示全部都允許。

但那只會允許某些類型的通訊，凡是涉及憑證（credentials）的都會被排除：例如 Cookie、Authorization 標頭（像 Bearer Token 會用到的）等。

因此，為了讓一切正常運作，最好明確指定被允許的來源。

## 使用 `CORSMiddleware` { #use-corsmiddleware }

你可以在 **FastAPI** 應用程式中使用 `CORSMiddleware` 來設定：

* 匯入 `CORSMiddleware`。
* 建立允許的來源清單（字串）。
* 將它加入到你的 **FastAPI** 應用程式做為「中介軟體（middleware）」。

你也可以指定你的後端是否允許：

* 憑證（credentials，例如 Authorization 標頭、Cookie 等）。
* 特定的 HTTP 方法（如 `POST`、`PUT`），或使用萬用字元 `"*"` 表示全部。
* 特定的 HTTP 標頭，或使用萬用字元 `"*"` 表示全部。

{* ../../docs_src/cors/tutorial001_py310.py hl[2,6:11,13:19] *}

`CORSMiddleware` 的實作在預設參數上相當嚴格，因此你需要明確啟用特定的來源、方法或標頭，瀏覽器才會允許在跨網域情境中使用它們。

支援以下參數：

* `allow_origins` - 允許進行跨來源請求的來源清單。例如 `['https://example.org', 'https://www.example.org']`。你可以使用 `['*']` 來允許任何來源。
* `allow_origin_regex` - 允許進行跨來源請求的來源，使用正規表示式字串比對。例如 `'https://.*\.example\.org'`。
* `allow_methods` - 允許跨來源請求的 HTTP 方法清單。預設為 `['GET']`。你可以使用 `['*']` 來允許所有標準方法。
* `allow_headers` - 允許跨來源請求所支援的 HTTP 請求標頭清單。預設為 `[]`。你可以使用 `['*']` 來允許所有標頭。對於<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests" class="external-link" rel="noopener" target="_blank">簡單 CORS 請求</a>，`Accept`、`Accept-Language`、`Content-Language` 與 `Content-Type` 標頭一律被允許。
* `allow_credentials` - 指示是否支援跨來源請求的 Cookie。預設為 `False`。

    當 `allow_credentials` 設為 `True` 時，`allow_origins`、`allow_methods` 與 `allow_headers` 都不能設為 `['*']`。上述各項必須<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#credentialed_requests_and_wildcards" class="external-link" rel="noopener" target="_blank">明確指定</a>。

* `expose_headers` - 指示哪些回應標頭應該讓瀏覽器可存取。預設為 `[]`。
* `max_age` - 設定瀏覽器快取 CORS 回應的最長秒數。預設為 `600`。

此中介軟體會回應兩種特定的 HTTP 請求類型...

### CORS 預檢請求 { #cors-preflight-requests }

任何帶有 `Origin` 與 `Access-Control-Request-Method` 標頭的 `OPTIONS` 請求。

在這種情況下，中介軟體會攔截傳入的請求並回應適當的 CORS 標頭，並回傳 `200` 或 `400`（僅供資訊參考）。

### 簡單請求 { #simple-requests }

任何帶有 `Origin` 標頭的請求。在這種情況下，中介軟體會如常將請求往下傳遞，但會在回應上加入適當的 CORS 標頭。

## 更多資訊 { #more-info }

想進一步了解 <abbr title="Cross-Origin Resource Sharing - 跨來源資源共用">CORS</abbr>，請參考 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">Mozilla 的 CORS 文件</a>。

/// note | 技術細節

你也可以使用 `from starlette.middleware.cors import CORSMiddleware`。

**FastAPI** 在 `fastapi.middleware` 中提供了幾個中介軟體，做為開發者的便利性。但多數可用的中介軟體其實直接來自 Starlette。

///
