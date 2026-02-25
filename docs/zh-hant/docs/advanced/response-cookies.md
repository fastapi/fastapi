# 回應 Cookie { #response-cookies }

## 使用 `Response` 參數 { #use-a-response-parameter }

你可以在路徑操作函式（path operation function）中宣告一個型別為 `Response` 的參數。

接著你可以在那個「暫時」的 `Response` 物件上設定 Cookie。

{* ../../docs_src/response_cookies/tutorial002_py310.py hl[1, 8:9] *}

之後如常回傳你需要的任何物件（例如 `dict`、資料庫模型等）。

如果你宣告了 `response_model`，它仍會用來過濾並轉換你回傳的物件。

FastAPI 會使用那個暫時的 `Response` 取出 Cookie（以及標頭與狀態碼），並將它們放入最終回應；最終回應包含你回傳的值，且會套用任何 `response_model` 的過濾。

你也可以在相依項（dependencies）中宣告 `Response` 參數，並在其中設定 Cookie（與標頭）。

## 直接回傳 `Response` { #return-a-response-directly }

當你在程式碼中直接回傳 `Response` 時，也可以建立 Cookie。

要這麼做，你可以依照 [直接回傳 Response](response-directly.md){.internal-link target=_blank} 中的說明建立一個回應。

接著在其中設定 Cookie，然後回傳它：

{* ../../docs_src/response_cookies/tutorial001_py310.py hl[10:12] *}

/// tip | 提示

請注意，如果你不是使用 `Response` 參數，而是直接回傳一個 `Response`，FastAPI 會原樣回傳它。

因此你必須確保資料型別正確；例如，如果你回傳的是 `JSONResponse`，就要確保資料可與 JSON 相容。

同時也要確認沒有送出原本應該由 `response_model` 過濾的資料。

///

### 更多資訊 { #more-info }

/// note | 技術細節

你也可以使用 `from starlette.responses import Response` 或 `from starlette.responses import JSONResponse`。

為了方便開發者，FastAPI 也將相同的 `starlette.responses` 透過 `fastapi.responses` 提供。不過，大多數可用的回應類別都直接來自 Starlette。

另外由於 `Response` 常用於設定標頭與 Cookie，FastAPI 也在 `fastapi.Response` 提供了它。

///

想查看所有可用的參數與選項，請參閱 <a href="https://www.starlette.dev/responses/#set-cookie" class="external-link" target="_blank">Starlette 文件</a>。
