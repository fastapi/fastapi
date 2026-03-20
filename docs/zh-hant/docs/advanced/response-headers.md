# 回應標頭 { #response-headers }

## 使用 `Response` 參數 { #use-a-response-parameter }

你可以在你的*路徑操作函式（path operation function）*中宣告一個 `Response` 型別的參數（就像處理 Cookie 一樣）。

然後你可以在那個*暫時性的* `Response` 物件上設定標頭。

{* ../../docs_src/response_headers/tutorial002_py310.py hl[1, 7:8] *}

接著你可以像平常一樣回傳任何你需要的物件（`dict`、資料庫模型等）。

如果你宣告了 `response_model`，它仍會用來過濾並轉換你回傳的物件。

FastAPI 會使用那個暫時性的回應來擷取標頭（還有 Cookie 與狀態碼），並把它們放到最終回應中；最終回應包含你回傳的值，且會依任何 `response_model` 進行過濾。

你也可以在依賴中宣告 `Response` 參數，並在其中設定標頭（與 Cookie）。

## 直接回傳 `Response` { #return-a-response-directly }

當你直接回傳 `Response` 時，也能加入標頭。

依照[直接回傳 Response](response-directly.md){.internal-link target=_blank}中的說明建立回應，並把標頭作為額外參數傳入：

{* ../../docs_src/response_headers/tutorial001_py310.py hl[10:12] *}

/// note | 技術細節

你也可以使用 `from starlette.responses import Response` 或 `from starlette.responses import JSONResponse`。

為了方便開發者，FastAPI 提供與 `starlette.responses` 相同的內容於 `fastapi.responses`。但大多數可用的回應類型其實直接來自 Starlette。

由於 `Response` 常用來設定標頭與 Cookie，FastAPI 也在 `fastapi.Response` 提供了它。

///

## 自訂標頭 { #custom-headers }

請記住，專有的自訂標頭可以<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">使用 `X-` 前綴</a>來新增。

但如果你有自訂標頭並希望瀏覽器端的客戶端能看見它們，你需要把這些標頭加入到 CORS 設定中（詳見 [CORS（跨來源資源共用）](../tutorial/cors.md){.internal-link target=_blank}），使用在<a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette 的 CORS 文件</a>中記載的 `expose_headers` 參數。
