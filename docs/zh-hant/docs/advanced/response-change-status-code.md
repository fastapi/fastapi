# 回應 - 變更狀態碼 { #response-change-status-code }

你可能已經讀過，可以設定預設的[回應狀態碼](../tutorial/response-status-code.md){.internal-link target=_blank}。

但有些情況你需要回傳與預設不同的狀態碼。

## 使用情境 { #use-case }

例如，假設你預設想回傳 HTTP 狀態碼 "OK" `200`。

但如果資料不存在，你想要建立它，並回傳 HTTP 狀態碼 "CREATED" `201`。

同時你仍希望能用 `response_model` 過濾並轉換所回傳的資料。

在這些情況下，你可以使用 `Response` 參數。

## 使用 `Response` 參數 { #use-a-response-parameter }

你可以在你的路徑操作函式（path operation function）中宣告一個 `Response` 型別的參數（就像你可以對 Cookies 和標頭那樣）。

接著你可以在那個「*暫時的*」回應物件上設定 `status_code`。

{* ../../docs_src/response_change_status_code/tutorial001_py310.py hl[1,9,12] *}

然後你可以照常回傳任何需要的物件（例如 `dict`、資料庫模型等）。

若你宣告了 `response_model`，它仍會被用來過濾並轉換你回傳的物件。

FastAPI 會使用那個「*暫時的*」回應來取得狀態碼（以及 Cookies 和標頭），並將它們放入最終回應中；最終回應包含你回傳的值，且會被任何 `response_model` 過濾。

你也可以在相依性（dependencies）中宣告 `Response` 參數，並在其中設定狀態碼。但請注意，最後被設定的值會生效。
