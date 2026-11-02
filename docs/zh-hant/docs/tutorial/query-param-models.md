# 查詢參數模型 { #query-parameter-models }

如果你有一組具有相關性的**查詢參數**，你可以建立一個 **Pydantic 模型**來聲明它們。

這將允許你在**多個地方**去**重複使用模型**，並且一次性為所有參數聲明驗證和元資料 (metadata)。😎

/// note

FastAPI 從 `0.115.0` 版本開始支援這個特性。🤓

///

## 使用 Pydantic 模型的查詢參數 { #query-parameters-with-a-pydantic-model }

在一個 **Pydantic 模型**中聲明你需要的**查詢參數**，然後將參數聲明為 `Query`：

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** 將會從請求的**查詢參數**中**提取**出**每個欄位**的資料，並提供你定義的 Pydantic 模型。

## 查看文件 { #check-the-docs }

你可以在 `/docs` 頁面的 UI 中查看查詢參數：

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## 禁止額外的查詢參數 { #forbid-extra-query-parameters }

在一些特殊的使用場景中（可能不是很常見），你可能希望**限制**你要收到的查詢參數。

你可以使用 Pydantic 的模型設定來 `forbid`（禁止）任何 `extra`（額外）欄位：

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

如果客戶端嘗試在**查詢參數**中發送一些**額外的**資料，他們將會收到一個**錯誤**回應。

例如，如果客戶端嘗試發送一個值為 `plumbus` 的 `tool` 查詢參數，如：

```http
https://example.com/items/?limit=10&tool=plumbus
```

他們將收到一個**錯誤**回應，告訴他們查詢參數 `tool` 是不允許的：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## 組合參數模型 { #combine-parameter-models }

你可以聲明多個查詢參數模型，並將它們與個別的查詢參數或依賴項組合使用。

{* ../../docs_src/query_param_models/tutorial003_an_py310.py hl[9:15,20:22] *}

請求參數仍位於同一層級。

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

查詢字串中沒有 `pagination` 或 `filters` 鍵。每個模型都會使用自己的預設值、欄位驗證器和模型驗證器，獨立驗證查詢參數。在依賴項中聲明模型或個別參數時也同樣適用。

如果模型共用參數名稱或別名，每個模型都會獨立驗證該請求參數。對於獨立的值，請使用不同的名稱或別名。OpenAPI 只會列出共用參數一次，與依賴項共用參數的處理方式相同，因此共用的聲明應描述相同的型別和限制。

每個模型的 `extra` 設定都會套用至所有查詢參數，包括在其他模型或依賴項中聲明的參數。使用 `extra="forbid"` 時，任何不屬於該模型的參數都會被拒絕。使用 `extra="allow"` 時，這些參數會作為額外資料納入模型。

這也適用於 `Header` 和 `Cookie` 模型。

## 可選的查詢參數模型 { #optional-query-parameter-models }

聲明查詢參數模型時使用 `| None` 並將預設值設為 `None`，即可讓這組參數變為可選。

{* ../../docs_src/query_param_models/tutorial004_an_py310.py hl[18] *}

如果未發送 `start` 和 `end`，`date_range` 就會是 `None`。如果發送了其中任一參數，FastAPI 就會驗證模型，並要求提供這兩個欄位。

使用 `| None` 但未設定預設值時，該參數仍為必填。

額外參數會遵循模型的 `extra` 設定。被忽略的額外參數不會使模型被視為已提供。

OpenAPI 會個別列出這組參數的欄位，並將它們標記為可選。

你也可以聲明可選的 [header 參數模型](header-param-models.md#optional-header-parameter-models)和 [cookie 參數模型](cookie-param-models.md#optional-cookie-parameter-models)。

## 總結 { #summary }

你可以使用 **Pydantic 模型**在 **FastAPI** 中聲明**查詢參數**。😎

/// tip

劇透警告：你也可以使用 Pydantic 模型來聲明 cookie 和 headers，但你將在本教學的後面部分閱讀到這部分內容。🤫

///
