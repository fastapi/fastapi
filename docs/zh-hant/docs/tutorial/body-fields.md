# Body - 欄位 { #body-fields }

就像你可以在「路徑操作函式 (path operation function)」的參數中用 `Query`、`Path` 和 `Body` 宣告額外的驗證與中繼資料一樣，你也可以在 Pydantic 模型中使用 Pydantic 的 `Field` 來宣告驗證與中繼資料。

## 匯入 `Field` { #import-field }

首先，你需要匯入它：

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[4] *}


/// warning

請注意，`Field` 是直接從 `pydantic` 匯入的，不像其他（如 `Query`、`Path`、`Body` 等）是從 `fastapi` 匯入。

///

## 宣告模型屬性 { #declare-model-attributes }

接著你可以在模型屬性上使用 `Field`：

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[11:14] *}

`Field` 的用法與 `Query`、`Path`、`Body` 相同，擁有相同的參數等。

/// note | 技術細節

實際上，你接下來會看到的 `Query`、`Path` 等，會建立共同父類別 `Param` 的子類別物件，而 `Param` 本身是 Pydantic 的 `FieldInfo` 類別的子類別。

而 Pydantic 的 `Field` 也會回傳一個 `FieldInfo` 的實例。

`Body` 也會直接回傳 `FieldInfo` 子類別的物件。稍後你會看到還有其他類別是 `Body` 類別的子類別。

記得，當你從 `fastapi` 匯入 `Query`、`Path` 等時，它們其實是回傳特殊類別的函式。

///

/// tip

注意，每個帶有型別、預設值與 `Field` 的模型屬性，其結構和「路徑操作函式」的參數相同，只是把 `Path`、`Query`、`Body` 換成了 `Field`。

///

## 加入額外資訊 { #add-extra-information }

你可以在 `Field`、`Query`、`Body` 等中宣告額外資訊。這些資訊會被包含在產生的 JSON Schema 中。

你會在後續文件中學到更多關於加入額外資訊的內容，特別是在宣告範例時。

/// warning

傳入 `Field` 的額外鍵也會出現在你的應用程式所產生的 OpenAPI schema 中。
由於這些鍵不一定屬於 OpenAPI 規格的一部分，一些 OpenAPI 工具（例如 [OpenAPI 驗證器](https://validator.swagger.io/)）可能無法處理你產生的 schema。

///

## 回顧 { #recap }

你可以使用 Pydantic 的 `Field` 為模型屬性宣告額外的驗證與中繼資料。

你也可以使用額外的關鍵字引數來傳遞額外的 JSON Schema 中繼資料。
