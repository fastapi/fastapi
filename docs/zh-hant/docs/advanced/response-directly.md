# 直接回傳 Response { #return-a-response-directly }

當你建立一個 **FastAPI** 的路徑操作 (path operation) 時，通常可以從中回傳任何資料：`dict`、`list`、Pydantic 模型、資料庫模型等。

預設情況下，**FastAPI** 會使用在[JSON 相容編碼器](../tutorial/encoder.md){.internal-link target=_blank}中說明的 `jsonable_encoder`，自動將回傳值轉為 JSON。

然後在幕後，它會把這些與 JSON 相容的資料（例如 `dict`）放進 `JSONResponse`，用來把回應傳回給用戶端。

但你也可以直接從路徑操作回傳 `JSONResponse`。

例如，當你需要回傳自訂的 headers 或 cookies 時就很有用。

## 回傳 `Response` { #return-a-response }

其實，你可以回傳任何 `Response`，或其任何子類別。

/// tip

`JSONResponse` 本身就是 `Response` 的子類別。

///

當你回傳一個 `Response` 時，**FastAPI** 會直接傳遞它。

它不會對 Pydantic 模型做任何資料轉換，也不會把內容轉成其他型別等。

這給了你很大的彈性。你可以回傳任何資料型別、覆寫任何資料宣告或驗證等。

## 在 `Response` 中使用 `jsonable_encoder` { #using-the-jsonable-encoder-in-a-response }

因為 **FastAPI** 不會對你回傳的 `Response` 做任何更動，你需要自行確保它的內容已經準備好。

例如，你不能直接把一個 Pydantic 模型放進 `JSONResponse`，需要先把它轉成 `dict`，並將所有資料型別（像是 `datetime`、`UUID` 等）轉成與 JSON 相容的型別。

在這些情況下，你可以先用 `jsonable_encoder` 把資料轉好，再傳給回應物件：

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | 技術細節

你也可以使用 `from starlette.responses import JSONResponse`。

**FastAPI** 為了方便開發者，將 `starlette.responses` 也提供為 `fastapi.responses`。但大多數可用的回應類型其實直接來自 Starlette。

///

## 回傳自訂 `Response` { #returning-a-custom-response }

上面的範例展示了所需的各個部分，但目前還不太實用，因為你其實可以直接回傳 `item`，**FastAPI** 就會幫你把它放進 `JSONResponse`，轉成 `dict` 等，這些都是預設行為。

現在來看看如何用它來回傳自訂回應。

假設你想要回傳一個 <a href="https://en.wikipedia.org/wiki/XML" class="external-link" target="_blank">XML</a> 回應。

你可以把 XML 內容放進一個字串，把它放進 `Response`，然後回傳它：

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## 注意事項 { #notes }

當你直接回傳 `Response` 時，其資料不會自動被驗證、轉換（序列化）或文件化。

但你仍然可以依照[在 OpenAPI 中的額外回應](additional-responses.md){.internal-link target=_blank}中的說明進行文件化。

在後續章節中，你會看到如何在仍保有自動資料轉換、文件化等的同時，使用／宣告這些自訂的 `Response`。
