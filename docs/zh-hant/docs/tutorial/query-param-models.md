# 查詢參數模型

如果你有一組具有相關性的**查詢參數**，你可以建立一個 **Pydantic 模型**來聲明它們。

這將允許你在**多個地方**去**重複使用模型**，並且一次性為所有參數聲明驗證和元資料 (metadata)。😎

/// note

FastAPI 從 `0.115.0` 版本開始支援這個特性。🤓

///

## 使用 Pydantic 模型的查詢參數

在一個 **Pydantic 模型**中聲明你需要的**查詢參數**，然後將參數聲明為 `Query`：

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** 將會從請求的**查詢參數**中**提取**出**每個欄位**的資料，並將其提供給你定義的 Pydantic 模型。

## 查看文件

你可以在 `/docs` 頁面的 UI 中查看查詢參數：

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## 禁止額外的查詢參數

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

## 總結

你可以使用 **Pydantic 模型**在 **FastAPI** 中聲明**查詢參數**。😎

/// tip

劇透警告：你也可以使用 Pydantic 模型來聲明 cookie 和 headers，但你將在本教學的後面部分閱讀到這部分內容。🤫

///
