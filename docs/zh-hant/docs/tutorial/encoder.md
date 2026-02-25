# JSON 相容編碼器 { #json-compatible-encoder }

在某些情況下，你可能需要將某種資料型別（例如 Pydantic 模型）轉換為與 JSON 相容的類型（例如 `dict`、`list` 等）。

例如，當你需要把它儲存在資料庫中。

為此，**FastAPI** 提供了 `jsonable_encoder()` 函式。

## 使用 `jsonable_encoder` { #using-the-jsonable-encoder }

想像你有一個只接受與 JSON 相容資料的資料庫 `fake_db`。

例如，它不接受 `datetime` 物件，因為那與 JSON 不相容。

因此，必須將 `datetime` 物件轉為一個以 <a href="https://en.wikipedia.org/wiki/ISO_8601" class="external-link" target="_blank">ISO 格式</a> 表示資料的 `str`。

同樣地，這個資料庫不會接受 Pydantic 模型（帶有屬性的物件），只接受 `dict`。

你可以使用 `jsonable_encoder` 來處理。

它接收一個物件（例如 Pydantic 模型），並回傳一個與 JSON 相容的版本：

{* ../../docs_src/encoder/tutorial001_py310.py hl[4,21] *}

在此範例中，它會把 Pydantic 模型轉成 `dict`，並將 `datetime` 轉成 `str`。

呼叫後的結果可以用 Python 標準的 <a href="https://docs.python.org/3/library/json.html#json.dumps" class="external-link" target="_blank">`json.dumps()`</a> 進行編碼。

它不會回傳一個包含 JSON 內容的大型 `str`（字串）。它會回傳 Python 標準的資料結構（例如 `dict`），其中的值與子值都與 JSON 相容。

/// note

事實上，`jsonable_encoder` 在 **FastAPI** 內部也被用來轉換資料。不過在許多其他情境中它同樣實用。

///
