# 額外的狀態碼 { #additional-status-codes }

在預設情況下，**FastAPI** 會使用 `JSONResponse` 傳回回應，並把你從你的「路徑操作（path operation）」回傳的內容放進該 `JSONResponse` 中。

它會使用預設的狀態碼，或你在路徑操作中設定的狀態碼。

## 額外的狀態碼 { #additional-status-codes_1 }

如果你想在主要狀態碼之外再回傳其他狀態碼，可以直接回傳一個 `Response`（例如 `JSONResponse`），並直接設定你想要的額外狀態碼。

例如，你想要有一個允許更新項目的路徑操作，成功時回傳 HTTP 狀態碼 200 "OK"。

但你也希望它能接受新項目；當項目先前不存在時就建立它們，並回傳 HTTP 狀態碼 201 "Created"。

要達成這點，匯入 `JSONResponse`，直接在那裡回傳內容，並設定你想要的 `status_code`：

{* ../../docs_src/additional_status_codes/tutorial001_an_py310.py hl[4,25] *}

/// warning

當你直接回傳一個 `Response`（就像上面的範例），它會原封不動地被送出。

不會再經過模型序列化等處理。

請確認其中包含你要的資料，且各值是合法的 JSON（如果你使用的是 `JSONResponse`）。

///

/// note | 注意

你也可以使用 `from starlette.responses import JSONResponse`。

**FastAPI** 也將同樣的 `starlette.responses` 以 `fastapi.responses` 的形式提供，純粹是為了讓你（開發者）更方便。但大多數可用的回應類別其實都直接來自 Starlette。`status` 也一樣。

///

## OpenAPI 與 API 文件 { #openapi-and-api-docs }

如果你直接回傳額外的狀態碼與回應，它們不會被包含進 OpenAPI 綱要（API 文件）中，因為 FastAPI 無法事先知道你會回傳什麼。

但你可以在程式碼中補充文件，使用：[額外的回應](additional-responses.md){.internal-link target=_blank}。
