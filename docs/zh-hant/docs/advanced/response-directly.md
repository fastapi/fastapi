# 直接回傳 Response { #return-a-response-directly }

當你建立一個 **FastAPI** 的路徑操作 (path operation) 時，通常可以從中回傳任何資料：`dict`、`list`、Pydantic 模型、資料庫模型等。

如果你宣告了 [回應模型](../tutorial/response-model.md)，FastAPI 會用 Pydantic 將資料序列化為 JSON。

如果你沒有宣告回應模型，FastAPI 會使用在[JSON 相容編碼器](../tutorial/encoder.md)中說明的 `jsonable_encoder`，並把它放進 `JSONResponse`。

但你也可以直接從路徑操作回傳 `JSONResponse`。

/// tip

通常使用 [回應模型](../tutorial/response-model.md) 會有更好的效能，因為那樣會在 Rust 端使用 Pydantic 來序列化資料，而不是直接回傳 `JSONResponse`。

///

## 回傳 `Response` { #return-a-response }

其實，你可以回傳任何 `Response`，或其任何子類別。

/// info

`JSONResponse` 本身就是 `Response` 的子類別。

///

當你回傳一個 `Response` 時，**FastAPI** 會直接傳遞它。

它不會對 Pydantic 模型做任何資料轉換，也不會把內容轉成其他型別等。

這給了你很大的彈性。你可以回傳任何資料型別、覆寫任何資料宣告或驗證等。

同時也帶來了很大的責任。你必須確保你回傳的資料是正確的、格式正確、可被序列化等。

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

假設你想要回傳一個 [XML](https://en.wikipedia.org/wiki/XML) 回應。

你可以把 XML 內容放進一個字串，把它放進 `Response`，然後回傳它：

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## 回應模型如何運作 { #how-a-response-model-works }

當你在路徑操作中宣告 [回應模型 - 回傳型別](../tutorial/response-model.md) 時，**FastAPI** 會用 Pydantic 將資料序列化為 JSON。

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

由於這會在 Rust 端發生，效能會比用一般的 Python 與 `JSONResponse` 類別來完成好得多。

當使用 `response_model` 或回傳型別時，FastAPI 不會使用 `jsonable_encoder` 來轉換資料（那會較慢），也不會使用 `JSONResponse` 類別。

相反地，它會取用用回應模型（或回傳型別）透過 Pydantic 產生的 JSON 位元組，並直接回傳具備正確 JSON 媒體型別（`application/json`）的 `Response`。

## 注意事項 { #notes }

當你直接回傳 `Response` 時，其資料不會自動被驗證、轉換（序列化）或文件化。

但你仍然可以依照[在 OpenAPI 中的額外回應](additional-responses.md)中的說明進行文件化。

在後續章節中，你會看到如何在仍保有自動資料轉換、文件化等的同時，使用／宣告這些自訂的 `Response`。
