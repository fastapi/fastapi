# 查詢參數模型 { #query-parameter-models }

如果你有一組具有相關性的**查詢參數**，你可以建立一個 **Pydantic 模型**來聲明它們。

這將允許你在**多個地方**去**重複使用模型**，並且一次性為所有參數聲明驗證和元資料 (metadata)。😎

/// note

FastAPI 從 `0.115.0` 版本開始支援這個特性。🤓

///

## 使用 Pydantic 模型的查詢參數 { #query-parameters-with-a-pydantic-model }

在一個 **Pydantic 模型**中聲明你需要的**查詢參數**，然後將參數聲明為 `Query`：

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** 將會從請求的**查詢參數**中**提取**出**每個欄位**的資料，並將其提供給你定義的 Pydantic 模型。

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

## 合併參數模型 { #combine-parameter-models }

你可以宣告多個查詢參數模型，並將它們與個別的查詢參數或相依性合併使用。

{* ../../docs_src/query_param_models/tutorial003_an_py310.py hl[9:15,20:22] *}

請求參數會維持在同一層級。

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

查詢字串中不會有 `pagination` 或 `filters` 鍵。每個模型會以自己的預設值、欄位驗證器與模型驗證器獨立驗證查詢參數。當模型或個別參數是在相依性中宣告時，也是如此。

如果多個模型共用參數名稱或別名，每個模型都會獨立驗證該請求參數。請為各自獨立的值使用不同的名稱或別名。OpenAPI 對於共用的參數只會列出一次，就像對在相依性中共用的參數一樣，因此共用的宣告應描述相同的型別與限制條件。

每個模型的 `extra` 設定會套用至所有查詢參數，包括在其他模型或相依性中宣告的參數。使用 `extra="forbid"` 時，任何不在該模型內的參數都會被拒絕。使用 `extra="allow"` 時，這些參數會以模型額外欄位的形式納入。

這也適用於 `Header` 與 `Cookie` 模型。

## 可選的查詢參數模型 { #optional-query-parameter-models }

將查詢參數模型宣告為 `| None` 並將預設值設為 `None`，即可讓整組參數成為可選。

{* ../../docs_src/query_param_models/tutorial004_an_py310.py hl[18] *}

如果 `start` 和 `end` 都沒有傳送，`date_range` 會是 `None`。如果其中任一有傳送，FastAPI 會驗證模型並要求兩個欄位都提供。

使用 `| None` 但沒有預設值，仍會讓該參數成為必填。

額外參數會遵循模型的 `extra` 設定。被忽略的額外參數不會讓模型被視為已提供。

OpenAPI 會個別列出該組的欄位，並將它們標示為可選。

你也可以宣告可選的[標頭參數模型](header-param-models.md#optional-header-parameter-models)與 [Cookie 參數模型](cookie-param-models.md#optional-cookie-parameter-models)。

## 總結 { #summary }

你可以使用 **Pydantic 模型**在 **FastAPI** 中聲明**查詢參數**。😎

/// tip

劇透警告：你也可以使用 Pydantic 模型來聲明 cookie 和 headers，但你將在本教學的後面部分閱讀到這部分內容。🤫

///
