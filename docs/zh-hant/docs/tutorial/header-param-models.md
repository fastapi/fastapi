# 標頭參數模型 { #header-parameter-models }

如果你有一組相關的標頭參數，可以建立一個 Pydantic 模型來宣告它們。

這能讓你在多處重複使用該模型，並一次性為所有參數宣告驗證與中繼資料。😎

/// note | 注意

自 FastAPI 版本 `0.115.0` 起支援。🤓

///

## 以 Pydantic 模型宣告標頭參數 { #header-parameters-with-a-pydantic-model }

在 Pydantic 模型中宣告你需要的標頭參數，然後將參數宣告為 `Header`：

{* ../../docs_src/header_param_models/tutorial001.py hl[9:14,18] *}

FastAPI 會從請求的標頭為每個欄位擷取資料，並交給你已定義的 Pydantic 模型實例。

## 檢視文件 { #check-the-docs }

你可以在 `/docs` 的文件介面看到所需的標頭：

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## 禁止額外標頭 { #forbid-extra-headers }

在某些特殊情境（可能不常見）下，你可能想限制允許接收的標頭。

你可以使用 Pydantic 的模型設定來 `forbid` 任何 `extra` 欄位：

{* ../../docs_src/header_param_models/tutorial002.py hl[10] *}

如果用戶端嘗試傳送額外的標頭，會收到錯誤回應。

例如，用戶端若傳送名為 `tool`、值為 `plumbus` 的標頭，會收到錯誤回應，指出不允許標頭參數 `tool`：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## 停用底線轉換 { #disable-convert-underscores }

與一般標頭參數相同，當參數名稱包含底線字元時，會自動轉換為連字號。

例如，若在程式碼中有標頭參數 `save_data`，實際期望的 HTTP 標頭為 `save-data`，在文件中也會如此顯示。

如果因某些原因需要停用這個自動轉換，你也可以在標頭參數的 Pydantic 模型上設定。

{* ../../docs_src/header_param_models/tutorial003.py hl[19] *}

/// warning | 警告

在將 `convert_underscores` 設為 `False` 之前，請注意有些 HTTP 代理與伺服器不允許含有底線的標頭。

///

## 組合參數模型 { #combine-parameter-models }

你可以將多個標頭參數模型與個別標頭參數及依賴項組合使用。每個模型的資料都會獨立擷取與驗證，如[查詢參數模型](query-param-models.md#combine-parameter-models)中所述。

每個模型的 `extra` 設定都適用於所有標頭參數，包括在其他模型或依賴項中宣告的參數。設定 `extra="forbid"` 時，該模型以外的任何標頭都會被拒絕。設定 `extra="allow"` 時，這些標頭會納入模型的額外欄位。

每個模型在讀取請求與產生 OpenAPI 時，都會使用自己的 `Header(convert_underscores=...)` 設定。明確指定的欄位別名會保留原樣作為標頭名稱。

## 可選的標頭參數模型 { #optional-header-parameter-models }

宣告標頭參數模型時，使用 `| None` 並將預設值設為 `None`，即可讓這組參數變為可選。

{* ../../docs_src/header_param_models/tutorial004.py hl[15] *}

如果未傳送 `x-client-name` 和 `x-client-version`，`client` 就是 `None`。如果傳送了其中任一標頭，FastAPI 就會驗證模型，並要求兩個欄位都必須提供。

預設值、額外欄位與 OpenAPI 的規則與[可選的查詢參數模型](query-param-models.md#optional-query-parameter-models)相同。

`Host` 等標頭也會遵循模型的 `extra` 設定。設定 `extra="allow"` 時，即使兩個宣告的欄位都未提供，這些標頭也會使模型被視為已提供。

## 摘要 { #summary }

你可以在 FastAPI 中使用 Pydantic 模型宣告標頭。😎
